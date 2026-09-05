import os

from groq import Groq


def generate_script(
    title,
    idea,
    age,
    language,
    duration
):

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

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
Main idea: {idea}
Target age: {age}
Language: {language}
Approximate duration: {duration}

Requirements:

- The story must be safe for children.
- Use simple language appropriate for the target age.
- Make the story fun, educational, and positive.
- Divide the story into clear scenes.
- Each scene should be visually descriptive.
- Include a beginning, middle, and ending.
- Include a positive educational message.
- Do not include violence, fear, or inappropriate content.

Use exactly this format:

🌟 NOVA KIDS STORY

TITLE:
[title]

AGE GROUP:
[age]

LANGUAGE:
[language]

DURATION:
[duration]

STORY:

Scene 1:
[story scene]

Scene 2:
[story scene]

Scene 3:
[story scene]

Scene 4:
[story scene]

Scene 5:
[story scene]

MESSAGE:
[positive educational lesson]

THE END ✨
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are NOVA AI, a professional "
                    "children's story writer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8,
        max_tokens=2000
    )

    script = response.choices[0].message.content

    return script
Scene 3:
NOVA explains the lesson
in a fun and safe way.

MESSAGE:

Learning is exciting.
Every child can discover something new.

THE END ✨
"""

    return script
