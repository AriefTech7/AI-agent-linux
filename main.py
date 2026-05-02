from langchain_ollama import ChatOllama   
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser


def main():
    # 2. Inisialisasi Model
    llm = ChatOllama(
        model='llama3.1:8b',
        temperature=0.1
    )   

    # 3. Definisi Prompt dengan Placeholder Chat History
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'kamu adalah asisstant pribadi saya.'),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{input}')
    ])

    # 4. Membangun Chain
    chain = prompt | llm | StrOutputParser()

    # 5. Manajemen Chat History
    session_store = {}

    def get_chat_history(session_id: str):
        if session_id not in session_store:
            session_store[session_id] = InMemoryChatMessageHistory()
        return session_store[session_id]

    # 6. Membungkus Chain dengan Riwayat Pesan
    agent = RunnableWithMessageHistory(
        chain,
        get_chat_history,
        input_messages_key='input',
        history_messages_key='chat_history'
    )

    # 7. Loop Interaksi
    session_id = 'user1-level2'
    print("--- Chatbot Ready (Ketik 'exit' untuk keluar) ---")

    while True:
        user_input = input('\nUser: ').strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['exit', 'quit', 'keluar']:
            print('Exiting...')
            break

        print("Assistant: ", end="", flush=True)
        
        # 8. Streaming Response
        config = {'configurable': {'session_id': session_id}}
        
        try:
            for chunk in agent.stream({'input': user_input}, config=config):
                print(chunk, end="", flush=True)
            print() # Baris baru setelah stream selesai
        except Exception as e:
            print(f"\nTerjadi kesalahan: {e}")

# Perbaikan pada pengecekan main module
if __name__ == "__main__":
    main()