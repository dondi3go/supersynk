import json

# Node class :
# - host_key is unique among hosts
# - node_key is unique among nodes belonging to same host
#   nodes belonging to different hosts can have same node_key
# - node_val is a string
class Node():
    def __init__(self, host_key:str, node_key:str, node_val:str):
        self.host_key = host_key
        self.node_key = node_key
        self.node_val = node_val

# A collection of Node objects
class Nodes:
    def __init__(self):
        self.nodes = []

     # Warning : no check on unicity, data model could be corrupted
    def _create(self, host_key:str, node_key:str, node_val:str) -> Node:
        node = Node(host_key, node_key, node_val)
        self.nodes.append(node)
        return node

    # Warning : no check on presence of node in collection
    def _remove(self, node:Node):
        self.nodes.remove(node)

    # Warning : no check on presence of node in collection
    def _update(self, node:Node, node_val:str):
        node.node_val = node_val

    # Get a Node from (host_key, node_key), return None if not found (tests)
    def get(self, host_key:str, node_key:str) -> Node:
        for node in self.nodes: # perf warning : iterate on all nodes
            if node.host_key == host_key and node.node_key == node_key:
                return node
        return None

    # Return the number of nodes in the collection (tests)
    def count(self) -> int:
        return len(self.nodes)

    # The only method to call on production
    def batch_update(self, host_key:str, node_keys:[], node_vals:[]) -> []:
        extractA = {} # (node_key > Node) dictionary for nodes belonging to host_key
        extractB = [] # nodes NOT belonging to host_key
        
        # Split nodes in two groups
        for node in self.nodes: # perf warning : iterate on all nodes
            if node.host_key == host_key:
                extractA[node.node_key] = node
            else:
                extractB.append(node)

        # Create or Update nodes
        for i in range(0, len(node_keys)):
            node_key = node_keys[i]
            node_val = node_vals[i]
            if not node_key in extractA:
                # Create
                self._create(host_key, node_key, node_val)
            else:
                # Update
                self._update(extractA[node_key], node_val)
                extractA.pop(node_key) # remove from dictionary

        # Remove nodes not updated during this update
        for node in extractA.values():
            # Remove
            self._remove(node) 

        # Return all other nodes as a list of strings
        result = []
        for node in extractB:
            result.append(node.host_key)
            result.append(node.node_key)
            result.append(node.node_val)
        return result

    # Remove all nodes belonging to one specific host
    def batch_remove(self, host_key:str):
        extractA = [] # nodes belonging to host_key
        
        # Get nodes belonging to host_key 
        for node in self.nodes: # perf warning : iterate on all items
            if node.host_key == host_key:
                extractA.append(node)
        
        # Remove them
        for node in extractA:
            self.nodes.remove(node)

    # Get all nodes
    def get_all(self):
        result = []
        for node in self.nodes:
            result.append(node.host_key)
            result.append(node.node_key)
            result.append(node.node_val)
        return result

