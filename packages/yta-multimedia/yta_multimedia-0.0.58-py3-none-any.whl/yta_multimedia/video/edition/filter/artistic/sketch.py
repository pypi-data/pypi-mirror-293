from yta_general_utils.type_checker import variable_is_type
from yta_general_utils.file_processor import file_is_video_file
from yta_multimedia.video.frames import get_all_frames_from_video
from yta_multimedia.image.edition.filter.sketch import image_to_sketch, image_to_line_sketch
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ImageSequenceClip
from typing import Union

def video_to_sketch_video(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], output_filename: Union[str, None]):
    # TODO: Document it
    return __video_to_frame_by_frame_filtered_video(video, image_to_sketch, output_filename)

def video_to_line_sketch_video(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], output_filename: Union[str, None]):
    # TODO: Document it
    return __video_to_frame_by_frame_filtered_video(video, image_to_line_sketch, output_filename)

def __video_to_frame_by_frame_filtered_video(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], filter_func: function, output_filename: Union[str, None] = None):
    """
    Internal function to be used by any of our video editing methods
    that actually use image filter frame by frame. They do the same
    by only changing the filter we apply.
    """
    # TODO: Check if 'filter_func' is a function

    if not video:
        raise Exception('No "video" provided.')
    
    if variable_is_type(video, str):
        if not file_is_video_file(video):
            return None
        
        video = VideoFileClip(video)

    original_frames = get_all_frames_from_video(video)
    sketched_frames = []
    for original_frame in original_frames:
        sketched_frames.append(filter_func(original_frame))

    sketched_video = ImageSequenceClip(sketched_frames).set_audio(video.audio)

    if output_filename:
        sketched_video.write_videofile(output_filename, fps = video.fps)

    return sketched_video

