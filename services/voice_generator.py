import os


def generate_voice(script, language):

    folder = "media"

    os.makedirs(
        folder,
        exist_ok=True
    )


    voice_file = (
        f"{folder}/voice.txt"
    )


    with open(
        voice_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"Language: {language}\n\n"
        )

        f.write(script)


    return voice_file
