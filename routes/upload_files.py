import time

from flask import request


def upload_files():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    files = request.files.getlist('file')

    if len(files) == 0:
        return 'No file selected', 400

    for index, file in enumerate(files):
        file.save(f'./song_files/uploaded_video_{index}.mp4')

    return 'Files uploaded successfully'


def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    if file.filename == '':
        return 'No file selected', 400

    file.save('uploaded_video.mp4')
    return 'File uploaded successfully'


