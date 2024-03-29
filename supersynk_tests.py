import unittest
from supersynk import PayloadValidator, Channel, Channels

class PayloadValidatorTest(unittest.TestCase):

    def setUp(self):
        self.validator = PayloadValidator()

    def test_validate_input_is_none(self):
        res = self.validator.get_input_validation(None)
        self.assertEqual(PayloadValidator.INPUT_IS_NONE, res)

    def test_validate_input_is_empty_string(self):
        res = self.validator.get_input_validation(r'')
        self.assertEqual(PayloadValidator.INPUT_IS_EMPTY_STRING, res)

    def test_validate_input_is_not_json(self):
        res = self.validator.get_input_validation(r'-')
        self.assertEqual(PayloadValidator.INPUT_IS_NOT_JSON, res)

    def test_validate_client_id_not_found(self):
        res = self.validator.get_input_validation(r'{"a":"b"}')
        self.assertEqual(PayloadValidator.CLIENT_ID_IS_NOT_FOUND, res)

    def test_validate_client_id_not_str(self):
        res = self.validator.get_input_validation(r'{"client_id":0}')
        self.assertEqual(PayloadValidator.CLIENT_ID_IS_NOT_STR, res)

    def test_validate_client_id_empty(self):
        res = self.validator.get_input_validation(r'{"client_id":""}')
        self.assertEqual(PayloadValidator.CLIENT_ID_IS_EMPTY, res)

    def test_validate_input_is_valid(self):
        res = self.validator.get_input_validation(r'{"client_id":"ada"}')
        self.assertEqual(PayloadValidator.INPUT_IS_VALID, res)

    def test_validate_input_is_valid_additional_data_as_string(self):
        res = self.validator.get_input_validation(r'{"client_id":"ada", "anything":"anything"}')
        self.assertEqual(PayloadValidator.INPUT_IS_VALID, res)

    def test_validate_input_is_valid_additional_data_as_array(self):
        res = self.validator.get_input_validation(r'{"client_id":"ada", "anything":[]}')
        self.assertEqual(PayloadValidator.INPUT_IS_VALID, res)

    def test_validate_input_is_valid_additional_data_as_json(self):
        res = self.validator.get_input_validation(r'{"client_id":"ada", "anything":{}}')
        self.assertEqual(PayloadValidator.INPUT_IS_VALID, res)



class ChannelTests(unittest.TestCase):

    def setUp(self):
        self.channel = Channel()

    def test_update_with_string_not_json(self):
        res = self.channel.update(r'-', 0.0)
        self.assertEqual(r'{"error":"invalid input (-)"}', res)

    def test_update_with_json_not_containing_client_id(self):
        res = self.channel.update(r'{"not_client_id":"ada"}', 0.0)
        self.assertEqual(r'{"error":"invalid input ({"not_client_id":"ada"})"}', res)

    def test_update_with_minimum_data(self):
        res = self.channel.update(r'{"client_id":"ada"}', 0.0)
        self.assertEqual(r'[]', res)

    def test_update_with_additional_data(self):
        # FIXME
        #res = self.channel.update("{\"c\":\"ada\", \"a\":\"\", \"b\":[], \"c\":{}}", 0.0)
        res = self.channel.update(r'{"client_id":"ada", "a":"", "b":[]}', 0.0)
        self.assertEqual(r'[]', res)

    def test_two_updates_from_different_clients(self):
        # first client
        self.channel.update(r'{"client_id":"ada"}', 0.0)
        # second client receives data from first client
        res = self.channel.update(r'{"client_id":"joe"}', 0.0)
        self.assertEqual(r'[{"client_id":"ada"}]', res)

    def test_get_all_on_empty_channel(self):
        res = self.channel.get_all()
        self.assertEqual(r'[]', res)

    def test_get_all_on_not_empty_channel(self):
        self.channel.update(r'{"client_id":"ada"}', 0.0) # first client
        self.channel.update(r'{"client_id":"joe"}', 0.0) # second client
        res = self.channel.get_all() # observer
        self.assertEqual(r'[{"client_id":"ada"},{"client_id":"joe"}]', res)

    def test_remove_disconnected_client(self):
        # add clients in the channel
        self.channel.update(r'{"client_id":"ada"}', 0.0)
        self.channel.update(r'{"client_id":"joe"}', 1.0)
        # remove disconnected clients
        timeout = 5
        current_time = 10
        res = self.channel.remove_disconnected_clients(current_time, timeout)
        self.assertEqual(True, res) # True = some client(s) were disconnected
        # check channel is empty
        res = self.channel.get_all()
        self.assertEqual(r'[]', res)
        # try removing disconnected clients again
        current_time = 11
        res = self.channel.remove_disconnected_clients(current_time, timeout)
        self.assertEqual(False, res) # False = no client were disconnected


class ChannelsTests(unittest.TestCase):

    def setUp(self):
        self.channels = Channels()

    def test_channels_update_with_minimum_data(self):
        res = self.channels.update("test", r'{"client_id":"ada"}', 0.0)
        self.assertEqual(r'[]', res)

    def test_channels_update_with_two_clients(self):
        self.channels.update("test", r'{"client_id":"ada"}', 0.0)
        res = self.channels.update("test", r'{"client_id":"joe"}', 0.0)
        self.assertEqual(r'[{"client_id":"ada"}]', res)

    def test_channels_get_all_from(self):
        self.channels.update("test", r'{"client_id":"ada"}', 0.0)
        self.channels.update("test", r'{"client_id":"joe"}', 0.0)
        res = self.channels.get_all_from("test")
        self.assertEqual(r'[{"client_id":"ada"},{"client_id":"joe"}]', res)

    def test_channels_get_all_from_non_existing_channel(self):
        res = self.channels.get_all_from("toto")
        self.assertEqual(r'[]', res)

    def test_channels_remove_disconnected_clients(self):
        self.channels.update("test", r'{"client_id":"ada"}', 0.0)
        self.assertFalse(self.channels.channels["test"].is_empty())
        self.assertFalse(self.channels.remove_disconnected_clients(4.0, 5.0)) # before timeout
        self.assertTrue(self.channels.remove_disconnected_clients(10.0, 5.0)) # after timeout
        self.assertTrue(self.channels.channels["test"].is_empty())

    def test_channels_remove_empty_channels(self):
        self.channels.update("test", r'{"client_id":"ada"}', 0.0)
        self.channels.remove_empty_channels()
        self.assertEqual(1, len(self.channels.channels)) # channel not empty, still exists
        self.assertTrue(self.channels.remove_disconnected_clients(10.0, 5.0))
        self.assertEqual(1, len(self.channels.channels)) 
        self.channels.remove_empty_channels()
        self.assertEqual(0, len(self.channels.channels)) # channel empty, do not exists

if __name__ == '__main__':
    unittest.main()