import re


def generate_scenes(script):

    if not script:
        raise ValueError(
            "Script is empty"
        )

    scenes = []

    pattern = (
        r"Scene\s*(\d+)\s*:\s*"
        r"(.*?)(?="
        r"Scene\s*\d+\s*:|"
        r"MESSAGE\s*:|"
        r"THE END|"
        r"$)"
    )

    matches = re.findall(
        pattern,
        script,
        re.DOTALL | re.IGNORECASE
    )

    for scene_number, text in matches:

        description = text.strip()

        if description:

            scenes.append(
                {
                    "scene_number": int(
                        scene_number
                    ),
                    "description": description
                }
            )

    if not scenes:

        raise ValueError(
            "No scenes found in generated script"
        )

    return scenes
