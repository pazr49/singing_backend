from moviepy.editor import *

def generate_composite_video(backing_track, uploaded_clips, forward_clip):

    print('Back track is:', backing_track)
    print('Uploaded clips are:', uploaded_clips[0].path) #, uploaded_clips[1].path])
    print('Forward clip is:', forward_clip.time_offset)

    backing_track = AudioFileClip(backing_track)
    clips = []

    if forward_clip is None:
        print('No forward clip')
        for i in range(len(uploaded_clips)):
            clip = VideoFileClip(uploaded_clips[i].path)
            clip = clip.set_start(abs(float(uploaded_clips[i].time_offset)))
            clips.append(clip)
    else:
        backing_track = backing_track.set_start(abs(float(forward_clip.time_offset)))
        for i in range(len(uploaded_clips)):
            if uploaded_clips[i] is not forward_clip:
                print('Not the forward clip')
                clip = VideoFileClip(uploaded_clips[i].path)
                clip = clip.set_start(abs(float(uploaded_clips[i].time_offset - forward_clip.time_offset)))
                clips.append(clip)
            else:
                print('Forward clip')
                clip = VideoFileClip(uploaded_clips[i].path)
                clip = clip.set_start(0)
                clips.append(clip)


    for i in range(len(clips)):
        clips[i] = clips[i].set_audio(uploaded_clips[i].auto_tuned_audio_path)

    video = CompositeVideoClip(clips, size=(720, 460))
    video = video.set_audio(CompositeAudioClip([backing_track, video.audio]))
    video = video.subclip(10, 60)
    video.write_videofile("final_output.mp4", fps=24, audio_codec="aac")

    return 'Clips successfully composited'

'''

if all the clips are negative (they start before the backing track), then they all need to move by the time diff value
    
If any clips have a positive value, then the backing track nees to move by that time diff, 

all others need to move by the difference between the backing track and the most positive, minus its own diff with the backing track

'''