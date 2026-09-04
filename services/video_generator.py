import os
import json


def create_video(
    image_prompts,
    voice
):

    folder = "media"

    os.makedirs(
        folder,
        exist_ok=True
    )


    video_file = (
        f"{folder}/video_project.json"
    )


    data = {
        "images": image_prompts,
        "voice": voice,
        "status": "ready"
    }


    with open(
        video_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


    return video_file
