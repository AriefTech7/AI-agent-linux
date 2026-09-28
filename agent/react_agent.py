from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from system_prompt import SYSTEM_PROMPT
from llm import chatgpt
from tools.tool_manager import tools
from config.connect_db import *

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


llm_with_tools = chatgpt.llm.bind_tools(tools)
tool_node = ToolNode(tools, handle_tool_errors=True)


def llm_call(state: AgentState):
    """
    Node 'llm_call'.
    Bertugas: BERPIKIR & MEMUTUSKAN — apakah perlu memanggil tool
    atau langsung menjawab user.
    """

    history_message = [SystemMessage(SYSTEM_PROMPT)] + state["messages"]

    response_ai = llm_with_tools.invoke(history_message)
    return {
        'messages': [response_ai]
    }


def router(state: AgentState) -> str:
    """
    Setelah llm_call selesai:
    - jika LLM meminta tool_calls -> lanjut ke node 'action'
    - jika tidak                  -> selesai (END)
    """
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "action"
    return END


def create_single_agent(checkpointer, store) -> StateGraph:

    workflow = StateGraph(AgentState)

    workflow.add_node("agent", llm_call)
    workflow.add_node("tool", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        router, {
            "action": "tool",
            END: END,
        },
    )
    workflow.add_edge("tool", "agent")

    graph = workflow.compile(
        checkpointer=checkpointer.get_checkpointer(),
        store=store
    )
    return graph
