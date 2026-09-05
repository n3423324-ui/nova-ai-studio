import os
import uuid

from openai import OpenAI


def generate_voice(
    script,
    language
):

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "OPENAI_API_KEY is not configured"
        )


    client = OpenAI(
        api_key=api_key
    )


    os.makedirs(
        "media/voices",
        exist_ok=True
    )


    filename = (
        f"media/voices/"
        f"{uuid.uuid4().hex}.mp3"
    )


    instructions = f"""
Speak clearly and warmly.

This is a children's educational story.

Language:
{language}

Use a friendly,
gentle,
enthusiastic storytelling voice.
"""


    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=script,
        instructions=instructions,
        response_format="mp3"
    )


    response.write_to_file(
        filename
    )


    return filename
