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

        prompt = (
            "3D animated children's movie scene, "
            "high quality cartoon animation, "
            "colorful, bright, cinematic lighting, "
            "friendly characters, safe for children, "
            "educational, professional animation. "
            f"Scene: {description}. "
            "No text, no letters, no subtitles, "
            "no watermark."
        )

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
