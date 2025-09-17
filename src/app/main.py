from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.config import settings
from src.app.routes import voice_agents

is_production = settings.environment == "production"

app = FastAPI(
    title="Building a voice agents for forms",
    description="Using FastAPI and Groq API",
    version="1.0.0",
    terms_of_service=None,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Sebastian Marat Urdanegui Bisalaya",
        "url": "https://sebastianurdanegui.vercel.app/",
        "email": "sebasurdanegui@gmail.com"
    }
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.include_router(voice_agents.router)
