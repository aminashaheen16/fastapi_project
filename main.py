from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.api import router

app = FastAPI(
    title="FastAPI LLM API",
    description="FastAPI + Cohere LLM + JWT Auth + Supabase + File Analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router with /api prefix
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to FastAPI LLM API 🚀",
        "docs": "/docs",
        "api_root": "/api"
    }