from langchain_ollama import ChatOllama   
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.output_parsers import StrOutputParser
from datetime import date
import time
import subprocess

@tool
def run_linux_command(query: str) -> str:
    """Fungsi untuk mendapatkan perintah Linux berdasarkan query pengguna."""
    allowed_command = ['ls', 'pwd', 'cd', 'btop']
    hasil = ""
    if query[0] not in allowed_command:
        return "perintah tidak diizinkan"
    else:
        hasil = subprocess.run(query, shell=True, capture_output=True, text=True)
    return f"hasil perintah '{query}':\n{hasil.stdout}\n{hasil.stderr}"


    
@tool
def jam()->str:
    """mengembalikan jam saat ini"""
    time_now = time.localtime()
    return time.strftime("%H:%M",time_now)

@tool
def tanggal()-> str:
    """mengembalikan tanggal saat ini"""
    tanggal_hari_ini = date.today()
    return tanggal_hari_ini.strftime("%A, %d %B %Y")
    



THREAD_ID = 'user-id-1'
SYSTEM_PROMPT = """
You are a linux system administrator profesional.
Rules:
1. if user is just chatting, responds normally
"""



def main():
    tools = [run_linux_command,jam,tanggal]
    # 2. Inisialisasi Model
    llm = ChatOllama(
        model='llama3.1:8b',
        temperature=0
    )   
    
    memory = MemorySaver()
    
    agent = create_agent(
        llm,
        tools=tools,
        checkpointer=memory,
        system_prompt=SYSTEM_PROMPT
        )
    
    
    print("🐧 Linux Agent siap. Ketik 'exit' untuk keluar.")
    while True:
        user = input('User: ').strip()
        if user.lower() in ['exit']:
            print('Exiting...')
            break
        response = agent.invoke({"messages":[("user",user)]},config={'configurable':{'thread_id':THREAD_ID}})
        print(response['messages'][-1].content)
# Perbaikan pada pengecekan main module
if __name__ == "__main__":
    main()