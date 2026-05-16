from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    auth,
    children,
    recommendations,
    weekly_plans,
    ml_router,
    knowledge,
    photo_analyser,
    ai_insights,s
)

app = FastAPI(title="LittleWell API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "https://littlewell.app",
        "https://www.littlewell.app",
        "https://dev.littlewell.app",
        "https://iteration2.littlehelp.live",
        "https://littlehelp.live",
        "https://www.littlehelp.live",
        "https://iteration1.littlehelp.live",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(children.router)
app.include_router(recommendations.router)
app.include_router(weekly_plans.router)
app.include_router(ml_router.router)
app.include_router(knowledge.router)
app.include_router(photo_analyser.router)
app.include_router(ai_insights.router)


@app.get("/")
def root():
    return {"message": "LittleWell backend is running"}