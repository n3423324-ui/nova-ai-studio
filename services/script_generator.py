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

- Create multiple scenes.
- Make the story educational.
- Use simple language suitable for children.
- Keep the story safe and friendly.
- Include a clear lesson.
- Do not include harmful, scary, or inappropriate content.

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
Scene description

Scene 2:
Scene description

Scene 3:
Scene description

Scene 4:
Scene description

MESSAGE:
Educational lesson
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert writer "
                    "of educational children's stories."
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
