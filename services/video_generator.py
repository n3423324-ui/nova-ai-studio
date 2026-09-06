   import os
import uuid

from moviepy import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)


def create_video(
    images,
    voices
):

    if not images:
        raise ValueError(
            "No images provided"
        )

    if not voices:
        raise ValueError(
            "No voice files provided"
        )

    os.makedirs(
        "media/videos",
        exist_ok=True
    )

    clips = []

    try:

        image_map = {}

        for image in images:

            scene_number = (
                image.get("scene")
            )

            image_map[
                scene_number
            ] = image

        for voice_data in voices:

            scene_number = (
                voice_data[
                    "scene_number"
                ]
            )

            voice_path = (
                voice_data[
                    "voice_path"
                ]
            )

            if scene_number not in image_map:

                continue

            image_path = (
                image_map[
                    scene_number
                ].get(
                    "image_path"
                )
            )

            if not image_path:

                raise ValueError(
                    f"Image missing for scene "
                    f"{scene_number}"
                )

            if not os.path.exists(
                image_path
            ):

                raise FileNotFoundError(
                    f"Image not found: "
                    f"{image_path}"
                )

            if not os.path.exists(
                voice_path
            ):

                raise FileNotFoundError(
                    f"Voice not found: "
                    f"{voice_path}"
                )

            audio = AudioFileClip(
                voice_path
            )

            duration = (
                audio.duration
            )

            clip = ImageClip(
                image_path
            ).with_duration(
                duration
            )

            clip = clip.with_audio(
                audio
            )

            clips.append(
                clip
            )

        if not clips:

            raise ValueError(
                "No video clips created"
            )

        final_video = (
            concatenate_videoclips(
                clips,
                method="compose"
            )
        )

        filename = (
            "media/videos/"
            f"{uuid.uuid4().hex}.mp4"
        )

        final_video.write_videofile(
            filename,
            codec="libx264",
            audio_codec="aac",
            fps=24
        )

        final_video.close()

        return filename

    finally:

        for clip in clips:

            try:

                clip.close()

            except Exception:

                pass
