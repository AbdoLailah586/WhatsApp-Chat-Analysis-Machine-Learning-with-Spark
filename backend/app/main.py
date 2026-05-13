from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import upload, classify, analytics
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="WhatsApp Message Categorizer", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(classify.router)
app.include_router(analytics.router)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
