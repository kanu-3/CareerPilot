from fastapi import FastAPI

from backend.api.routes.agent_routes import router as agent_router
from backend.api.routes.approval_routes import router as approval_router
from backend.api.routes.profile_routes import router as profile_router


app = FastAPI(
    title="CareerPilot API",
    description="Personal AI Career Agent",
    version="1.0.0",
)


app.include_router(agent_router)
app.include_router(approval_router)
app.include_router(profile_router)


@app.get("/")
def root():
    return {
        "name": "CareerPilot",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }