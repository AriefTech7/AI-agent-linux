import psycopg
from langgraph.store.postgres.aio import AsyncPostgresStore
from langgraph.checkpoint.postgres import PostgresSaver
# DB_URL = "postgresql://[user database]:linux@localhost:[port database]/[nama database]?sslmode=disable"
DB_URL = "postgresql://agent_linux:linux@localhost:5432/aiagentdb?sslmode=disable"

async def create_storePostgre():
    store = AsyncPostgresStore.from_conn_string(DB_URL)
    await store.setup()
    return store

def create_checkpointerPostgre():
    conn = psycopg.connect(DB_URL)
    checkpointer = PostgresSaver(conn=conn)
    return checkpointer
