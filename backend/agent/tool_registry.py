from backend.tools.job_management_tool import save_job
from backend.tools.learning_tool import (
    create_learning_task,
    update_learning_task,
)
from backend.tools.memory_tool import save_memory
from backend.tools.notification_tool import create_notification
from backend.tools.application_tool import update_application
from backend.tools.mock_action_tool import mock_submit_application

TOOL_REGISTRY = {
    "save_job": save_job,
    "create_learning_task": create_learning_task,
    "update_learning_task": update_learning_task,
    "save_memory": save_memory,
    "create_notification": create_notification,
    "update_application": update_application,

    "submit_application": mock_submit_application,
}


def get_tool(tool_name: str):
    return TOOL_REGISTRY.get(tool_name)