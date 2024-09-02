import requests
import json
import typing
import uuid
from .models import Secret

class SecretManager:

    def __init__(self, client):
        self.client = client

    def create_secret(self, secret) -> Secret:
        response = requests.post(f"{self.client.base_url}/secrets/create-secret/", headers=self.client.headers, json=secret)
        return response.json()

    def get_secret(self, dataset_id: uuid.UUID) -> Secret:
        response = requests.post(f"{self.client.base_url}/secrets/get-secret/", headers=self.client.headers, data=json.dumps({'id': dataset_id}))
        return response.json()
    
    def get_secrets(self) -> typing.List[Secret]:
        url = f"{self.client.base_url}/secrets/get-secrets/"
        secrets = self.client._api_get(url)
        return [Secret(**secret) for secret in secrets]


    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self.get_secrets()

