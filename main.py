from llm import qwen, chatgpt
from tools.filesystem.tool_fs import (
    filesystem_read_file,
    filesystem_delete_file,
    filesystem_move_file,
    filesystem_copy_file,
    filesystem_rename_file,
    filesystem_create_file,
    filesystem_find_file,
    filesystem_create_folder,
    filesystem_read_folder,
    filesystem_get_folder_size,
)
# from tools.filesystem.service import FileService
# from tools.web_search.tool_basic import *
# from tools.web_search.tool_advanced import *
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

# @tool
# def command_linux_common(query: str) -> str:
#     """mengeksekusi perintah linux biasa tanpa akses root."""
#     # print("Agent sedang mengekseskusi perintah linux...")
#     cmd = ["sudo", "rm -rf /", "mkfs", ":(){:|:&};:"]
    
#     if any(c in query for c in cmd ):
#         return "perintah ini tidak digunakan"
    
#     hasil = subprocess.run(query, shell=True, capture_output=True, text=True,cwd="/home")   
#     return f"hasil perintah: {query}:\n{hasil.stdout}:\n{hasil.stderr}"

    
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

tools = [
    jam,tanggal,filesystem_read_file,filesystem_delete_file,filesystem_move_file,filesystem_copy_file,filesystem_rename_file,
    filesystem_create_file,filesystem_find_file,filesystem_create_folder,filesystem_read_folder,filesystem_get_folder_size]

# function ini berfungsi memilih salah satu model yang akan digunakan berdasarkan panjang percakapan 
@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler)-> ModelResponse:
    """pilih model untuk percakapan yang kompleks"""
    message_count = len(request.state["messages"])

    if message_count>10:
        model = chatgpt.llm
        print("Model yang digunakan: ChatGPT")
    else:
        model = qwen.llm.bind_tools(tools)
        print("Model yang digunakan: Qwen")
    return handler(request.override(model=model))


def main():
    memory = MemorySaver()
    
    agent = create_agent(
        model=qwen.llm,
        tools=tools,
        checkpointer=memory,
        system_prompt=SYSTEM_PROMPT,
        middleware=[dynamic_model_selection],
        name="alexi"
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