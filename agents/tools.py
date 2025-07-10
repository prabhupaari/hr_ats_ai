from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from typing import List
import os

llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")

@tool
def generate_summary(resume_text: str, jd_text: str) -> str:
    """Generate a summary explaining why the candidate is a good fit for the job."""
    prompt = f"""
    Job Description:
    {jd_text}

    Resume:
    {resume_text}

    Based on the above, provide a concise summary of why this candidate is suitable for the job.
    """
    return llm.invoke(prompt).content


@tool
def generate_interview_questions(resume_text: str, jd_text: str) -> List[str]:
    """Generate 3 to 5 interview questions tailored to the candidate based on resume and JD."""
    prompt = f"""
    Job Description:
    {jd_text}

    Resume:
    {resume_text}

    Based on the above, provide 3 to 5 interview questions to evaluate the candidate.
    """
    return llm.invoke(prompt).content.split("\n")
