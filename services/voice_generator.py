import os
import uuid
import asyncio

import edge_tts


def generate_voice(text, language):

    os.makedirs(
        "media/audio",
        exist_ok=True
    )

    voices = {
        "English": "en-US-AvaMultilingualNeural",
        "Arabic": "ar-SA-HamedNeural"
    }

    voice = voices.get(
        language,
        "en-US-AvaMultilingualNeural"
    )

    filename = (
        f"media/audio/{uuid.uuid4().hex}.mp3"
    )

    async def create_audio():

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice
        )

        await communicate.save(
            filename
        )

    asyncio.run(
        create_audio()
    )

    return filename
