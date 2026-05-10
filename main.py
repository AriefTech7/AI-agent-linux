from langchain_ollama import ChatOllama   
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

from datetime import date
import time
import subprocess

@tool
def command_linux_common(query: str) -> str:
    """mengeksekusi perintah linux biasa tanpa akses root."""
    print("Agent sedang mengekseskusi perintah...")
    cmd = ["sudo", "rm -rf /", "mkfs", ":(){:|:&};:"]
    
    if any(c in query for c in cmd ):
        return "perintah ini tidak digunakan"
    
    hasil = subprocess.run(query, shell=True, capture_output=True, text=True,cwd="/home")   
    return f"hasil perintah: {query}:\n{hasil.stdout}:\n{hasil.stderr}"
# @tool
# def execute_command_linux(query: str) -> str:
#     """mengembalikan hasil eksekusi perintah di linux"""
#     result = subprocess.run(query, shell=True, capture_output=True, text=True)
#     return f"hasil perintah: {query} \noutput perintah{result.stdout}\noutput error {result.stderr}"


    
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
2. Always use tools when user asks about system information, time, date, or wants to execute commands
3. Be careful with destructive commands
"""



def main():
    tools = [command_linux_common,jam,tanggal]
    # 2. Inisialisasi Model
    llm = ChatOllama(
        model='llama3.1:8b',
        temperature=0
    ).bind_tools(tools)
    
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
        response = agent.invoke({"messages":[("user",user)]},config={'configurable':{'thread_id':THREAD_ID}},stream_mode="values")
        print(f"Asisstant: {response['messages'][-1].content}",flush=True)
        
# Perbaikan pada pengecekan main module
if __name__ == "__main__":
    main()