import librosa
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from utils.auto_tune import auto_tune
from utils.audio_offset import *
from utils.normailise_audio import normalize_audio


class UploadedClip:
    def __init__(self, path, time_offset):
        self.path = path
        self.time_offset = time_offset
        self.auto_tuned_audio_path = None


def create_output_video():
    # load in the clips
    uploaded_videos = [UploadedClip('./uploaded_video_0.mp4', 0), UploadedClip('./uploaded_video_1.mp4', 0)]
    backing_track = './song_files/backing_track.mp3'

    backing_audio, sr = librosa.load(backing_track, sr=None)
    backing_normalised = normalize_audio(backing_audio) * 0.5


    # create normalised auto-tuned files and set the file path in the UploadedClip objects
    print('Auto-tuning clips')
    for video in uploaded_videos:
        video.auto_tuned_audio_path = auto_tune(backing_normalised, video.path, 'C:maj')

    # returns a list of aligned and auto-tuned clips and the backing track in mp.clip format
    print('Aligning clips with audio offset')
    aligned_clips, backing_track = align_clips(uploaded_videos, backing_track)

    for i in range(len(aligned_clips)):
        aligned_clips[i] = aligned_clips[i].resize((360, 460)).set_pos((i*360, 0))

    video = CompositeVideoClip(aligned_clips, size=(720, 460))
    video = video.set_audio(CompositeAudioClip([backing_track, video.audio]))
    video = video.subclip(10, 60)
    video.write_videofile("final_output.mp4", fps=24, audio_codec="aac")

    return 'Clips successfully composited'