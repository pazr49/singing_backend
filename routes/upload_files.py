from flask import request
from utils.save_files import save_files

def upload_files():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    files = request.files.getlist('file')

    return save_files(files)


def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    if file.filename == '':
        return 'No file selected', 400

    file.save('uploaded_video.mp4')
    return 'File uploaded successfully'
