from yta_multimedia.video.generation.rrss.discord.classes.discord_conversation_message import DiscordConversationMessage
from moviepy.editor import concatenate_videoclips
from typing import Union

class DiscordConversationVideoGenerator:
    def __init__(self):
        pass

    def generate_clip(self, messages: list[DiscordConversationMessage], output_filename: Union[str, None] = None):
        """
        Generates a video clip with the provided messages. This method
        will return the clip and also write it locally if 'output_filename'
        is provided.
        """
        if not messages:
            raise Exception('No "messages" provided.')
        
        clips = []
        for message in messages:
            clips.append(message.generate_clip())

        # TODO: Force 60 fps

        clip = concatenate_videoclips(clips).set_fps(60)

        if output_filename:
            clip.write_videofile(output_filename)

        return clip