from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import children, recommendations, weekly_plans

app = FastAPI(title="LittleWell API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://littlewell.app",
        "https://www.littlewell.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(children.router)
app.include_router(recommendations.router)
app.include_router(weekly_plans.router)
@app.get("/")
def root():
    return {"message": "LittleWell backend is running"}