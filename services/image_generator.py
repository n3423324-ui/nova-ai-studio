import os

from groq import Groq


def generate_image_prompts(scenes):

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured"
        )

    client = Groq(
        api_key=api_key
    )

    images = []

    for scene in scenes:

        scene_number = scene["scene_number"]
        description = scene["description"]

        prompt = f"""
Create a detailed image-generation prompt for a
children's animated movie scene.

Scene description:
{description}

Requirements:
- High-quality 3D animated cartoon style.
- Colorful and cinematic.
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
