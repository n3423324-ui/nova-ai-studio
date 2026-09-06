import os
import uuid
import base64

import requests


def generate_image_prompts(scenes):

    images = []

    account_id = os.getenv(
        "CLOUDFLARE_ACCOUNT_ID"
    )

    api_token = os.getenv(
        "CLOUDFLARE_API_TOKEN"
    )

    if not account_id:
        raise RuntimeError(
            "CLOUDFLARE_ACCOUNT_ID is not configured"
        )

    if not api_token:
        raise RuntimeError(
            "CLOUDFLARE_API_TOKEN is not configured"
        )

    os.makedirs(
        "media/images",
        exist_ok=True
    )

    url = (
        "https://api.cloudflare.com/client/v4/"
        f"accounts/{account_id}/"
        "ai/run/@cf/black-forest-labs/"
        "flux-1-schnell"
    )

    headers = {
        "Authorization": (
            f"Bearer {api_token}"
        ),
        "Content-Type": (
            "application/json"
        )
    }

    for scene in scenes:

        scene_number = scene.get(
            "scene_number",
            1
        )

        description = scene.get(
            "description",
            ""
        )

        # منع الوصف الطويل جداً
        description = description.strip()

        if len(description) > 500:
            description = description[:500]

        prompt = f"""
Create a high quality 3D animated children's movie scene.

Scene description:
{description}

Style:
Professional Pixar-inspired 3D animation.
Colorful.
Cinematic.
Friendly.
Safe for children.
Consistent characters.

IMPORTANT:
Do not generate any text.
Do not generate subtitles.
Do not generate captions.
Do not generate letters.
Do not generate words.
Do not generate Arabic text.
Do not generate English text.
Do not generate logos.
Do not generate signs containing readable text.
The image must contain absolutely no writing.

Only show the characters and the environment.

Scene:
{description}
"""
        # حماية إضافية من تجاوز حد Cloudflare
        if len(prompt) > 1500:
            prompt = prompt[:1500]

        response = requests.post(
            url,
            headers=headers,
            json={
                "prompt": prompt
            },
            timeout=120
        )

        if not response.ok:

            raise RuntimeError(
                "Cloudflare image generation failed: "
                + response.text
            )

        try:

            result = response.json()

            image_data = (
                result["result"]["image"]
            )

            image_bytes = base64.b64decode(
                image_data
            )

        except Exception:

            # في بعض استجابات Cloudflare
            # تكون الصورة مباشرة
            image_bytes = response.content

        filename = (
            "media/images/"
            f"scene_{scene_number}_"
            f"{uuid.uuid4().hex}.png"
        )

        with open(
            filename,
            "wb"
        ) as file:

            file.write(
                image_bytes
            )

        images.append(
            {
                "scene": scene_number,
                "prompt": prompt,
                "image_path": filename
            }
        )

    return images
