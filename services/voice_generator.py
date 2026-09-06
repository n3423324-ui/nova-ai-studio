import os
import uuid

from gtts import gTTS


def get_language_code(language):

    language_map = {
        "English": "en",
        "Arabic": "ar",
        "العربية": "ar",
        "French": "fr",
        "Spanish": "es",
        "German": "de"
    }

    return language_map.get(
        language,
        "en"
    )


def generate_voice_for_scene(
    text,
    language
):

    if not text:
        raise ValueError(
            "Scene text is empty"
        )

    os.makedirs(
        "media/audio",
        exist_ok=True
    )

    lang_code = get_language_code(
        language
    )

    filename = (
        "media/audio/"
        f"{uuid.uuid4().hex}.mp3"
    )

    tts = gTTS(
        text=text,
        lang=lang_code,
        slow=False
    )

    tts.save(
        filename
    )

    return filename


def generate_scene_voices(
    scenes,
    language
):

    voices = []

    for scene in scenes:

        voice_path = (
            generate_voice_for_scene(
                scene["description"],
                language
            )
        )

        voices.append(
            {
                "scene_number": (
                    scene["scene_number"]
                ),
                "voice_path": voice_path
            }
        )

    return voices
