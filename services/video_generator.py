import os
import uuid
import json


def create_video(
    image_prompts,
    voice
):

    os.makedirs(
        "media/videos",
        exist_ok=True
    )


    filename = (
        f"media/videos/{uuid.uuid4()}.json"
    )


    data = {
        "images": image_prompts,
        "voice": voice,
        "status": "ready"
    }


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


    return filename            data,
            f,
            ensure_ascii=False,
            indent=4
        )


    return video_file
