import json


def generate_image_prompts(scenes):

    images = []

    for index, scene in enumerate(scenes, start=1):

        prompt = {
            "scene": index,
            "prompt": f"""
Create a colorful children's animation scene.

Style:
3D cartoon, friendly, safe for kids age 3-6.

Scene description:
{scene}

Characters:
NOVA the little explorer.

Mood:
Happy, educational, magical.
"""
        }

        images.append(prompt)

    return images
