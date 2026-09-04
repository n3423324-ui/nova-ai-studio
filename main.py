from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import json

from app.database import Base, engine, get_db
from app.models import Project

from services.script_generator import generate_script
from services.scene_generator import generate_scenes
from services.image_generator import generate_image_prompts
from services.voice_generator import generate_voice
from services.video_generator import create_video


# إنشاء الجداول
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="NOVA AI STUDIO"
)


templates = Jinja2Templates(
    directory="templates"
)


@app.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db)
):

    projects = db.query(Project).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "projects": projects
        }
    )


@app.get("/create")
def create_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={}
    )


@app.post("/create")
def create_project(
    title: str = Form(...),
    idea: str = Form(...),
    age_group: str = Form(...),
    language: str = Form(...),
    duration: str = Form(...),
    video_type: str = Form(...),
    db: Session = Depends(get_db)
):

    # 1- إنشاء القصة
    script = generate_script(
        title,
        idea,
        age_group,
        language,
        duration
    )


    # 2- إنشاء المشروع
    project = Project(
        title=title,
        idea=idea,
        age_group=age_group,
        language=language,
        duration=duration,
        video_type=video_type,
        script=script,
        status="Script Generated"
    )


    db.add(project)
    db.commit()
    db.refresh(project)



    # 3- استخراج المشاهد
    scenes = generate_scenes(
        script
    )


    # 4- إنشاء أوصاف الصور
    image_prompts = generate_image_prompts(
        scenes
    )


    project.images = json.dumps(
        image_prompts,
        ensure_ascii=False
    )

    project.status = "Images Ready"


    # 5- إنشاء الصوت
    voice = generate_voice(
        script,
        language
    )


    project.voice_path = voice



    # 6- إنشاء الفيديو
    video = create_video(
        image_prompts,
        voice
    )


    project.video_path = video

    project.status = "Video Created"


    db.commit()
    db.refresh(project)



    return {
        "message": "Project created successfully",
        "id": project.id,
        "status": project.status,
        "script": script
    }
