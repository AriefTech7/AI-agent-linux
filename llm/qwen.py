from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()

llm = ChatOllama(
    model='qwen2.5:3b',
    temperature=0,
)