# Channel class :
# A Channel contains data shared by several hosts (nodes)
# A host updates one channel with its own nodes states, 
# and gets in return the state of all the nodes in the channel
class Channel:
    def __init__(self):
        self.nodes = Nodes()
        self.host_last_update = {} # host_key:str > time:float

    INPUT_IS_VALID = 0
    INPUT_IS_NONE = 1
    INPUT_IS_EMPTY_STRING = 2
    INPUT_IS_NOT_JSON = 3
    HOST_KEY_IS_NOT_FOUND = 4
    HOST_KEY_IS_NOT_STR = 5
    HOST_KEY_IS_EMPTY = 6
    NODES_IS_NOT_FOUND = 7
    NODES_IS_NOT_LIST = 8

    # Check s is a valid JSON string containing some special nodes
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

        # Check dictionary contains 'host_key'
        if not "host_key" in d:
            return Channel.HOST_KEY_IS_NOT_FOUND

        host_key = d["host_key"]

        # Check 'host_key' value is a string
        if not type(host_key) is str:
            return Channel.HOST_KEY_IS_NOT_STR

        # Check 'host_key' value is not empty
        if len(host_key) == 0:
             return Channel.HOST_KEY_IS_EMPTY

        # Check dictionary contains 'nodes'
        if not "nodes" in d:
            return Channel.NODES_IS_NOT_FOUND

        nodes = d["nodes"]

        # Check 'nodes' value is a list
        if not type(nodes) is list:
            return Channel.NODES_IS_NOT_LIST

        return Channel.INPUT_IS_VALID

    # Update a channel with a JSON string, call 'get_input_validation()' before
    # Take a json string as input
    # Get a json string as output (all nodes except these belonging to host)
    def update(self, json_string:str, time:float) -> str:

        # Convert input
        try:
            d = json.loads(json_string) # d is a dictionary
            host_key = d["host_key"]
            node_keys = []
            node_vals = []

            nodes = d["nodes"]
            for node in nodes:
                node_keys.append(node["node_key"])
                node_vals.append(node["node_val"])
        except:
            return "[]"

        # Update
        strings = self.nodes.batch_update(host_key, node_keys, node_vals)

        # Store the update time of host_key
        self.host_last_update[host_key] = time

        # Convert to output (warning : code duplication)
        result = "["
        output_node_count = len(strings) // 3
        for i in range(0, output_node_count):
            host_key = strings[3*i]
            node_key = strings[3*i+1]
            node_val = strings[3*i+2]
            result += "{"
            result += "\"host_key\":\"" + host_key + "\", "
            result += "\"node_key\":\"" + node_key + "\", "
            result += "\"node_val\":\"" + node_val + "\""
            result += "}"
            if(i<output_node_count-1):
                result += ","
        result += "]"
        return result

    # Get a json string with all nodes of all hosts
    def get_all(self) -> str:
        # Update
        strings = self.nodes.get_all()

        # Convert to output (warning : code duplication)
        result = "["
        output_node_count = len(strings) // 3
        for i in range(0, output_node_count):
            host_key = strings[3*i]
            node_key = strings[3*i+1]
            node_val = strings[3*i+2]
            result += "{"
            result += "\"host_key\":\"" + host_key + "\", "
            result += "\"node_key\":\"" + node_key + "\", "
            result += "\"node_val\":\"" + node_val + "\""
            result += "}"
            if(i<output_node_count-1):
                result += ","
        result += "]"
        return result

    # Remove nodes whose last update is older than timeout
    def remove_disconnected_hosts(self, time:float, timeout:float) -> bool :
        removed_host_keys = []
        for host_key, last_update in self.host_last_update.items():
            if time - last_update > timeout:
                self.nodes.batch_remove(host_key)
                removed_host_keys.append(host_key)
        for host_key in removed_host_keys:
            self.host_last_update.pop(host_key, None)
        return len(removed_host_keys) > 0

# Channels class :
# Each channel is identified by a key
class Channels:
    def __init__(self):
        self.channels = {} # channel_key > channel
    
    # Update one channel (identified by channel_key) with a json_string
    # And get a json_string as a response
    def update(self, channel_key:str, json_string:str, time:float) -> str:

        if not channel_key in self.channels:
            # Create new Channel
            self.channels[channel_key] = Channel()

        # Update channel
        return self.channels[channel_key].update(json_string, time)

    # Get the 'channel_key' of each active channel
    def get_all_channel_keys(self):
        # TODO
        pass

    # Get all nodes in one channel
    def get_all_nodes(self, channel_key:str):
        if not channel_key in self.channels:
            return "[]"
        
        return self.channels[channel_key].get_all()

    # Clean up all active channels (remove disconnected users)
    # Close empty channels
    def clean_up(self, timeout:float):
        # TODO
        pass

if __name__ == '__main__':
    print("supersynk 0.0.1 alpha")
    print("run 'python supersynk_tests.py' to run the tests")
    print("run 'python supersynk_server.py' to run the server")
