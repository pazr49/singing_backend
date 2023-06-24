import librosa
from audio_offset_finder.audio_offset_finder import find_offset_between_files
from flask import Flask

app = Flask(__name__)

from routes.ping import ping
from routes.create_output_video import create_output_video, UploadedClip
from routes.upload_files import upload_files, upload_file
from routes.songs import get_song_by_id, get_parts, get_songs

app.add_url_rule('/upload_files', view_func=upload_files, methods=['POST'])
app.add_url_rule('/upload_file', view_func=upload_files, methods=['POST'])
app.add_url_rule('/composite', view_func=create_output_video, methods=['GET'])
app.add_url_rule('/ping', view_func=ping, methods=['GET'])
app.add_url_rule('/songs', view_func=get_songs, methods=['GET'])
app.add_url_rule('/songs/<string:song_id>', view_func=get_song_by_id, methods=['GET'])
app.add_url_rule('/songs/<string:song_id>/song_parts', view_func=get_parts, methods=['GET'])
app.add_url_rule('/create_output_video', view_func=create_output_video, methods=['POST'])


if __name__ == '__main__':
   with app.app_context():
      app.run(host='0.0.0.0', port=8000)
