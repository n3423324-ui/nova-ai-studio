from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Project
from services.script_generator import generate_script


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

    script = generate_script(
        title,
        idea,
        age_group,
        language,
        duration
    )


    project = Project(
        title=title,
        idea=idea,
        age_group=age_group,
        language=language,
        duration=duration,
        video_type=video_type,
        script=script
    )


    db.add(project)
    db.commit()
    db.refresh(project)


    return {
        "message": "Project created successfully",
        "id": project.id,
        "script": script
    }
