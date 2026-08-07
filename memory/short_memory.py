class ShortMemory:
    def __init__(self, graph, checkpointer):
        self.graph = graph
        self.checkpointer = checkpointer

    def create_config(self, thread_id):
        return {
            "configurable": {
                "thread_id": thread_id
            }
        }

    def get_state(self, thread_id):
        config = self.create_config(thread_id)
        return self.graph.get_state(config)

    def get_messages(self, thread_id):
        state = self.get_state(thread_id)

        if not state:
            return []

        return state.values.get("messages", [])

    def get_last_message(self, thread_id):
        messages = self.get_messages(thread_id)
        return messages[-1] if messages else None

    def get_message_count(self, thread_id):
        return len(self.get_messages(thread_id))

    def get_context(self, thread_id):
        return self.get_messages(thread_id)

    def clear_thread(self, thread_id):
        self.checkpointer.delete_thread(thread_id)
