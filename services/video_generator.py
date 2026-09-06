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

    if not images:

        raise ValueError(
            "No images provided"
        )


    if not voice:

        raise ValueError(
            "No voice provided"
        )


    if not os.path.exists(
        voice
    ):

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

        # ----------------------------------
        # تحميل الصوت
        # ----------------------------------

        audio = AudioFileClip(
            voice
        )


        audio_duration = (
            audio.duration
        )


        # ----------------------------------
        # مدة كل مشهد
        # ----------------------------------

        image_duration = (
            audio_duration / len(images)
        )


        # ----------------------------------
        # إنشاء مقاطع الصور
        # ----------------------------------

        for image in images:

            image_path = image.get(
                "image_path"
            )


            if not image_path:

                raise ValueError(
                    "Image path is missing"
                )


            if not os.path.exists(
                image_path
            ):

                raise FileNotFoundError(
                    f"Image not found: {image_path}"
                )


            clip = ImageClip(
                image_path
            )


            clip = clip.with_duration(
                image_duration
            )


            clips.append(
                clip
            )


        # ----------------------------------
        # دمج المشاهد
        # ----------------------------------

        video = concatenate_videoclips(

            clips,

            method="compose"

        )


        # ----------------------------------
        # إضافة الصوت
        # ----------------------------------

        video = video.with_audio(
            audio
        )


        # ----------------------------------
        # اسم الفيديو
        # ----------------------------------

        filename = (
            "media/videos/"
            f"{uuid.uuid4().hex}.mp4"
        )


        # ----------------------------------
        # حفظ الفيديو
        # ----------------------------------

        video.write_videofile(

            filename,

            codec="libx264",

            audio_codec="aac",

            fps=24,

            preset="medium",

            threads=2

        )


        return filename


    finally:

        # ----------------------------------
        # إغلاق المقاطع
        # ----------------------------------

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
