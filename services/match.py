from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.schema.document import Document
import json

from rag.embedder import get_openai_embedder
from api.database import SessionLocal
from api.models import JobDescription, Resume, ParsedResume


def get_top_k_resumes(jd_text, k=3):
    vectorstore = FAISS.load_local("vector_db", get_openai_embedder(), allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    results = retriever.get_relevant_documents(jd_text)
    resumes = [doc for doc in results if doc.metadata.get("type") == "resume"]
    return resumes


def build_summary_chain():
    prompt = PromptTemplate(
        input_variables=["jd", "resume"],
        template="""Given the Job Description and Resume below, write a short explanation of why this resume is a good fit.

Job Description:
{jd}

Resume:
{resume}

Summary:"""
    )
    llm = OpenAI(temperature=0)
    return LLMChain(prompt=prompt, llm=llm)

def get_jd_text(jd_id: int):
    db = SessionLocal()
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise ValueError("JD not found")
    return jd.description

def match_resumes_with_summary(jd_id: int, k=3):
    db = SessionLocal()
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise ValueError("JD not found")

    top_resumes = get_top_k_resumes(jd.description, k=k)
    chain = build_summary_chain()
    matches = []
    for doc in top_resumes:
        resume_id = doc.metadata.get("resume_id")
        parsed = db.query(ParsedResume).filter(ParsedResume.resume_id == resume_id).first()
        parsed_data = json.loads(parsed.parsed_data) if parsed else {}
        resume_text = doc.page_content

        summary = chain.run(jd=jd.description, resume=resume_text)

        matches.append({
            "resume_id": resume_id,
            "summary": summary,
            "parsed": parsed_data
        })

    return matches
