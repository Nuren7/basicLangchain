from typing import Annotated, TypedDict

from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from tools import TOOLS


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def create_agent(api_key: str):
    model = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        api_key=api_key,
    )
    model_with_tools = model.bind_tools(TOOLS)

    def call_model(state: AgentState):
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return END

    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue)
    graph.add_edge("tools", "agent")

    return graph.compile()


def run_agent(messages, agent) -> str:
    result = agent.invoke({"messages": messages})
    messages[:] = result["messages"]
    return result["messages"][-1].content