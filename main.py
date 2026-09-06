import os
import uuid

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from services.script_generator import generate_script
from services.scene_generator import generate_scenes
from services.image_generator import generate_image_prompts
from services.voice_generator import generate_voice
from services.video_generator import create_video


app = FastAPI(
    title="NOVA AI Studio"
)


os.makedirs(
    "media/videos",
    exist_ok=True
)

os.makedirs(
    "media/images",
    exist_ok=True
)

os.makedirs(
    "media/audio",
    exist_ok=True
)


app.mount(
    "/media",
    StaticFiles(directory="media"),
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
            background: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 700px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
        }

        input,
        textarea,
        select,
        button {
            width: 100%;
            padding: 12px;
            margin-top: 8px;
            margin-bottom: 18px;
            box-sizing: border-box;
        }

        button {
            background: #6c3cff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
        }

        #loading {
            display: none;
            font-size: 18px;
        }

        #result {
            display: none;
            margin-top: 25px;
        }

        video {
            width: 100%;
            border-radius: 12px;
        }

        .download {
            display: block;
            margin-top: 15px;
            padding: 14px;
            text-align: center;
            background: #22c55e;
            color: white;
            text-decoration: none;
            border-radius: 8px;
        }

    </style>

</head>

<body>

<div class="container">

    <h1>✨ Create New NOVA Video</h1>


    <form id="videoForm">

        <label>
            Video Title
        </label>

        <input
            id="title"
            required
        >


        <label>
            Video Idea
        </label>

        <textarea
            id="idea"
            required
        ></textarea>


        <label>
            Age Group
        </label>

        <select id="age">

            <option>
                3-6 Years
            </option>

            <option>
                7-10 Years
            </option>

        </select>


        <label>
            Language
        </label>

        <select id="language">

            <option>
                English
            </option>

            <option>
                Arabic
            </option>

        </select>


        <label>
            Duration
        </label>

        <select id="duration">

            <option>
                1 Minute
            </option>

            <option>
                3 Minutes
            </option>

            <option>
                5 Minutes
            </option>

        </select>


        <label>
            Video Type
        </label>

        <select id="video_type">

            <option>
                Educational Story
            </option>

            <option>
                Adventure
            </option>

            <option>
                Bedtime Story
            </option>

        </select>


        <button
            type="submit"
        >
            🚀 Generate Video
        </button>

    </form>


    <div id="loading">

        ⏳ Creating your video...

        <br>

        This may take a few minutes.

    </div>


    <div id="result">

        <h2>
            🎬 Your Video Is Ready!
        </h2>

        <video
            id="videoPlayer"
            controls
        ></video>


        <a
            id="downloadButton"
            class="download"
            download
        >
            ⬇ Download Video
        </a>


        <h3>
            Generated Story
        </h3>

        <pre
            id="story"
        ></pre>

    </div>

</div>


<script>

const form =
    document.getElementById(
        "videoForm"
    );


form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        document.getElementById(
            "loading"
        ).style.display =
            "block";


        document.getElementById(
            "result"
        ).style.display =
            "none";


        const formData =
            new FormData();


        formData.append(
            "title",
            document.getElementById(
                "title"
            ).value
        );


        formData.append(
            "idea",
            document.getElementById(
                "idea"
            ).value
        );


        formData.append(
            "age",
            document.getElementById(
                "age"
            ).value
        );


        formData.append(
            "language",
            document.getElementById(
                "language"
            ).value
        );


        formData.append(
            "duration",
            document.getElementById(
                "duration"
            ).value
        );


        formData.append(
            "video_type",
            document.getElementById(
                "video_type"
            ).value
        );


        try {

            const response =
                await fetch(
                    "/create",
                    {
                        method:
                            "POST",

                        body:
                            formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    data.message ||
                    "Video generation failed"
                );

            }


            document.getElementById(
                "videoPlayer"
            ).src =
                data.video_url;


            document.getElementById(
                "downloadButton"
            ).href =
                data.video_url;


            document.getElementById(
                "story"
            ).textContent =
                data.script;


            document.getElementById(
                "loading"
            ).style.display =
                "none";


            document.getElementById(
                "result"
            ).style.display =
                "block";

        }

        catch (error) {

            document.getElementById(
                "loading"
            ).style.display =
                "none";


            alert(
                "Error: " +
                error.message
            );

        }

    }
);

</script>

</body>

</html>
"""


@app.post(
    "/create"
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

        script = generate_script(
            title,
            idea,
            age,
            language,
            duration
        )


        scenes = generate_scenes(
            script
        )


        images = generate_image_prompts(
            scenes
        )


        voice = generate_voice(
            script
        )


        video_path = create_video(
            images,
            voice
        )


        video_filename = os.path.basename(
            video_path
        )


        video_url = (
            f"/media/videos/"
            f"{video_filename}"
        )


        return JSONResponse(
            {
                "message":
                    "Project created successfully",

                "status":
                    "Video Created",

                "id":
                    uuid.uuid4().hex,

                "script":
                    script,

                "video_url":
                    video_url,

                "scenes":
                    scenes
            }
        )


    except Exception as error:

        return JSONResponse(
            status_code=500,

            content={
                "message":
                    "Video generation failed",

                "detail":
                    str(error)
            }
        )
