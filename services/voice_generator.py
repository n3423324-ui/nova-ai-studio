import os
import uuid
from gtts import gTTS


def generate_voice(script, language="English"):

    if not script or not script.strip():
        raise ValueError("Script is empty")

    os.makedirs(
        "media/audio",
        exist_ok=True
    )

    language_map = {
        "English": "en",
        "Arabic": "ar",
        "German": "de",
        "French": "fr",
        "Spanish": "es"
    }

    lang_code = language_map.get(
        language,
        "en"
    )

    filename = (
        f"media/audio/"
        f"{uuid.uuid4().hex}.mp3"
    )

    tts = gTTS(
        text=script,
        lang=lang_code,
        slow=False
    )

    tts.save(
        filename
    )

    return filename
