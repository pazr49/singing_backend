from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import find_peaks
import moviepy.editor as mp
import numpy as np

'''

if all the clip offsets are negative (they start before the backing track), then they all need to move by the time diff value

If any clips have a positive value, then the backing track nees to move by that time diff, 

all others need to move by the difference between the backing track and the most positive, minus its own diff with the backing track

'''

def align_clips(uploaded_clips, backing_track):
    # find the peaks in the audio for the backing track
    backing_track_peaks = find_peaks_audio(backing_track)
    print('backing track peaks are ', backing_track_peaks)

    # the forward clip is the clip that starts latest
    largest_offset = 0
    forward_clip = None

    # Find the offset for each video clip and update the UploadedClip object. The offset is the time difference
    # between each video clip and the backing track
    for i in range(len(uploaded_clips)):
        video_peaks = find_peaks_video(uploaded_clips[i].path)
        print(f'video peaks {i} are ', video_peaks)
        offset = find_offset_between_peaks(video_peaks, backing_track_peaks)
        print(f'offset for video {i} is {offset}')
        uploaded_clips[i].time_offset = offset

        if offset > largest_offset:
            largest_offset = offset
            forward_clip = uploaded_clips[i]

    backing_track = AudioFileClip(backing_track)

    # if forward_clip is not None, then the backing track starts latest and all other clips can be moved
    # forwards by their offset
    if forward_clip is None:
        print('backing track is forward')
        for i in range(len(uploaded_clips)):
            print(f'moving clip {i} forward by ', uploaded_clips[i].time_offset)
            uploaded_clips[i].video_clip = uploaded_clips[i].video_clip.set_start(abs(float(uploaded_clips[i].time_offset)))
            uploaded_clips[i].audio_clip = uploaded_clips[i].audio_clip.set_start(abs(float(uploaded_clips[i].time_offset)))

    # if forward_clip is not None, then we have to find the most forward clip then move all other clips and
    # the backing track forwards to that point
    else:
        print('forward clip is ', forward_clip.path)
        print('moving backing track forward by ', forward_clip.time_offset)
        backing_track = backing_track.set_start(abs(float(forward_clip.time_offset)))
        for i in range(len(uploaded_clips)):
            if uploaded_clips[i] is not forward_clip:
                print(f'moving clip {i} forward by ', forward_clip.time_offset - uploaded_clips[i].time_offset)
                uploaded_clips[i].video_clip = uploaded_clips[i].video_clip.set_start(abs(float(forward_clip.time_offset - uploaded_clips[i].time_offset)))
                uploaded_clips[i].audio_clip = uploaded_clips[i].audio_clip.set_start(abs(float(forward_clip.time_offset - uploaded_clips[i].time_offset)))
            else:
                uploaded_clips[i].video_clip = uploaded_clips[i].video_clip.set_start(0)

    aligned_clips = []
    # set the audio for each video clip to the auto-tuned audio
    for i in range(len(uploaded_clips)):
        clip = uploaded_clips[i].video_clip
        clip = clip.set_audio(uploaded_clips[i].audio_clip)
        aligned_clips.append(clip)

    # return the aligned clips and the backing track
    return aligned_clips, backing_track


def find_offset_between_peaks(video_peaks, backing_track_peaks):
    differences = []

    if len(backing_track_peaks) != len(video_peaks):
        difference = video_peaks[0] - backing_track_peaks[0]
        if difference > 1:
            pass
        differences.append(difference)

    # loop through the peaks and find the difference between them
    for num1, num2 in zip(video_peaks, backing_track_peaks):
        difference = num1 - num2
        differences.append(difference)

    average_offset = sum(differences) / len(differences)
    return average_offset


def find_peaks_audio(audio_file):
    # https://stackoverflow.com/questions/1713335/peak-finding-algorithm-for-python-scipy
    # Load the WAV file
    audio = AudioSegment.from_mp3(audio_file)
    audio = audio[:10000]  # Keep only the first 10 seconds (assuming 1 second = 1000 milliseconds)
    audio.export('./projects/tmp.wav', format='wav')
    sample_rate, audio_data = wavfile.read('./projects/tmp.wav')

    # Extract the audio channel (assuming mono audio)
    audio_channel = audio_data[:, 0] if audio_data.ndim > 1 else audio_data

    # Normalize the audio channel
    audio_channel = audio_channel / np.max(np.abs(audio_channel))

    peaks, _ = find_peaks(audio_channel, distance=sample_rate//4, prominence=0.1)
    # Calculate the times of the peaks
    times = peaks / sample_rate

    return times


def find_peaks_video(filename, threshold=0.5, prominence=0.5, distance=20000):
    # Load the video file
    video = mp.VideoFileClip(filename).subclip(0, 10)

    # Extract the audio from the video
    audio = video.audio.to_soundarray(fps=44100)

     # Convert audio to mono if it's stereo
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    # Normalize the audio data to the range [-1, 1]
    audio = audio / np.max(np.abs(audio))

    # Find the peaks in the audio data
    peaks, _ = find_peaks(audio, height=threshold, prominence=prominence, distance=distance)

    # Convert peak indices to times
    peak_times = peaks / 44100
    return peak_times