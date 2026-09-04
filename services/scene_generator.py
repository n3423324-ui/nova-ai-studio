import re


def generate_scenes(script):

    scenes = []

    matches = re.findall(
        r"Scene\s+\d+:(.*?)(?=Scene\s+\d+:|MESSAGE:|$)",
        script,
        re.DOTALL
    )


    for index, text in enumerate(matches, start=1):

        scenes.append(
            {
                "scene_number": index,
                "description": text.strip()
            }
        )


    return scenes
