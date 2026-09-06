import os
import shutil
import uuid

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from services.script_generator import generate_script
from services.scene_generator import generate_scenes
from services.image_generator import generate_image_prompts
from services.voice_generator import generate_scene_voices
from services.video_generator import create_video


# إنشاء التطبيق
app = FastAPI(
    title="NOVA AI Studio"
)


# إنشاء مجلدات المشروع
os.makedirs(
    "media/images",
    exist_ok=True
)

os.makedirs(
    "media/audio",
    exist_ok=True
)

os.makedirs(
    "media/videos",
    exist_ok=True
)


# السماح بعرض الملفات
app.mount(
    "/media",
    StaticFiles(
        directory="media"
    ),
    name="media"
)


@app.get(
    "/",
    response_class=HTMLResponse
)
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>NOVA AI Studio</title>

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
        >

        <style>

            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                padding: 20px;
            }

            .container {
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 20px;
            }

            h1 {
                text-align: center;
            }

            label {
                display: block;
                margin-top: 20px;
                font-size: 18px;
            }

            input,
            textarea,
            select {
                width: 100%;
                padding: 15px;
                margin-top: 8px;
                box-sizing: border-box;
                font-size: 16px;
            }

            button {
                width: 100%;
                padding: 18px;
                margin-top: 25px;
                font-size: 20px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                background: #6c3df0;
                color: white;
            }

            button:hover {
                background: #5429c7;
            }

            .result {
                margin-top: 30px;
            }

            video {
                width: 100%;
                border-radius: 15px;
                margin-top: 20px;
            }

            .download {
                display: block;
                margin-top: 20px;
                padding: 18px;
                text-align: center;
                background: #20b85b;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-size: 20px;
            }

            pre {
                white-space: pre-wrap;
                background: #f5f5f5;
                padding: 20px;
                border-radius: 10px;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>NOVA AI Studio</h1>

            <form
                action="/create"
                method="post"
            >

                <label>
                    Video Title
                </label>

                <input
                    type="text"
                    name="title"
                    required
                >


                <label>
                    Video Idea
                </label>

                <textarea
                    name="idea"
                    rows="5"
                    required
                ></textarea>


                <label>
                    Age Group
                </label>

                <select
                    name="age"
                >

                    <option value="3-6 Years">
                        3-6 Years
                    </option>

                    <option value="7-10 Years">
                        7-10 Years
                    </option>

                    <option value="10-14 Years">
                        10-14 Years
                    </option>

                </select>


                <label>
                    Language
                </label>

                <select
                    name="language"
                >

                    <option value="English">
                        English
                    </option>

                    <option value="Arabic">
                        العربية
                    </option>

                </select>


                <label>
                    Duration
                </label>

                <select
                    name="duration"
                >

                    <option value="1 Minute">
                        1 Minute
                    </option>

                    <option value="3 Minutes">
                        3 Minutes
                    </option>

                    <option value="5 Minutes">
                        5 Minutes
                    </option>

                </select>


                <label>
                    Video Type
                </label>

                <select
                    name="video_type"
                >

                    <option value="Educational Story">
                        Educational Story
                    </option>

                    <option value="Kids Story">
                        Kids Story
                    </option>

                    <option value="Learning Video">
                        Learning Video
                    </option>

                </select>


                <button
                    type="submit"
                >
                    🚀 Generate Video
                </button>

            </form>

        </div>

    </body>

    </html>
    """


@app.post(
    "/create",
    response_class=HTMLResponse
)
def create_project(

    title: str = Form(...),

    idea: str = Form(...),

    age: str = Form(...),

    language: str = Form(...),

    duration: str = Form(...),

    video_type: str = Form(...)

):

    try:

        # =====================================
        # 1. إنشاء القصة
        # =====================================

        script = generate_script(

            title=title,

            idea=idea,

            age=age,

            language=language,

            duration=duration

        )


        # =====================================
        # 2. استخراج المشاهد
        # =====================================

        scenes = generate_scenes(
            script
        )


        if not scenes:

            raise RuntimeError(
                "No scenes were generated"
            )


        # =====================================
        # 3. إنشاء الصور
        # =====================================

        images = generate_image_prompts(
            scenes
        )


        if not images:

            raise RuntimeError(
                "No images were generated"
            )


        # =====================================
        # 4. إنشاء صوت مستقل لكل مشهد
        # =====================================

        voices = generate_scene_voices(

            scenes=scenes,

            language=language

        )


        if not voices:

            raise RuntimeError(
                "No voices were generated"
            )


        # =====================================
        # 5. إنشاء الفيديو
        # =====================================

        video_path = create_video(

            images=images,

            voices=voices

        )


        if not os.path.exists(
            video_path
        ):

            raise RuntimeError(
                "Video file was not created"
            )


        # تحويل المسار إلى رابط
        video_url = (
            "/"
            + video_path.replace(
                "\\",
                "/"
            )
        )


        # =====================================
        # صفحة النتيجة
        # =====================================

        return f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>
                Video Created Successfully
            </title>

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    background: #f4f4f4;
                    padding: 20px;
                }}

                .container {{
                    max-width: 650px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 20px;
                }}

                h1 {{
                    text-align: center;
                    color: #222;
                }}

                video {{
                    width: 100%;
                    margin-top: 20px;
                    border-radius: 15px;
                }}

                .download {{
                    display: block;
                    margin-top: 25px;
                    padding: 18px;
                    text-align: center;
                    background: #20b85b;
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                    font-size: 20px;
                }}

                .back {{
                    display: block;
                    margin-top: 15px;
                    padding: 15px;
                    text-align: center;
                    background: #6c3df0;
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                }}

                .story {{
                    margin-top: 30px;
                    padding: 20px;
                    background: #f5f5f5;
                    border-radius: 10px;
                    white-space: pre-wrap;
                    direction: {"rtl" if language == "Arabic" else "ltr"};
                }}

            </style>

        </head>

        <body>

            <div class="container">

                <h1>
                    🎬 Video Created Successfully
                </h1>


                <h2>
                    {title}
                </h2>


                <video
                    controls
                    playsinline
                >

                    <source
                        src="{video_url}"
                        type="video/mp4"
                    >

                    Your browser does not support video.

                </video>


                <a
                    class="download"
                    href="{video_url}"
                    download
                >

                    ↓ Download Video

                </a>


                <div class="story">

                    <h2>
                        Generated Story
                    </h2>

                    {script}

                </div>


                <a
                    class="back"
                    href="/"
                >

                    ← Create Another Video

                </a>

            </div>

        </body>

        </html>
        """

    except Exception as error:

        return f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>
                Error
            </title>

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    padding: 30px;
                    background: #f4f4f4;
                }}

                .error {{
                    max-width: 600px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 20px;
                }}

                pre {{
                    white-space: pre-wrap;
                    color: red;
                }}

            </style>

        </head>

        <body>

            <div class="error">

                <h1>
                    Error Creating Video
                </h1>

                <pre>{str(error)}</pre>

                <a href="/">
                    Try Again
                </a>

            </div>

        </body>

        </html>
        """


@app.get(
    "/download/{filename}"
)
def download_video(
    filename: str
):

    file_path = (
        f"media/videos/{filename}"
    )

    if not os.path.exists(
        file_path
    ):

        raise FileNotFoundError(
            "Video not found"
        )

    return FileResponse(

        file_path,

        media_type="video/mp4",

        filename=filename

    )


@app.get(
    "/health"
)
def health():

    return {
        "status": "ok",
        "message": "NOVA AI Studio is running"
    }
