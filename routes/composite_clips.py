from audio_offset_finder.audio_offset_finder import find_offset_between_files
from utils.generate_composite_video import generate_composite_video

def composite_clips():
    path1 = 'uploaded_video_0.mp4'
    path2 = 'uploaded_video_1.mp4'

    offset = find_offset_between_files(path1, path2, trim=30)
    time_diff = offset['time_offset']

    print('Time offset is:', time_diff)
    print('Standard score is:', offset['standard_score'])

    return generate_composite_video(path1, path2, time_diff)