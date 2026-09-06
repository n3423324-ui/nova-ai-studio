import re


def generate_scenes(script):

    scenes = []

    pattern = (
        r"(?:Scene|المشهد)\s+(\d+)\s*:"
        r"(.*?)(?=(?:Scene|المشهد)\s+\d+\s*:|"
        r"(?:MESSAGE|Message|الدرس)\s*:|$)"
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

    return scenes
