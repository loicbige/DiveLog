from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine,Base

app = FastAPI("divelogAPI", "", "0.0.1")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])

