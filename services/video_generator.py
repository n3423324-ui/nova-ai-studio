import os
import uuid

from moviepy import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)


def create_video(
    images,
    voice
):

    os.makedirs(
        "media/videos",
        exist_ok=True
    )


    audio = AudioFileClip(
        voice
    )


    image_duration = (
        audio.duration / len(images)
    )


    clips = []


    for image in images:

        image_path = image[
            "image_path"
        ]


        clip = (
            ImageClip(image_path)
            .with_duration(image_duration)
        )


        clips.append(
            clip
        )


    video = concatenate_videoclips(
        clips,
        method="compose"
    )


    video = video.with_audio(
        audio
    )


    filename = (
        f"media/videos/"
        f"{uuid.uuid4().hex}.mp4"
    )


    video.write_videofile(
        filename,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )


    audio.close()


    for clip in clips:

        clip.close()


    video.close()


    return filename            file,
            ensure_ascii=False,
            indent=4
        )


    return filename            data,
            f,
            ensure_ascii=False,
            indent=4
        )


    return video_file
