import pydantic 
from uuid import UUID, uuid4


class Workflow(pydantic.BaseModel):
    id: str
    name: str
    description: str
    organisation_id: str
    current_config_version_id: str
    created_at: str

class WorkflowConfig(pydantic.BaseModel):
    id: UUID = uuid4()
    workflow_id: UUID
    config: dict
    created_at: str

