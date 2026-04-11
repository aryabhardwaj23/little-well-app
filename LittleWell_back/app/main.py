from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import children, recommendations

app = FastAPI(title="LittleWell API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(children.router)
app.include_router(recommendations.router)


@app.get("/")
def root():
    return {"message": "LittleWell backend is running"}