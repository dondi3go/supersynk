import json
import time
import threading


class PayloadValidator:
    """Validate the payload of the requests made to the server.
    """
    def __init__(self):
        pass

    INPUT_IS_VALID = 0
    INPUT_IS_NONE = 1
    INPUT_IS_EMPTY_STRING = 2
    INPUT_IS_NOT_JSON = 3
    CLIENT_ID_IS_NOT_FOUND = 4
    CLIENT_ID_IS_NOT_STR = 5
    CLIENT_ID_IS_EMPTY = 6

    def get_input_validation(self, json_string:str) -> int :
        """Check json_string is a valid JSON string containing some special property
        """
        # Check is not None
        if json_string is None:
            return PayloadValidator.INPUT_IS_NONE

        # Check is not an empty string
        if json_string == "":
            return PayloadValidator.INPUT_IS_EMPTY_STRING

        # Check is json
        try:
            dic = json.loads(json_string) # dic is a dictionary
        except json.JSONDecodeError:
            return PayloadValidator.INPUT_IS_NOT_JSON

        # Check dictionary contains 'client_id'
        if not Channel.CLIENT_ID_PROPERTY_NAME in dic:
            return PayloadValidator.CLIENT_ID_IS_NOT_FOUND

        client_id = dic[Channel.CLIENT_ID_PROPERTY_NAME]

        # Check client_id value is a string
        if not isinstance(client_id, str):
            return PayloadValidator.CLIENT_ID_IS_NOT_STR

        # Check client_id value is not empty
        if len(client_id) == 0:
            return PayloadValidator.CLIENT_ID_IS_EMPTY

        return PayloadValidator.INPUT_IS_VALID


class Channel:
    """A Channel contains data provided by one or several clients.
    A client updates one channel with its own data,
    and gets in return the data of all the other clients of the channel.
    """
    def __init__(self):
        self.clients = {}
        self.clients_last_update = {} # client_id:str > time:float
        self.lock = threading.Lock()

    CLIENT_ID_PROPERTY_NAME = "client_id"

    def update(self, json_string:str, current_time:float) -> str:
        """Update a channel with a JSON string, call 'get_input_validation()' before
        Take a json string as input
        Get a json string as output (all data except these belonging to client)
        """

        # Assume validation has been performed before
        # but protect anyway
        try:
            dic = json.loads(json_string) # dic is a dictionary
            client_id = dic[Channel.CLIENT_ID_PROPERTY_NAME]
            assert len(client_id) > 0
        except (json.JSONDecodeError, KeyError, AssertionError):
            return r'{"error":"invalid input (' + json_string + r')"}'

        # ----------------------------------
        # Store the json string of client_id
        self.clients[client_id] = json_string

        # Store the update time of client_id
        self.clients_last_update[client_id] = current_time

        # Get all other json strings
        json_strings = []
        for (key, value) in self.clients.items():
            if not key == client_id:
                json_strings.append(value)
        # ----------------------------------

        result = "["
        count = len(json_strings)
        for i in range(0, count):
            result += json_strings[i]
            if i<count-1:
                result += ","
        result += "]"

        return result

    def get_all(self) -> str:
        """Get a json string containing data from all clients in the channel
        """
        json_strings = []
        # ----------------------------------
        with self.lock :
            json_strings = list(self.clients.values())
        # ----------------------------------
        result = "["
        count = len(json_strings)
        for i in range(0, count):
            result += json_strings[i]
            if i<count-1:
                result += ","
        result += "]"

        return result

    def remove_disconnected_clients(self, current_time:float, timeout:float) -> bool :
        """Remove clients whose last update is older than timeout
        """
        disconnection_occured = False
        client_ids = list(self.clients_last_update.keys())
        for client_id in client_ids:
            last_update = self.clients_last_update[client_id]
            if current_time - last_update > timeout:
                # ------------------------------------------------------------
                with self.lock :
                    self.clients.pop(client_id, None)
                    self.clients_last_update.pop(client_id, None)
                # ------------------------------------------------------------
                disconnection_occured = True
        return disconnection_occured
    
    def is_empty(self):
        """Return True if the channel has no clients
        """
        if len(self.clients) == 0:
            return True
        return False


class Channels:
    """Each channel is identified by an id, 
    and contains data provided by one or several clients

    The server directly uses this class, it does not have to use Channel.
    """
    def __init__(self):
        self.channels = {} # channel_id > channel

    def update(self, channel_id:str, json_string:str, current_time:float) -> str:
        """Update one channel (identified by channel_id) with a json_string
        And get a json_string as a response
        """
        if not channel_id in self.channels:
            # Create new Channel
            self.channels[channel_id] = Channel()

        # Update channel
        return self.channels[channel_id].update(json_string, current_time)

    def get_all_channel_ids(self):
        """Get the 'channel_id' of all active channel
        """
        channel_ids = list(self.channels.keys())
        count = len(channel_ids)
        result = "["
        for i, channel_id in enumerate(channel_ids):
            result += "\"" + channel_id + "\""
            if i<count-1:
                result += ","
        result += "]"
        return result

    def get_all_from(self, channel_id:str):
        """Get all data from one channel
        """
        if not channel_id in self.channels:
            return "[]"
        return self.channels[channel_id].get_all()

    def remove_disconnected_clients(self, current_time:float, timeout:float):
        """Remove clients whose latest update time is older than 'timeout'
        """
        disconnection_occured = False
        for channel in self.channels.values():
            if channel.remove_disconnected_clients(current_time, timeout):
                disconnection_occured = True
        return disconnection_occured

    def remove_empty_channels(self):
        """Remove channels containing no clients
        """
        empty_channel_ids = []
        for channel_id, channel in self.channels.items():
            if channel.is_empty():
                empty_channel_ids.append(channel_id)
        
        for channel_id in empty_channel_ids:
            self.channels.pop(channel_id, None)


starting_time = time.time()
def get_current_time():
    """Get time as the number of seconds elapsed since the script started
    """
    return time.time() - starting_time

# Headers expected in client requests
CLIENT_ID_KEY = 'Client-Id'
CLIENT_TIME_KEY = 'Client-Time'
SERVER_TIME_KEY = 'Server-Time'

# Stored values of client_time
clients_latest_request = {} # client_id:str > client_time:float
def is_late_request(headers):
    """Return True if headers contain 'Client-Id' and 'Client-Time' and
       Client-Time value is older than a previous stored value
    """
    if CLIENT_ID_KEY in headers and CLIENT_TIME_KEY in headers:
        client_id = headers[CLIENT_ID_KEY]
        client_time = float(headers[CLIENT_TIME_KEY])
        if not client_id in clients_latest_request:
           clients_latest_request[client_id] = 0 
        if clients_latest_request[client_id] > client_time :
            return True
        clients_latest_request[client_id] = client_time
    return False

def add_response_header(headers):
    """Add a header named 'Server-Time' with a value of current time (second)
    """
    headers[SERVER_TIME_KEY] = "{:.3f}".format(get_current_time())


if __name__ == '__main__':
    print("supersynk :")
    print("run 'python supersynk_tests.py' to run the tests")
    print("run 'python supersynk_server.py' to run the server")
