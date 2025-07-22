from fastapi import FastAPI
from backend.routers import users, clients , tasks , payments
from backend import models, database

# Create tables
# models.Base.metadata.create_all(bind=database.engine)

# Create FastAPI app
app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(tasks.router)
app.include_router(payments.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello my fellow, good morning!"}

