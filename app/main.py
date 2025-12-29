from fastapi import FastAPI
from app.api.routes.copilot import router as copilot_router

app = FastAPI()

app.include_router(copilot_router, prefix="/copilot")

@app.get("/")
def home():
    return {"message": "Copilot app is running"}
