import os
import base64
import uuid

from openai import OpenAI


def generate_image_prompts(scenes):

    images = []

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured"
        )

    client = OpenAI(
        api_key=api_key
    )

    os.makedirs(
        "media/images",
        exist_ok=True
    )

    for scene in scenes:

        scene_number = scene["scene_number"]
        description = scene["description"]

        prompt = f"""
Create a high quality children's animated movie image.

Style:
3D animated cartoon,
cinematic,
colorful,
bright,
friendly,
safe for children,
educational,
professional animation.

Scene:
{description}

Keep the visual style and main character design
consistent with the other scenes.

No text inside the image.
"""

        result = client.images.generate(
            model="gpt-image-2",
            prompt=prompt,
            size="1024x1024"
        )

        image_data = base64.b64decode(
            result.data[0].b64_json
        )

        filename = (
            f"media/images/"
            f"scene_{scene_number}_"
            f"{uuid.uuid4().hex}.png"
        )

        with open(
            filename,
            "wb"
        ) as file:

            file.write(
                image_data
            )

        images.append(
            {
                "scene": scene_number,
                "prompt": prompt.strip(),
                "image_path": filename
            }
        )

    return images
