from app.database import Base, engine
from app.routers import auth, exercises, muscles, workouts
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Rep Mate API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(exercises.router)
app.include_router(muscles.router)
app.include_router(workouts.router)

@app.get("/health")
def health():
    return {"status": "ok"}
