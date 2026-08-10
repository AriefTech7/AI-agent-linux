from psycopg_pool import ConnectionPool 
from langgraph.checkpoint.postgres import PostgresSaver


DB_URL= "postgresql://agent_linux:linux@localhost:5432/aiagentdb?sslmode=disable"
pool = ConnectionPool(DB_URL)
checkpointer = PostgresSaver(pool)
# checkpointer.setup()


