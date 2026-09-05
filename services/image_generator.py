import os
import uuid
import requests

from groq import Groq


def generate_image_prompts(scenes):

    groq_api_key = os.getenv("GROQ_API_KEY")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")

    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not configured")

    if not account_id:
        raise RuntimeError("CLOUDFLARE_ACCOUNT_ID is not configured")

    if not api_token:
        raise RuntimeError("CLOUDFLARE_API_TOKEN is not configured")

    groq_client = Groq(
        api_key=groq_api_key
    )

    os.makedirs(
        "media/images",
        exist_ok=True
    )

    images = []

    for scene in scenes:

        scene_number = scene["scene_number"]
        description = scene["description"]

        prompt_request = f"""
Create a detailed image generation prompt for a
high-quality children's animated movie.

Scene:
{description}

Requirements:
- Beautiful 3D animated cartoon style
- Bright and colorful
- Friendly characters
- Safe for children
- Cinematic lighting
- Educational atmosphere
- Consistent main character design
- No text inside the image

Return only the final image prompt.
"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You create professional prompts "
                        "for children's animated movies."
                    )
                },
                {
                    "role": "user",
                    "content": prompt_request
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        image_prompt = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        url = (
            f"https://api.cloudflare.com/client/v4/"
            f"accounts/{account_id}/ai/run/"
            f"@cf/black-forest-labs/flux-1-schnell"
        )

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": image_prompt
        }

        result = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120
        )

        if result.status_code != 200:

            raise RuntimeError(
                f"Cloudflare image generation failed: "
                f"{result.status_code} - "
                f"{result.text}"
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
                result.content
            )

        images.append(
            {
                "scene": scene_number,
                "prompt": image_prompt,
                "image_path": filename
            }
        )

    return images- Colorful and cinematic.
- Friendly and safe for children.
- Educational atmosphere.
- Consistent character appearance.
- Bright lighting.
- Professional animated movie quality.
- No text or letters inside the image.

Return only the final image-generation prompt.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert prompt writer "
                        "for children's animated movies."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        image_prompt = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        images.append(
            {
                "scene": scene_number,
                "prompt": image_prompt,
                "image_path": None
            }
        )

    return images3D animated cartoon,
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
