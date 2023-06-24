import librosa
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from routes.songs import get_song_by_id
from utils.auto_tune import auto_tune
from utils.audio_offset import *
from utils.normailise_audio import normalize_audio
from flask import request

class UploadedClip:
    def __init__(self, path, time_offset):
        self.path = path
        self.time_offset = time_offset
        self.audio_clip = None
        self.video_clip = None


def create_output_video():

    songID = request.form.get('song_id')
    projectID = request.form.get('project_id')
    partIDs = request.form.get('part_ids').split(',')

    key = get_song_by_id(songID).json['key']

    uploaded_clips= []
    for clipId in partIDs:
        uploaded_clips.append(UploadedClip(f'./song_files/{clipId}.mp4', 0))

    backing_track = f'./backing_tracks/{songID}.mp3'

    backing_audio, sr = librosa.load(backing_track, sr=None)
    backing_normalised = normalize_audio(backing_audio) * 0.5


    # create normalised auto-tuned files and set the file path in the UploadedClip objects
    print('Auto-tuning clips')
    for clip in uploaded_clips:
        auto_tuned_audio = auto_tune(backing_normalised, clip.path, key)
        clip.audio_clip = AudioFileClip(auto_tuned_audio)
        clip.video_clip = VideoFileClip(clip.path)

    # returns a list of aligned and auto-tuned clips and the backing track in mp.clip format
    print('Aligning clips with audio offset')
    aligned_clips, backing_track = align_clips(uploaded_clips, backing_track)

    # resize the clips and set their position in the final video
    print('Resizing and positioning clips')
    for i in range(len(aligned_clips)):
        width = 720 / len(aligned_clips)
        aligned_clips[i] = aligned_clips[i].resize((width, 460)).set_pos((i*width, 0))

    print('writing final video')
    video = CompositeVideoClip(aligned_clips, size=(720, 460))
    video = video.set_audio(CompositeAudioClip([backing_track, video.audio]))
    video = video.subclip(10, 60)
    video.write_videofile("final_outpssu2t.mp4", fps=24, audio_codec="aac")

    return 'Clips successfully composited'