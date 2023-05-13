from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip


def generate_composite_video(path1, path2, time_diff):
    clip1 = VideoFileClip(path1)
    clip2 = VideoFileClip(path2)

    if time_diff > 0:
        clip2 = clip2.set_start(abs(float(time_diff)))
    else:
        clip1 = clip1.set_start(abs(float(time_diff)))

    clip1 = clip1.resize((360, 460))
    clip2 = clip2.resize((360, 460)).set_position((360, 0))

    video = CompositeVideoClip([clip1, clip2], size=(720, 460))
    video.write_videofile("final_output.mp4", fps=24, audio_codec="aac")

    return 'Clips successfully composited'