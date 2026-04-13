from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import children, recommendations, api

app = FastAPI(title="LittleWell API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://littlewell.app",
        "https://www.littlewell.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(children.router)
app.include_router(recommendations.router)
app.include_router(api.router)

@app.get("/")
def root():
    return {"message": "LittleWell backend is running"}
