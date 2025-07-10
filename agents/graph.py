from langgraph.graph import StateGraph, END
from agents.tools import generate_summary, generate_interview_questions

from typing import Dict
from typing import TypedDict

class ResumeAgentState(TypedDict):
    jd_text: str
    resume_text: str
    summary: str = ""
    questions: list = []


def summarize_node(state: ResumeAgentState):
    state["summary"] = generate_summary.invoke({
        "resume_text": state["resume_text"],
        "jd_text": state["jd_text"],
    })
    return state

def question_node(state: ResumeAgentState):
    state["questions"] = generate_interview_questions.invoke({
        "resume_text": state["resume_text"],
        "jd_text": state["jd_text"],
    })
    return state

def build_resume_graph():
    builder = StateGraph(ResumeAgentState)
    builder.add_node("summarize", summarize_node)
    builder.add_node("questions", question_node)
    builder.set_entry_point("summarize")
    builder.add_edge("summarize", "questions")
    builder.add_edge("questions", END)
    return builder.compile()