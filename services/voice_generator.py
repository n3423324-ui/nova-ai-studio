import os
import uuid

from gtts import gTTS


def generate_voice(
    text,
    language
):

    if not text:
        raise ValueError(
            "No text provided for voice generation"
        )


    os.makedirs(
        "media/audio",
        exist_ok=True
    )


    # ----------------------------------
    # تحديد اللغة
    # ----------------------------------

    if language.lower() == "arabic":

        voice_language = "ar"

    else:

        voice_language = "en"


    # ----------------------------------
    # اسم الملف
    # ----------------------------------

    filename = (
        "media/audio/"
        f"{uuid.uuid4().hex}.mp3"
    )


    # ----------------------------------
    # إنشاء الصوت
    # ----------------------------------

    try:

        tts = gTTS(

            text=text,

            lang=voice_language,

            slow=False

        )


        tts.save(
            filename
        )


    except Exception as error:

        raise RuntimeError(
            f"Voice generation failed: {error}"
        )


    # ----------------------------------
    # التحقق من الملف
    # ----------------------------------

    if not os.path.exists(
        filename
    ):

        raise RuntimeError(
            "Voice file was not created"
        )


    if os.path.getsize(
        filename
    ) == 0:

        raise RuntimeError(
            "Generated voice file is empty"
        )


    return filename
