def generate_script(
    title,
    idea,
    age,
    language,
    duration
):

    duration_text = str(duration).lower()

    if "1" in duration_text:
        scenes_count = 4

    elif "3" in duration_text:
        scenes_count = 6

    elif "5" in duration_text:
        scenes_count = 8

    else:
        scenes_count = 5


    # ==========================================
    # العربية
    # ==========================================

    if language.lower() == "arabic":

        scenes = [

            f"""
المشهد 1:
تبدأ القصة في عالم جميل وملون.
يظهر بطل القصة ويبدأ يومًا جديدًا.
يتذكر البطل أن لديه شيئًا مهمًا ليتعلمه:
{idea}
""",

            f"""
المشهد 2:
يبدأ البطل في استكشاف المكان من حوله.
يقابل أصدقاء جدد ويتحدث معهم.
يبدأ الجميع في التفكير في فكرة:
{idea}
""",

            f"""
المشهد 3:
تظهر مشكلة صغيرة أمام الأصدقاء.
يشعر الجميع بالحيرة في البداية.
لكنهم يقررون التعاون لإيجاد حل.
""",

            f"""
المشهد 4:
يبدأ الأصدقاء في العمل معًا.
كل واحد منهم يقدم فكرة مفيدة.
يتعلم الجميع أن التعاون يجعل الأشياء أسهل.
""",

            f"""
المشهد 5:
بعد المحاولة والتعلم،
يبدأ الحل بالظهور.
يشعر الأصدقاء بالسعادة لأنهم لم يستسلموا.
""",

            f"""
المشهد 6:
يفهم البطل الدرس المهم.
يعرف أن التعلم والمحاولة يساعداننا دائمًا.
يشارك ما تعلمه مع أصدقائه.
""",

            f"""
المشهد 7:
يحتفل الأصدقاء بنجاحهم.
يلعبون ويضحكون معًا.
يشعر الجميع بالفخر بما حققوه.
""",

            f"""
المشهد 8:
ينتهي اليوم بسعادة.
يتذكر الجميع الدرس الذي تعلموه.
ويعرفون أن كل يوم يمكن أن يكون مغامرة جديدة.
"""
        ]


        selected_scenes = (
            scenes[:scenes_count]
        )


        story = ""


        for index, scene in enumerate(
            selected_scenes,
            start=1
        ):

            scene_text = (
                scene
                .replace(
                    f"المشهد {index}:",
                    ""
                )
                .strip()
            )


            story += (
                f"\nScene {index}:\n"
                f"{scene_text}\n"
            )


        script = f"""
TITLE:
{title}


AGE GROUP:
{age}


LANGUAGE:
العربية


DURATION:
{duration}


STORY:
{story}


MESSAGE:

التعلم ممتع.

التعاون والمحاولة يساعداننا
على اكتشاف أشياء جديدة.

THE END
"""


        return script.strip()


    # ==========================================
    # الإنجليزية
    # ==========================================

    scenes = [

        f"""
Scene 1:
The story begins in a beautiful and colorful world.
The main character starts a new day and discovers
something exciting.
The adventure is connected to this idea:
{idea}
""",

        f"""
Scene 2:
The character explores the world around them
and meets new friends.
Together they begin learning about the new idea.
""",

        f"""
Scene 3:
A small problem appears.
The friends feel confused at first,
but they decide to work together.
""",

        f"""
Scene 4:
Everyone shares ideas and helps each other.
They learn that teamwork can make difficult
things easier.
""",

        f"""
Scene 5:
After trying several ideas,
the friends begin to discover a solution.
They feel happy because they did not give up.
""",

        f"""
Scene 6:
The main character understands an important lesson.
Learning takes patience, curiosity,
and courage.
""",

        f"""
Scene 7:
The friends celebrate what they learned.
They laugh, play,
and enjoy their time together.
""",

        f"""
Scene 8:
The adventure comes to a happy ending.
Everyone remembers the lesson
and looks forward to another new adventure.
"""
    ]


    selected_scenes = (
        scenes[:scenes_count]
    )


    story = ""


    for scene in selected_scenes:

        story += (
            "\n"
            + scene.strip()
            + "\n"
        )


    script = f"""
TITLE:
{title}


AGE GROUP:
{age}


LANGUAGE:
English


DURATION:
{duration}


STORY:

{story}


MESSAGE:

Learning is exciting.

Every new adventure gives us
a chance to discover something new.

THE END
"""


    return script.strip()
