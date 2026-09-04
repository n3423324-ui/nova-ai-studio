from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Project(Base):

    __tablename__ = "projects"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String(200),
        nullable=False
    )


    idea = Column(
        Text,
        nullable=False
    )


    age_group = Column(
        String(50)
    )


    language = Column(
        String(50)
    )


    duration = Column(
        String(50)
    )


    video_type = Column(
        String(100)
    )


    script = Column(
        Text
    )


    images = Column(
        Text
    )


    voice_path = Column(
        String(500)
    )


    video_path = Column(
        String(500)
    )


    youtube_url = Column(
        String(500)
    )


    status = Column(
        String(50),
        default="Draft"
    )
    video_type = Column(
        String(100)
    )

    script = Column(
        Text
    )

    images = Column(
        Text
    )

    voice_path = Column(
        String(500)
    )

    video_path = Column(
        String(500)
    )

    youtube_url = Column(
        String(500)
    )

    status = Column(
        String(50),
        default="Draft"
    )    )


    duration = Column(
        String(50)
    )


    video_type = Column(
        String(100)
    )


    script = Column(
        Text
    )


    status = Column(
        String(50),
        default="Draft"
    )
