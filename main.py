import uuid
import asyncio
from agent import react_agent
from helper.stream import run_stream
from memory.working import WorkingMemory
from memory.episodic import Episodic
# from MCP.client import Client
from langchain_core.messages import HumanMessage
from config.connect_db import *


async def main():
    # database postgresql for working memory
    checkpointer, conn = await create_checkpointer_postgres()
    await checkpointer.setup()
    working_memory = WorkingMemory(checkpointer=checkpointer)

    # database postgresql for episodic memory
    store = await create_storePostgre()
    await store.setup()
    episodic_memory = Episodic(store=store)
    
    
    # graph
    agent = react_agent.create_single_agent(
        checkpointer=working_memory,
        store=episodic_memory        
        )

    # thread id
    THREAD_ID = str(uuid.uuid4())
    config = {"configurable": {"thread_id": THREAD_ID}}

    print("agent Agent Linux siap. Ketik 'exit' untuk keluar.")
    while True:
        user = input("\nYou: ").strip()
        if not user:
            continue
        if user.lower() in ("exit", "quit"):
            await conn.close()
            break
        message = {"messages": [HumanMessage(content=user)]}
        print("\nAgent: ", end="")
        await run_stream(graph=agent, input=message, config=config)

if __name__ == "__main__":
    asyncio.run(main())
