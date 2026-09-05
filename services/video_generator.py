import os
import uuid

from moviepy import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)


def create_video(images, voice):

    if not images:
        raise ValueError("No images provided for video creation")

    if not voice:
        raise ValueError("No voice file provided")

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

        # تحميل الصوت
        audio = AudioFileClip(voice)

        # مدة كل صورة
        image_duration = (
            audio.duration / len(images)
        )

        # إنشاء المقاطع من الصور
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
                ImageClip(image_path)
                .with_duration(image_duration)
            )

            clips.append(clip)

        # دمج الصور
        video = concatenate_videoclips(
            clips,
            method="compose"
        )

        # إضافة الصوت
        video = video.with_audio(
            audio
        )

        # اسم فريد للفيديو
        filename = (
            f"media/videos/"
            f"{uuid.uuid4().hex}.mp4"
        )

        # حفظ الفيديو
        video.write_videofile(
            filename,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        return filename

    finally:

        # إغلاق المقاطع
        for clip in clips:
            try:
                clip.close()
            except Exception:
                pass

        if video is not None:
            try:
                video.close()
            except Exception:
                pass

        if audio is not None:
            try:
                audio.close()
            except Exception:
                pass
