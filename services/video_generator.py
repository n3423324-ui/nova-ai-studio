import os
import uuid

from moviepy import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)


def create_video(images, voice):

    if not images:
        raise ValueError(
            "No images provided for video creation"
        )

    if not voice:
        raise ValueError(
            "No voice file provided"
        )

    if not os.path.exists(voice):
        raise FileNotFoundError(
            f"Voice file not found: {voice}"
        )

    os.makedirs(
        "media/videos",
        exist_ok=True
    )

    clips = []
    audio = None
    video = None

    try:

        # Load audio
        audio = AudioFileClip(
            voice
        )

        # Calculate duration for each image
        image_duration = (
            audio.duration / len(images)
        )

        # Create video clips from images
        for image in images:

            image_path = image.get(
                "image_path"
            )

            if not image_path:
                raise ValueError(
                    "image_path is missing from image data"
                )

            if not os.path.exists(image_path):
                raise FileNotFoundError(
                    f"Image file not found: {image_path}"
                )

            clip = (
                ImageClip(
                    image_path
                )
                .with_duration(
                    image_duration
                )
            )

            clips.append(
                clip
            )

        # Combine image clips
        video = concatenate_videoclips(
            clips,
            method="compose"
        )

        # Add audio
        video = video.with_audio(
            audio
        )

        # Create unique filename
        filename = (
            "media/videos/"
            f"{uuid.uuid4().hex}.mp4"
        )

        # Export video
        video.write_videofile(
            filename,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            logger=None
        )

        return filename

    finally:

        # Close all image clips
        for clip in clips:
            try:
                clip.close()
            except Exception:
                pass

        # Close final video
        if video is not None:
            try:
                video.close()
            except Exception:
                pass

        # Close audio
        if audio is not None:
            try:
                audio.close()
            except Exception:
                pass
