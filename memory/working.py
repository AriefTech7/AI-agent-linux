from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


class WorkingMemory:

    def __init__(
        self,
        checkpointer: AsyncPostgresSaver
    ):
        self.checkpointer = checkpointer

    def get_checkpointer(
        self
    ) -> AsyncPostgresSaver:

        return self.checkpointer