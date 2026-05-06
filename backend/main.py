from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine,Base
from routers.dives import router as dives_router
from routers.stats import router as stats_router

from models.dive import Dive
from models.profile import ProfilePoint
from models.equipment import Equipement,DiveEquipement
from models.tanks import Tank
app = FastAPI(title="divelogAPI", description="", version="0.0.1")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status" : "ok"}

app.include_router(dives_router)
app.include_router(stats_router)
