import requests
import json
import typing
import uuid

from .models import Workflow, WorkflowConfig

class WorkflowManager:

    def __init__(self, client):
        self.client = client

    def create_workflow(self, workflow):
        response = requests.post(f"{self.client.base_url}/workflows/", headers=self.client.headers, json=workflow)
        return response.json()

    def get_workflow(self, workflow_id: uuid.UUID):
        response = requests.post(f"{self.client.base_url}/workflows/get-workflow/", headers=self.client.headers, data=json.dumps({'id': workflow_id}))
        workflow_record = response.json()
        print(workflow_record)
        return Workflow(**workflow_record)

    
    def get_workflows(self):
        response = requests.get(f"{self.client.base_url}/workflows/get-workflows/", headers=self.client.headers)
        result = response.json()
        workflows = [Workflow(**i) for i in response.json()]
        
        latest_configs = []
        
        for workflow in workflows:
            response = requests.post(
                f"{self.client.base_url}/workflow-config-versions/get-config-versions/",
                headers=self.client.headers,
                data=json.dumps({'workflow_id': workflow.id})
            )
            result = response.json()
            workflow_config = WorkflowConfig(**result[0])
            latest_configs.append(workflow_config)
        
        return latest_configs

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self.get_workflows()