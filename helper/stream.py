from langchain_core.messages import AIMessage, AIMessageChunk


async def run_stream(graph, input, config):
    async for msg, metadata in graph.astream(
        input=input,
        stream_mode="messages",
        config=config
    ):
        if not isinstance(msg, (AIMessage, AIMessageChunk)):
            continue

        if not msg.content:
            continue

        print(
            msg.content,
            end="",
            flush=True
        )

    print()