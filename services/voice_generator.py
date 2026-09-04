import os
import uuid


def generate_voice(script, language):

    os.makedirs(
        "media/voices",
        exist_ok=True
    )


    filename = (
        f"media/voices/{uuid.uuid4()}.txt"
    )


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            f"Language: {language}\n\n"
        )

        file.write(script)


    return filename
