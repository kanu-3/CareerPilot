from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agent.graph import agent_graph


router = APIRouter(prefix="/agent", tags=["Agent"])


class AgentRunRequest(BaseModel):
    user_id: int
    request: str
    job_id: int | None = None


@router.post("/run")
def run_agent(payload: AgentRunRequest):
    try:
        state = {
            "user_id": payload.user_id,
            "request": payload.request,
            "job_id": payload.job_id,
        }

        result = agent_graph.invoke(state)

        return {
            "success": not bool(result.get("error")),
            "run_id": result.get("run_id"),
            "decision": result.get("decision"),
            "explanation": result.get("explanation"),
            "selected_tool": result.get("selected_tool"),
            "tool_input": result.get("tool_input"),
            "tool_result": result.get("tool_result"),
            "approval_required": result.get("approval_required", False),
            "approval_status": result.get("approval_status"),
            "skill_gaps": result.get("skill_gaps", []),
            "response": result.get("response"),
            "error": result.get("error"),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
    