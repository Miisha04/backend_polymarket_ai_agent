from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.monitoring import router as monitoring_router
from app.routers.chat import router as chat_router
from app.database import engine, Base 

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Backend Orchestrator",
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",  # адрес вашего фронтенда
    "http://localhost:8501", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(monitoring_router)
app.include_router(chat_router)

