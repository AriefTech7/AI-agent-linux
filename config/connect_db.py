import psycopg
from psycopg.rows import dict_row
from langgraph.store.postgres.aio import AsyncPostgresStore
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
# DB_URL = "postgresql://[user database]:linux@localhost:[port database]/[nama database]?sslmode=disable"
DB_URL = "postgresql://agent_linux:linux@localhost:5432/aiagentdb?sslmode=disable"


async def create_storePostgre():
    conn = await psycopg.AsyncConnection.connect(
        DB_URL,
        autocommit=True,
        row_factory=dict_row
    )
    store = AsyncPostgresStore(conn=conn)
    return store


async def create_checkpointer_postgres():
    conn = await psycopg.AsyncConnection.connect(
        DB_URL,
        autocommit=True,
        row_factory=dict_row
    )

    checkpointer = AsyncPostgresSaver(conn=conn)

    return checkpointer, conn
