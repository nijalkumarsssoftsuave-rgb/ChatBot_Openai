from fastapi import FastAPI
from app.routes.upload_file_route import router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import auth_router
from dotenv import load_dotenv
from db.sqlite_db import init_db
load_dotenv()

init_db()
app = FastAPI(
    title="RAG Document API",
    version="1.0.0"
)

# CORS (required if frontend / Swagger / Postman is used)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)
app.include_router(auth_router)