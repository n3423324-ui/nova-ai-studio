def generate_image_prompts(scenes):

    images = []

    for scene in scenes:

        prompt = f"""
Children animation scene.

Style:
3D cartoon,
bright colors,
friendly characters,
safe for kids.

Scene:
{scene['description']}
"""


        images.append(
            {
                "scene": scene["scene_number"],
                "prompt": prompt.strip()
            }
        )


    return images
