from flask import Flask, request
from supersynk import Channels, get_current_time

app = Flask(__name__)
channels = Channels()

#
#
#
@app.route('/api', methods=["GET"])
def get_api_details():
    body = "supersynk server"
    return body, 200

#
#
#
@app.route('/api/channels', methods=["GET"])
def get_channel_ids():
    body = channels.get_all_channel_ids()
    return body, 200

#
#
#
@app.route('/api/channels/<channel_id>', methods=["GET"])
def get_one_channel(channel_id):
    body = channels.get_all_from(channel_id)
    return body, 200

#
#
#
@app.route('/api/channels/<channel_id>', methods=["POST"])
def update_one_channel(channel_id):
    request_body = request.data.decode('utf-8') # request.data is of type 'bytes'
    current_time = get_current_time()
    response_body = channels.update(channel_id, request_body, current_time)
    return response_body, 200

#
#
#
if __name__ == '__main__':
    app.run(port=9999)