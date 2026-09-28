from langgraph.graph import StateGraph, START, END

from backend.agent.state import AgentState

from backend.agent.lifecycle import (
    start_agent_run,
    finalize_agent_run,
)

from backend.agent.nodes import (
    retrieve_profile,
    retrieve_job,
    retrieve_knowledge_node,
    retrieve_memories,
    retrieve_learning,
)

from backend.agent.planner import create_plan
from backend.agent.reasoner import reason_about_job
from backend.agent.tool_selector import select_tool

from backend.agent.approval import (
    check_tool_approval,
    create_approval_request,
)

from backend.agent.executor import execute_selected_tool


def route_after_approval_check(state: AgentState) -> str:
    if state.get("error"):
        return "finalize"

    if state.get("approval_required"):
        return "approval"

    return "execute"


def build_agent_graph():
    graph = StateGraph(AgentState)


    graph.add_node(
        "start_run",
        start_agent_run,
    )


    graph.add_node(
        "retrieve_profile",
        retrieve_profile,
    )

    graph.add_node(
        "retrieve_job",
        retrieve_job,
    )

    graph.add_node(
        "retrieve_knowledge",
        retrieve_knowledge_node,
    )

    graph.add_node(
        "retrieve_memories",
        retrieve_memories,
    )

    graph.add_node(
        "retrieve_learning",
        retrieve_learning,
    )


    graph.add_node(
        "planner",
        create_plan,
    )

    graph.add_node(
        "reason",
        reason_about_job,
    )



    graph.add_node(
        "select_tool",
        select_tool,
    )


    graph.add_node(
        "check_approval",
        check_tool_approval,
    )

    graph.add_node(
        "create_approval_request",
        create_approval_request,
    )

    graph.add_node(
        "execute",
        execute_selected_tool,
    )


    graph.add_node(
        "finalize_run",
        finalize_agent_run,
    )

    graph.add_edge(
        START,
        "start_run",
    )

    graph.add_edge(
        "start_run",
        "retrieve_profile",
    )

    graph.add_edge(
        "retrieve_profile",
        "retrieve_job",
    )

    graph.add_edge(
        "retrieve_job",
        "retrieve_knowledge",
    )

    graph.add_edge(
        "retrieve_knowledge",
        "retrieve_memories",
    )

    graph.add_edge(
        "retrieve_memories",
        "retrieve_learning",
    )

    graph.add_edge(
        "retrieve_learning",
        "planner",
    )

    graph.add_edge(
        "planner",
        "reason",
    )

    graph.add_edge(
        "reason",
        "select_tool",
    )

    graph.add_edge(
        "select_tool",
        "check_approval",
    )

    graph.add_conditional_edges(
        "check_approval",
        route_after_approval_check,
        {
            "execute": "execute",
            "approval": "create_approval_request",
            "finalize": "finalize_run",
        },
    )

    graph.add_edge(
        "create_approval_request",
        END,
    )

    graph.add_edge(
        "execute",
        "finalize_run",
    )

    graph.add_edge(
        "finalize_run",
        END,
    )

    return graph.compile()


agent_graph = build_agent_graph()