def generate_script(
    title,
    idea,
    age,
    language,
    duration
):

    if language.lower() in [
        "arabic",
        "العربية",
        "ar"
    ]:

        return f"""
المشهد 1:
في يوم جميل، بدأت شخصيتنا الصغيرة مغامرة جديدة.

المشهد 2:
اكتشف الأطفال فكرة جديدة:
{idea}

المشهد 3:
تعلم الجميع الدرس بطريقة ممتعة وآمنة.

المشهد 4:
احتفل الأصدقاء بما تعلموه وعادوا سعداء.

الدرس:
التعلم ممتع، وكل طفل يستطيع اكتشاف أشياء جديدة.
""".strip()

    return f"""
Scene 1:
On a beautiful day, our little character started a new adventure.

Scene 2:
The children discovered something new:
{idea}

Scene 3:
Everyone learned the lesson in a fun and safe way.

Scene 4:
The friends celebrated what they learned and went home happily.

Message:
Learning is exciting, and every child can discover something new.
""".strip()
