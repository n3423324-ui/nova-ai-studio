import re


def generate_scenes(script):

    scenes = []

    parts = re.split(
        r"Scene \d+:",
        script
    )

    for part in parts:
        text = part.strip()

        if text and not text.startswith("🌟"):
            scenes.append(text)

    return scenes
