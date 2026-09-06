import os
import traceback

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from services.script_generator import generate_script
from services.scene_generator import generate_scenes
from services.image_generator import generate_image_prompts
from services.voice_generator import generate_voice
from services.video_generator import create_video


app = FastAPI(
    title="NOVA AI Studio",
    version="1.0.0"
)


# ---------------------------------------
# إنشاء المجلدات المطلوبة
# ---------------------------------------

os.makedirs("media", exist_ok=True)
os.makedirs("media/images", exist_ok=True)
os.makedirs("media/audio", exist_ok=True)
os.makedirs("media/videos", exist_ok=True)


# ---------------------------------------
# السماح بالوصول إلى ملفات الفيديو
# ---------------------------------------

app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)


# ---------------------------------------
# الصفحة الرئيسية
# ---------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
def home():

    return """
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>NOVA AI Studio</title>

<style>

body {
    font-family: Arial, sans-serif;
    background: #f5f5f5;
    padding: 30px;
}

.container {
    max-width: 700px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 15px;
}

h1 {
    text-align: center;
}

label {
    display: block;
    margin-top: 20px;
    font-size: 20px;
}

input,
textarea,
select {
    width: 100%;
    padding: 12px;
    margin-top: 8px;
    font-size: 18px;
    box-sizing: border-box;
}

textarea {
    height: 120px;
}

button {
    margin-top: 25px;
    width: 100%;
    padding: 15px;
    font-size: 20px;
    cursor: pointer;
}

#loading {
    display: none;
    margin-top: 20px;
    font-size: 18px;
}

#result {
    margin-top: 25px;
}

video {
    width: 100%;
    margin-top: 20px;
}

</style>

</head>


<body>

<div class="container">

<h1>NOVA Video</h1>


<form id="videoForm">

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
    required
></textarea>


<label>
Age Group
</label>

<select name="age">

<option value="3-6 Years">
3-6 Years
</option>

<option value="6-9 Years">
6-9 Years
</option>

<option value="9-12 Years">
9-12 Years
</option>

</select>


<label>
Language
</label>

<select name="language">

<option value="English">
English
</option>

<option value="Arabic">
Arabic
</option>

</select>


<label>
Duration
</label>

<select name="duration">

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

<select name="video_type">

<option value="Educational Story">
Educational Story
</option>

<option value="Adventure">
Adventure
</option>

<option value="Learning">
Learning
</option>

</select>


<button
    type="submit"
    id="generateButton"
>

🚀 Generate Video

</button>

</form>


<div id="loading">

⏳ Creating your video...

<br>

This may take a few minutes.

</div>


<div id="result"></div>


</div>


<script>

const form =
    document.getElementById(
        "videoForm"
    );


const loading =
    document.getElementById(
        "loading"
    );


const result =
    document.getElementById(
        "result"
    );


const button =
    document.getElementById(
        "generateButton"
    );


form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        loading.style.display =
            "block";


        result.innerHTML =
            "";


        button.disabled =
            true;


        const formData =
            new FormData(form);


        try {

            const response =
                await fetch(
                    "/create",
                    {
                        method: "POST",
                        body: formData
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


            loading.style.display =
                "none";


            button.disabled =
                false;


            result.innerHTML =
                `
                <h2>Video Created Successfully</h2>

                <p>${data.status}</p>

                <video controls>

                    <source
                        src="${data.video_url}"
                        type="video/mp4"
                    >

                </video>

                `;

        }

        catch (error) {

            loading.style.display =
                "none";


            button.disabled =
                false;


            result.innerHTML =
                `
                <h2>Error</h2>

                <p>
                    ${error.message}
                </p>
                `;

        }

    }
);

</script>


</body>

</html>
"""


# ---------------------------------------
# API إنشاء الفيديو
# ---------------------------------------

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

        # -----------------------------------
        # التحقق من البيانات
        # -----------------------------------

        if not title.strip():

            raise ValueError(
                "Video title is required"
            )


        if not idea.strip():

            raise ValueError(
                "Video idea is required"
            )


        # -----------------------------------
        # 1. إنشاء القصة
        # -----------------------------------

        script = generate_script(

            title=title.strip(),

            idea=idea.strip(),

            age=age,

            language=language,

            duration=duration

        )


        if not script:

            raise RuntimeError(
                "Script generation failed"
            )


        # -----------------------------------
        # 2. استخراج المشاهد
        # -----------------------------------

        scenes = generate_scenes(
            script
        )


        if not scenes:

            raise RuntimeError(
                "No scenes were generated"
            )


        # -----------------------------------
        # 3. إنشاء الصور
        # -----------------------------------

        images = generate_image_prompts(
            scenes
        )


        if not images:

            raise RuntimeError(
                "No images were generated"
            )


        # -----------------------------------
        # 4. إنشاء الصوت
        #
        # التصحيح المهم:
        # تمرير language إلى generate_voice
        # -----------------------------------

        voice = generate_voice(

            script,

            language

        )


        if not voice:

            raise RuntimeError(
                "Voice generation failed"
            )


        # -----------------------------------
        # 5. إنشاء الفيديو
        # -----------------------------------

        video_path = create_video(

            images,

            voice

        )


        if not video_path:

            raise RuntimeError(
                "Video creation failed"
            )


        # -----------------------------------
        # تحويل المسار إلى رابط
        # -----------------------------------

        video_url = (
            "/media/"
            + video_path.replace(
                "media/",
                ""
            )
        )


        # -----------------------------------
        # النتيجة النهائية
        # -----------------------------------

        return JSONResponse(

            status_code=200,

            content={

                "message":
                    "Project created successfully",

                "status":
                    "Video Created",

                "title":
                    title,

                "video_type":
                    video_type,

                "script":
                    script,

                "scenes":
                    scenes,

                "video_url":
                    video_url

            }

        )


    except Exception as error:

        print(
            "VIDEO CREATION ERROR:"
        )

        print(
            traceback.format_exc()
        )


        return JSONResponse(

            status_code=500,

            content={

                "message":
                    "Video creation failed",

                "detail":
                    str(error)

            }

        )


# ---------------------------------------
# Health Check
# ---------------------------------------

@app.get(
    "/health"
)
def health():

    return {

        "status":
            "ok",

        "service":
            "NOVA AI Studio"

    }
