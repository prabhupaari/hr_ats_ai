from fastapi import FastAPI, HTTPException
import uvicorn

from api.database import Base, engine
from api.routes import jd, resume

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(jd.router, prefix="/jd", tags=["Job Descriptions"])
app.include_router(resume.router, prefix="/resume", tags=["Resumes"])

from services.match import match_resumes_with_summary



@app.post("/match_resumes/{jd_id}")
def match_resumes(jd_id: int):
    try:
        results = match_resumes_with_summary(jd_id)
        return {"matches": results}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)