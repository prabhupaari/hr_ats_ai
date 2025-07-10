from fastapi import FastAPI, HTTPException
import uvicorn

from api.database import Base, engine
from api.routes import jd, resume
from agents.graph import build_resume_graph, ResumeAgentState
from services.match import match_resumes_with_summary, get_top_k_resumes, get_jd_text

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(jd.router, prefix="/jd", tags=["Job Descriptions"])
app.include_router(resume.router, prefix="/resume", tags=["Resumes"])


@app.get("/match/{jd_id}")
async def process_resume(jd_id: int, k: int = 3):
    jd_text = get_jd_text(jd_id)
    if not jd_text:
        raise HTTPException(status_code=404, detail="JD not found")

    resumes = get_top_k_resumes(jd_text, k)
    results = []

    graph = build_resume_graph()

    for doc in resumes:
        resume_text = doc.page_content
        state = ResumeAgentState(jd_text=jd_text, resume_text=resume_text)
        final_state = graph.invoke(state)
        results.append({
            "summary": final_state["summary"],
            "questions": final_state["questions"],
        })

    return {"results": results}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)