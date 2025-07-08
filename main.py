from fastapi import FastAPI
import uvicorn

from api.database import Base, engine
from api.routes import jd, resume

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(jd.router, prefix="/jd", tags=["Job Descriptions"])
app.include_router(resume.router, prefix="/resume", tags=["Resumes"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)