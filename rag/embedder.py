import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def get_openai_embedder():
    return OpenAIEmbeddings(model="text-embedding-3-small")
