import time
from threading import Thread, main_thread
from flask import Flask, request
from supersynk import Channels, get_current_time


app = Flask(__name__)
channels = Channels()

#
#
#
@app.route('/api', methods=["GET"])
def get_api_details():
    """Details about the API
    """
    body = "supersynk server"
    return body, 200

#
#
#
@app.route('/api/channels', methods=["GET"])
def get_channel_ids():
    """Get the ids of all the channels
    """
    body = channels.get_all_channel_ids()
    return body, 200

#
#
#
@app.route('/api/channels/<channel_id>', methods=["GET"])
def get_one_channel(channel_id):
    """Get the data of all the clients of one channel
    """
    body = channels.get_all_from(channel_id)
    return body, 200

#
#
#
@app.route('/api/channels/<channel_id>', methods=["POST"])
def update_one_channel(channel_id):
    """Update one client in one channel, and get the data of all the other clients
    """
    request_body = request.data.decode('utf-8') # request.data is of type 'bytes'
    current_time = get_current_time()
    response_body = channels.update(channel_id, request_body, current_time)
    return response_body, 200

#
#
#
def run_disconnection_loop():
    """ Regularly tell channels to remove their disconnected clients
    """
    # time span without activity before disconnection from a channel (in seconds)
    timeout = 1
    # time span between two calls for disconnection (in seconds)
    sleep_span = 5
    # start disconnection loop
    while True:
        current_time = get_current_time()
        channels.remove_disconnected_clients(current_time, timeout)
        time.sleep(sleep_span)
        # without this, the loop prevents the server from stopping with Ctrl+C :
        if not main_thread().is_alive():
            break

#
#
#
if __name__ == '__main__':
    # run disconnection loop
    other_thread = Thread(target=run_disconnection_loop)
    other_thread.start()
    # run flask app (5000 is the default port for flask apps)
    app.run(host='0.0.0.0',port=5000)