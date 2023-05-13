from flask import Flask

app = Flask(__name__)

from routes.ping import ping
from routes.composite_clips import composite_clips
from routes.upload_files import upload_files, upload_file
from routes.songs import get_song, get_parts

app.add_url_rule('/upload_files', view_func=upload_files, methods=['POST'])
app.add_url_rule('/upload_file', view_func=upload_files, methods=['POST'])
app.add_url_rule('/composite', view_func=composite_clips, methods=['GET'])
app.add_url_rule('/ping', view_func=ping, methods=['GET'])
app.add_url_rule('/songs/<string:song_id>', view_func=get_song, methods=['GET'])
app.add_url_rule('/songs/<string:song_id>/song_parts', view_func=get_parts, methods=['GET'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)