from flask import Flask
from supersynk import Channels, get_current_time

app = Flask(__name__)
channels = Channels()

#
#
#
@app.route('/api/channels', methods=["GET"])
def get_channel_names():
    return "[toto, titi, tata]", 200

#
#
#
@app.route('/api/channels/<channel_id>', methods=["GET"])
def get_one_channel(channel_id):
    body = channels.get_all_nodes(channel_id)
    return body, 200

#
#
#
@app.route('/api/channels/<channel_id>', methods=["POST"])
def update_one_channel(channel_id):
    current_time = get_current_time()
    body = channels.update(channel_id, request.body, current_time)
    return body, 200

#
#
#
if __name__ == '__main__':
    app.run(port=9999)