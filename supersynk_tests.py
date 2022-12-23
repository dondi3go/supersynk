from supersynk import *
import time

# Home made test framework (because punk)
def assert_eq(a, b):
    print(" ok" if a == b else " KO : " + str(a) + " != " + str(b))

# Tests for class Nodes
def run_nodes_tests():
    print("\nTESTS for class Nodes")

    print("TEST 1 : create collection of nodes")
    nodes = Nodes()
    assert_eq(0, nodes.count())

    print("TEST 2 : create a new node")
    nodes._create("ada", "head", "a")
    assert_eq(1, nodes.count())
    hn = nodes.get("ada", "head")
    assert_eq(hn.node_val, "a")

    print("TEST 3 : remove a given node")
    nodes._remove(hn)
    assert_eq(0, nodes.count())

    print("TEST 4 : update with no data")
    nodes.batch_update("pia", [], [])
    assert_eq(0, nodes.count())

    print("TEST 5 : update with data - create")
    nodes.batch_update("pia", ["lhand", "rhand"], ["c", "d"])
    assert_eq(2, nodes.count())
    hn = nodes.get("pia", "lhand")
    assert_eq(hn.node_val, "c")

    print("TEST 6 : update with data - update")
    nodes.batch_update("pia", ["lhand", "rhand"], ["g", "h"])
    assert_eq(2, nodes.count())
    hn = nodes.get("pia", "lhand")
    assert_eq(hn.node_val, "g")

    print("TEST 7 : update with data - remove")
    nodes.batch_update("pia", ["lhand"], ["i"])
    assert_eq(1, nodes.count())
    hn = nodes.get("pia", "lhand")
    assert_eq(hn.node_val, "i")

    print("TEST 8 : batch remove")
    assert_eq(1, nodes.count())
    nodes.batch_update("jon", ["lhand", "rhand"], ["k", "l"])
    assert_eq(3, nodes.count())
    nodes.batch_remove("jon")
    assert_eq(1, nodes.count())

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
    assert_eq(Channel.HOST_KEY_IS_NOT_FOUND, channel.get_input_validation("{\"a\":\"b\"}"))

    print("TEST 1e : validate wrong host_key value")
    assert_eq(Channel.HOST_KEY_IS_NOT_STR, channel.get_input_validation("{\"host_key\":0, \"nodes\":[]}"))

    print("TEST 1f : validate wrong host_key value")
    assert_eq(Channel.HOST_KEY_IS_EMPTY, channel.get_input_validation("{\"host_key\":\"\", \"nodes\":[]}"))

    print("TEST 1g : validate no 'nodes' key")
    assert_eq(Channel.NODES_IS_NOT_FOUND, channel.get_input_validation("{\"host_key\":\"ada\"}"))

    print("TEST 1h : validate wrong nodes value")
    assert_eq(Channel.NODES_IS_NOT_LIST, channel.get_input_validation("{\"host_key\":\"ada\", \"nodes\":\"\"}"))

    print("TEST 1i : validate minimum data")
    assert_eq(Channel.INPUT_IS_VALID, channel.get_input_validation("{\"host_key\":\"ada\", \"nodes\":[]}"))

    # UPDATE

    print("TEST 2 : update with minimum data")
    res = channel.update("{\"host_key\":\"ada\", \"nodes\":[]}", 0.0)
    assert_eq("[]", res)

    print("TEST 3 : update with one node (ada)")
    res = channel.update("{\"host_key\":\"ada\", \"nodes\":[{\"node_key\":\"rhand\", \"node_val\":\"a\"}]}", 0.0)
    assert_eq("[]", res)

    print("TEST 4 : update with another node (joe) and get ada")
    res = channel.update("{\"host_key\":\"joe\", \"nodes\":[{\"node_key\":\"rhand\", \"node_val\":\"b\"}]}", 0.0)
    assert_eq("[{\"host_key\":\"ada\", \"node_key\":\"rhand\", \"node_val\":\"a\"}]", res)
    # check result is json

    print("TEST 5 : get all nodes")
    res = channel.get_all()
    expected_res = "[{\"host_key\":\"ada\", \"node_key\":\"rhand\", \"node_val\":\"a\"},{\"host_key\":\"joe\", \"node_key\":\"rhand\", \"node_val\":\"b\"}]"
    assert_eq(expected_res, res)
    # check result is json

    print("TEST 6 : disconnect everyone")
    res = channel.remove_disconnected_hosts(10.0, 1.0)
    assert_eq(True, res)
    res = channel.get_all()
    assert_eq("[]", res)
    res = channel.remove_disconnected_hosts(11.0, 1.0)
    assert_eq(False, res)

    print("TEST 7 : performances")
    node1 = "{\"node_key\":\"head\", \"node_val\":\"a\"}"
    node2 = "{\"node_key\":\"rhand\", \"node_val\":\"b\"}"
    node3 = "{\"node_key\":\"lhand\", \"node_val\":\"c\"}"
    body = "{\"host_key\":\"joe\", \"nodes\":[" + node1 + "," + node2 + "," + node3 + "]}"
    request_count = 10000
    start_time = time.time()
    for i in range(0, request_count):
        channel.get_input_validation(body)
        current_time = 0.01 * i
        channel.update(body, current_time)
        channel.remove_disconnected_hosts(current_time, 10.0)
    elapsed_time = time.time() - start_time
    update_per_sec = request_count / elapsed_time
    print(str(int(update_per_sec)) + " updates per sec")

# Tests for class Channels
def run_channels_tests():

    print("\nTESTS for class Channels")
    channels = Channels()

    print("TEST 1 : update with minimum data")
    res = channels.update("test", "{\"host_key\":\"ada\", \"nodes\":[]}", 0.0)
    assert_eq("[]", res)

    print("TEST 2 : update with other data")
    res = channels.update("test", "{\"host_key\":\"joe\", \"nodes\":[{\"node_key\":\"rhand\", \"node_val\":\"b\"}]}", 0.0)
    assert_eq("[]", res)

    print("TEST 3 : get all nodes from existing channel")
    res = channels.get_all_nodes("test")
    expected_res = "[{\"host_key\":\"joe\", \"node_key\":\"rhand\", \"node_val\":\"b\"}]"
    assert_eq(expected_res, res)

    print("TEST 4 : get all nodes from non-existing channel")
    res = channels.get_all_nodes("toto")
    expected_res = "[]"
    assert_eq(expected_res, res)


if __name__ == '__main__':
    # Tests
    run_nodes_tests()
    run_channel_tests()
    run_channels_tests()