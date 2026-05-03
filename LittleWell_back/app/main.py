from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import children, recommendations, weekly_plans, auth, ml_router   

app = FastAPI(title="LittleWell API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://littlewell.app",
        "https://www.littlewell.app",
        "https://dev.littlewell.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)           # ← new
app.include_router(children.router)
app.include_router(recommendations.router)
app.include_router(weekly_plans.router)
app.include_router(ml_router.router)

@app.get("/")
def root():
    return {"message": "LittleWell backend is running"}