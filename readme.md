# 🧠 HR-AI Tool: Resume Matcher with RAG, LangChain & LangGraph

This project is a simple, production-style **HR assistant AI tool** built for learning how to integrate LLMs into backend systems using:

- ✅ FastAPI  
- ✅ LangChain  
- ✅ LangGraph  
- ✅ Retrieval-Augmented Generation (RAG)  
- ✅ OpenAI + FAISS Vector Store  
- ✅ SQLite3  

> ✨ Built to simulate real-world LLM workflows — resume parsing, vector indexing, RAG-based matching, and agent-driven summarization with interview questions.

---

## 🔍 Use Case

The app allows you to:

1. Upload **Job Descriptions**
2. Upload **Resumes** (PDF / DOCX)
3. Parse resumes using **GPT**
4. Store both JD and resumes in **Vector DB**
5. Retrieve top-k resumes for a JD using **semantic search**
6. Use **LangGraph agents** to:
   - Generate a summary on why each candidate fits the JD
   - Generate 3–5 interview questions

---

## 🛠️ Tech Stack

| Layer | Tech |
|------|------|
| API  | FastAPI |
| LLM  | OpenAI (ChatGPT + Embeddings) |
| RAG  | LangChain |
| Agent | LangGraph |
| Vector DB | FAISS |
| Parser | GPT (no third-party resume parser used) |
| Storage | SQLite3 |
| Others | Pydantic, BackgroundTasks, Uvicorn |

---

## 📁 Folder Structure

    hr_ats_ai/
    ├── api/ # FastAPI routes
    │ └── routes/
    ├── services/ # Business logic (resume/jd service, parser)
    ├── rag/ # Embedding, vector store management
    ├── agents/ # LangGraph agents & tools
    ├── data/ # Resume/JD upload storage
    ├── main.py # Entry point
    ├── requirements.txt
    └── README.md


---

## ▶️ Getting Started

### 1. Clone and install

    
    git clone https://github.com/prabhupaari/hr_ats_ai.git
    cd hr-ai-tool
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### 2. Add your OpenAI API key
Create a .env file or set as environment variable:
    ```
    bash
    export OPENAI_API_KEY=your-openai-api-key
    ```

### 3. Run the app
    uvicorn main:app -reload

### ✨ Example APIs
    POST /jd/ – Upload a job description

    POST /resume/ – Upload a resume (PDF/DOCX)

    GET /process_resume/{jd_id} – Get top-k matching resumes + summary + questions

### Core Concepts Demonstrated
    ✅ LangChain Document Loading, Splitting, Embeddings

    ✅ FAISS-based semantic retrieval

    ✅ LangGraph agent-based orchestration

    ✅ GPT-driven summarization and question generation

    ✅ FastAPI Background Tasks

    ✅ Production-oriented LLM architecture
