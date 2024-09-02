
import os
import requests
from typing import Any
import json
from uuid import UUID, uuid4
import pydantic

from .workflows.manager import WorkflowManager
from .datasets.manager import DatasetManager
from .models.manager import ModelsManager
from .secrets.manager import SecretManager

DEFAULT_URL = "https://api.truestate.io"

class Client:

    def __init__(self, api_key: str = None, organisation_id : str = None, base_url : str = None):

        if api_key is None:
            api_key = os.environ.get("TRUESTATE_API_KEY")
    
        if api_key is None:
            raise ValueError("Please ensure you set your API key as an environment variable, e.g. export TRUESTATE_API_KEY='your_api_key'")

        if organisation_id is None:
            organisation_id = os.environ.get("TRUESTATE_ORGANISATION")

        if organisation_id is None:
            raise ValueError("organisation not specified. Please ensure you enter your organisation_id, e.g. ts = Client(api_key, organisation='org_1234567890abcdef')")
        
        if base_url is None:
            base_url = DEFAULT_URL

        self.base_url = base_url
        self.headers = {
            'accept': 'application/json',
            'Current-Org-Id': f'{organisation_id}',
            'Authorization': f"Bearer {api_key}"
        }
        self.workflows = WorkflowManager(self)
        self.datasets = DatasetManager(self)
        self.models = ModelsManager(self)
        self.secrets = SecretManager(self)

    def _api_get(self, url: str) -> Any:
        response = requests.get(url, headers=self.headers)
        return response.json()

    def _api_post(self, url: str, data: Any) -> Any:
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
    
    def _api_put(self, url: str, data: Any) -> Any:
        response = requests.put(url, headers=self.headers, json=data)
        return response.json()
    
    def _api_delete(self, url: str) -> Any:
        response = requests.delete(url, headers=self.headers)
        return response.json()
    

