from supersynk import *

# Home made test framework (because punk)
def assert_eq(a, b):
    print(" ok" if a == b else " KO : " + str(a) + " != " + str(b))

# Tests for class Channel
def run_channel_tests():

    print("\nTESTS for class Channel")
    channel = Channel()

    # INPUT VALIDATION

    print("TEST 1a : validate data is None")
    assert_eq(Channel.INPUT_IS_NONE, channel.get_input_validation(None))

    print("TEST 1b : validate no data")
    assert_eq(Channel.INPUT_IS_EMPTY_STRING, channel.get_input_validation(""))

    print("TEST 1c : validate wrong data")
    assert_eq(Channel.INPUT_IS_NOT_JSON, channel.get_input_validation("-"))

    print("TEST 1d : validate wrong data")
    assert_eq(Channel.CLIENT_ID_IS_NOT_FOUND, channel.get_input_validation("{\"a\":\"b\"}"))

    print("TEST 1e : validate wrong client id value")
    assert_eq(Channel.CLIENT_ID_IS_NOT_STR, channel.get_input_validation("{\"c\":0, \"n\":[]}"))

    print("TEST 1f : validate wrong client id value")
    assert_eq(Channel.CLIENT_ID_IS_EMPTY, channel.get_input_validation("{\"c\":\"\", \"n\":[]}"))

    print("TEST 1g : validate no 'nodes' key")
    assert_eq(Channel.NODES_IS_NOT_FOUND, channel.get_input_validation("{\"c\":\"ada\"}"))

    print("TEST 1h : validate wrong nodes value")
    assert_eq(Channel.NODES_IS_NOT_LIST, channel.get_input_validation("{\"c\":\"ada\", \"n\":\"\"}"))

    print("TEST 1i : validate minimum data")
    assert_eq(Channel.INPUT_IS_VALID, channel.get_input_validation("{\"c\":\"ada\", \"n\":[]}"))

    # UPDATE

    print("TEST 2 : update with minimum data")
    res = channel.update("{\"c\":\"ada\", \"n\":[]}", 0.0)
    assert_eq("[]", res)

    print("TEST 3 : update with one node (ada)")
    res = channel.update("{\"c\":\"ada\", \"n\":[{\"k\":\"rhand\", \"v\":\"a\"}]}", 0.0)
    assert_eq("[]", res)

    print("TEST 4 : update with another node (joe) and get ada")
    res = channel.update("{\"c\":\"joe\", \"n\":[{\"k\":\"rhand\", \"v\":\"b\"}]}", 0.0)
    assert_eq("[{\"c\":\"ada\", \"n\":[{\"k\":\"rhand\", \"v\":\"a\"}]}]", res)
    # check result is json

    print("TEST 5 : get all nodes")
    res = channel.get_all()
    expected_res = "[{\"c\":\"ada\", \"n\":[{\"k\":\"rhand\", \"v\":\"a\"}]},{\"c\":\"joe\", \"n\":[{\"k\":\"rhand\", \"v\":\"b\"}]}]"
    assert_eq(expected_res, res)
    # check result is json

    print("TEST 6 : disconnect everyone")
    res = channel.remove_disconnected_clients(10.0, 1.0)
    assert_eq(True, res)
    res = channel.get_all()
    assert_eq("[]", res)
    res = channel.remove_disconnected_clients(11.0, 1.0)
    assert_eq(False, res)

    print("TEST 7 : performances")
    node1 = "{\"k\":\"head\", \"v\":\"a\"}"
    node2 = "{\"k\":\"rhand\", \"v\":\"b\"}"
    node3 = "{\"k\":\"lhand\", \"v\":\"c\"}"
    json_str = "{\"c\":\"joe\", \"n\":[" + node1 + "," + node2 + "," + node3 + "]}"
    request_count = 10000
    start_time = time.time()
    for i in range(0, request_count):
        channel.get_input_validation(json_str)
        current_time = get_current_time()
        channel.update(json_str, current_time)
        channel.remove_disconnected_clients(current_time, 10.0)
    elapsed_time = time.time() - start_time
    update_per_sec = request_count / elapsed_time
    print(str(int(update_per_sec)) + " updates per sec")

# Tests for class Channels
def run_channels_tests():

    print("\nTESTS for class Channels")
    channels = Channels()

    print("TEST 1 : update with minimum data")
    res = channels.update("test", "{\"c\":\"ada\", \"n\":[]}", 0.0)
    assert_eq("[]", res)

    print("TEST 2 : update with other data")
    res = channels.update("test", "{\"c\":\"joe\", \"n\":[{\"k\":\"rhand\", \"v\":\"b\"}]}", 0.0)
    assert_eq("[]", res)

    print("TEST 3 : get all nodes from existing channel")
    res = channels.get_all_nodes("test")
    expected_res = "[{\"c\":\"joe\", \"n\":[{\"k\":\"rhand\", \"v\":\"b\"}]}]"
    assert_eq(expected_res, res)

    print("TEST 4 : get all nodes from non-existing channel")
    res = channels.get_all_nodes("toto")
    expected_res = "[]"
    assert_eq(expected_res, res)


if __name__ == '__main__':
    # Tests
    run_channel_tests()
    run_channels_tests()