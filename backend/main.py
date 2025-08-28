# ================================
# 📂 backend/main.py
# ================================

from fastapi import FastAPI
from backend.routers import users, clients , tasks , payments
from backend import models, database
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


# Create tables
# models.Base.metadata.create_all(bind=database.engine)

# Create FastAPI app
app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(tasks.router)
app.include_router(payments.router)


# ✅ Allow frontend (http://127.0.0.1:5500) to talk with backend (http://127.0.0.1:8000)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:5500"],  # frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins temporarily for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve frontend folder at /frontend
app.mount("/frontend", StaticFiles(directory="./frontend"), name="frontend")

# Redirect root to frontend
@app.get("/")
def root():
    return RedirectResponse(url="/frontend/index.html")