from backend.agent.state import AgentState

from backend.tools.profile_tool import get_profile, get_skills
from backend.tools.jobs_tool import get_job
from backend.rag.retriever import retrieve_knowledge
from backend.tools.memory_tool import get_memories
from backend.tools.learning_tool import get_learning_tasks


def retrieve_profile(state: AgentState) -> AgentState:
    user_id = state["user_id"]

    profile = get_profile(user_id)
    skills = get_skills(user_id)

    state["profile"] = profile
    state["skills"] = skills

    return state


def retrieve_job(state: AgentState) -> AgentState:
    job_id = state.get("job_id")

    if job_id is None:
        state["error"] = "No job_id provided."
        return state

    job = get_job(job_id)

    state["job"] = job

    return state


def retrieve_knowledge_node(state: AgentState) -> AgentState:
    user_id = state["user_id"]
    request = state["request"]

    knowledge = retrieve_knowledge(
        query=request,
        user_id=user_id,
        limit=6,
    )

    state["knowledge"] = knowledge

    return state


def retrieve_memories(state: AgentState) -> AgentState:
    user_id = state["user_id"]

    memories = get_memories(user_id)

    state["memories"] = memories

    return state


def retrieve_learning(state: AgentState) -> AgentState:
    user_id = state["user_id"]

    learning_tasks = get_learning_tasks(user_id)

    state["learning_tasks"] = learning_tasks

    return state