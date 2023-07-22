import json
import time
import threading

# Channel class :
# A Channel contains data shared by several clients
# A client updates one channel with its own data, 
# and gets in return the state of all the data in the channel
class Channel:
    def __init__(self):
        self.clients = {}
        self.clients_last_update = {} # client_id:str > time:float
        self.lock = threading.Lock()

    INPUT_IS_VALID = 0
    INPUT_IS_NONE = 1
    INPUT_IS_EMPTY_STRING = 2
    INPUT_IS_NOT_JSON = 3
    CLIENT_ID_IS_NOT_FOUND = 4
    CLIENT_ID_IS_NOT_STR = 5
    CLIENT_ID_IS_EMPTY = 6

    # Check s is a valid JSON string containing some special property
    def get_input_validation(self, json_string:str) -> int :

        # Check is not None
        if json_string is None:
            return Channel.INPUT_IS_NONE

        # Check is not an empty string
        if json_string == "":
            return Channel.INPUT_IS_EMPTY_STRING

        # Check is json
        try:
            d = json.loads(json_string) # d is a dictionary
        except:
            return Channel.INPUT_IS_NOT_JSON

        # Check dictionary contains 'c' (client_id)
        if not "c" in d:
            return Channel.CLIENT_ID_IS_NOT_FOUND

        client_id = d["c"]

        # Check 'c' value is a string
        if not type(client_id) is str:
            return Channel.CLIENT_ID_IS_NOT_STR

        # Check 'c' value is not empty
        if len(client_id) == 0:
             return Channel.CLIENT_ID_IS_EMPTY

        return Channel.INPUT_IS_VALID

    # Update a channel with a JSON string, call 'get_input_validation()' before
    # Take a json string as input
    # Get a json string as output (all data except these belonging to client)
    def update(self, json_string:str, current_time:float) -> str:
        # Convert input
        try:
            d = json.loads(json_string) # d is a dictionary
        except:
            return "{\"error\":\"request payload (" + json_string + ") is not json\"}"
        
        try:
            client_id = d["c"]
        except:
            return "{\"error\":\"json does not contain 'c' property\"}"

        # ----------------------------------
        # Store the json string of client_id
        self.clients[client_id] = json_string

        # Store the update time of client_id
        self.clients_last_update[client_id] = current_time

        # Get all other json strings
        json_strings = []
        for k in self.clients.keys():
            if not k == client_id:
                json_strings.append(self.clients[k])
        # ----------------------------------

        result = "["
        count = len(json_strings)
        for i in range(0, count):
            result += json_strings[i]
            if i<count-1:
                result += ","
        result += "]"

        return result

    # Get a json string containing all data from all clients
    def get_all(self) -> str:
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

    # Remove clients whose last update is older than timeout
    def remove_disconnected_clients(self, time:float, timeout:float) -> bool :
        disconnexion_occured = False
        client_ids = list(self.clients_last_update.keys())
        for client_id in client_ids:
            last_update = self.clients_last_update[client_id]
            if time - last_update > timeout:
                # ------------------------------------------------------------
                with self.lock :
                    self.clients.pop(client_id, None)
                    self.clients_last_update.pop(client_id, None)
                # ------------------------------------------------------------
                disconnexion_occured = True
        return disconnexion_occured

# Channels class :
# Each channel is identified by an id
class Channels:
    def __init__(self):
        self.channels = {} # channel_id > channel

    # Update one channel (identified by channel_id) with a json_string
    # And get a json_string as a response
    def update(self, channel_id:str, json_string:str, current_time:float) -> str:

        if not channel_id in self.channels:
            # Create new Channel
            self.channels[channel_id] = Channel()

        # Update channel
        return self.channels[channel_id].update(json_string, current_time)

    # Get the 'channel_id' of each active channel
    def get_all_channel_ids(self):
        channel_ids = list(self.channels.keys())
        count = len(channel_ids)
        result = "["
        for i, channel_id in enumerate(channel_ids):
            result += "\"" + channel_id + "\""
            if i<count-1:
                result += ","
        result += "]"
        return result

    # Get all data from one channel
    def get_all_from(self, channel_id:str):
        if not channel_id in self.channels:
            return "[]"
        return self.channels[channel_id].get_all()

    #
    def remove_disconnected_clients(self, time:float, timeout:float):
        for channel_id in self.channels.keys():
            self.channels[channel_id].remove_disconnected_clients()

    #
    def remove_empty_channels(self):
        pass


# Get time as the number of seconds elapsed since the script started
starting_time = time.time()
def get_current_time():
    return time.time() - starting_time


if __name__ == '__main__':
    print("supersynk 0.0.1 alpha")
    print("run 'python supersynk_tests.py' to run the tests")
    print("run 'python supersynk_server.py' to run the server")
