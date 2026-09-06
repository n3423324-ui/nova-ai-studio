import os

from groq import Groq


def generate_script(
    title,
    idea,
    age,
    language,
    duration
):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured"
        )

    client = Groq(
        api_key=api_key
    )

    prompt = f"""
Create a complete children's educational story.

Title: {title}

Idea: {idea}

Age Group: {age}

Language: {language}

Duration: {duration}

Requirements:

- Write a fun educational children's story.
- Use simple language suitable for the selected age group.
- Create at least 4 scenes.
- Make the story safe and friendly for children.
- Include an educational lesson.
- Keep the main character consistent.
- Do not include harmful or scary content.

Use exactly this format:

TITLE:
Story title

AGE GROUP:
Age group

LANGUAGE:
Language

DURATION:
Duration

STORY:

Scene 1:
Description

Scene 2:
Description

Scene 3:
Description

Scene 4:
Description

MESSAGE:
Educational lesson
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert writer of safe, "
                    "fun, educational children's stories."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_completion_tokens=2000
    )

    return response.choices[0].message.content
