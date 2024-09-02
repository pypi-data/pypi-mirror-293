import requests
import typing
import json
import uuid


class ModelsManager:

    def __init__(self, client):
        self.client = client

    def create_model(self, model):
        response = requests.post(f"{self.client.base_url}/artifacts/", headers=self.client.headers, json=model)
        return response.json()

    def get_model(self, model_id: uuid.UUID):
        response = requests.post(f"{self.client.base_url}/artifacts/get-artifact-current", headers=self.client.headers, data=json.dumps({'id': model_id}))
        return response.json()

    def get_models(self):
        response = requests.get(f"{self.client.base_url}/artifacts/get-artifacts-current", headers=self.client.headers)
        return response.json()

    def __call__(self) -> typing.Any:
        return self.get_models()