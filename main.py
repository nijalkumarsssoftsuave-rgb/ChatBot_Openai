from fastapi import FastAPI
from app.routes.upload_file_route import router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import auth_router
from dotenv import load_dotenv
from db.sqlite_db import init_db
from app.routes.admin_auth_routes import admin_auth_router
from app.routes.seating_routes import seating_router
from app.routes.onboarding_chatbot import onboarding_router
from app.routes.pdf_route import pdf_router
load_dotenv()

init_db()
app = FastAPI(
    title="RAG Document API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(admin_auth_router)
app.include_router(seating_router)
app.include_router(onboarding_router)
app.include_router(pdf_router)