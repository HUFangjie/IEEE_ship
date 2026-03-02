from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine
from .routers import export, jobs, papers, search, settings, swipe

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PaperSwipe API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(settings.router)
app.include_router(search.router)
app.include_router(jobs.router)
app.include_router(papers.router)
app.include_router(swipe.router)
app.include_router(export.router)


@app.get("/health")
def health():
    return {"ok": True}
