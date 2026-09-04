from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./nova.db"
)


APP_NAME = "NOVA AI STUDIO"
