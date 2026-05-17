from langchain_ollama import ChatOllama   
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

from dotenv import load_dotenv
load_dotenv()

from datetime import date
import time
import subprocess
from system_prompt import SYSTEM_PROMPT

@tool
def command_linux_common(query: str) -> str:
    """mengeksekusi perintah linux biasa tanpa akses root."""
    # print("Agent sedang mengekseskusi perintah linux...")
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

tools = [command_linux_common,jam,tanggal]
# 2. Inisialisasi Model
basic_model = ChatOllama(
        model='llama3.1:8b',
        temperature=0
    ).bind_tools(tools)
advanced_model = ChatOpenAI(
    model='gpt-5-nano',
    temperature=0.7
)

# function ini berfungsi memilih salah satu model yang akan digunakan berdasarkan panjang percakapan 
@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler)-> ModelResponse:
    """pilih model untuk percakapan yang kompleks"""
    message_count = len(request.state["messages"])

    if message_count>10:
        model = advanced_model
    else:
        model = basic_model
    return handler(request.override(model=model))


def main():
    memory = MemorySaver()
    
    agent = create_agent(
        model=basic_model,
        tools=tools,
        checkpointer=memory,
        system_prompt=SYSTEM_PROMPT,
        middleware=[dynamic_model_selection]
        # name="alexi"
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