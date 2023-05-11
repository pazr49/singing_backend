from audio_offset_finder.audio_offset_finder import find_offset_between_files
from moviepy.editor import *
from flask import Flask, request

app = Flask(__name__)

def find_offset(path1, path2):
    offset = find_offset_between_files(path1, path2, trim=30)
    return offset


@app.route('/', methods=['GET'])
def hello():
    return 'Hello, world!'


@app.route('/upload', methods=['POST'])
def upload():
    # Check if the 'file' key is present in the request files
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    # Check if a file was selected
    if file.filename == '':
        return 'No file selected', 400

    # Save the uploaded file
    file.save('uploaded_video.mp4')
    return 'File uploaded successfully'

@app.route('/upload_files', methods=['POST'])
def upload_files():
    # Check if the 'file' key is present in the request files
    if 'file' not in request.files:
        return 'No file uploaded', 400

    files = request.files.getlist('file')  # Get a list of uploaded files

    # Check if any file was selected
    if len(files) == 0:
        return 'No file selected', 400

    for file in files:
        # Save each uploaded file
        file.save('uploaded_video_{}.mp4'.format(files.index(file)))

    composite_clips('uploaded_video_0.mp4', 'uploaded_video_1.mp4')

    return 'Files uploaded successfully'


@app.route('/composite', methods=['GET'])
def composite_clips(path1, path2):

    offset = find_offset(path1, path2)
    print('Time offset is: ' + str(offset['time_offset']))
    print('Standard score is: ' + str(offset['standard_score']))

    time_diff = offset['time_offset']

    if time_diff > 0:
        clip1 = VideoFileClip(path1)
        clip2 = VideoFileClip(path2)
        clip2 = clip2.set_start(abs((float(time_diff))))
    else:
        clip1 = VideoFileClip(path1)
        clip2 = VideoFileClip(path2)
        clip1 = clip1.set_start(abs((float(time_diff))))

    video = clips_array([[clip1, clip2]])
    video.write_videofile("final_output.mp4", fps=24, audio_codec="aac")
    return 'Clips successfully composited'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Specify the desired port here
    #composite_clips('uploaded_video_0.mp4', 'uploaded_video_1.mp4')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
