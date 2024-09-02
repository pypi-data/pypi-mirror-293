import requests
import json
import typing
import uuid

class DatasetManager:

    def __init__(self, client):
        self.client = client

    def create_dataset(self, dataset):
        response = requests.post(f"{self.client.base_url}/datasets-v2/", headers=self.client.headers, json=dataset)
        return response.json()

    def get(self, id: uuid.UUID = None):

        if id is None:
            response = requests.get(
                f"{self.client.base_url}/datasets-v2/get-datasets-current/",
                headers=self.client.headers
            )
            return response.json()

        else:
            response = requests.post(
                f"{self.client.base_url}/datasets-v2/get-dataset-current/",
                headers=self.client.headers,
                data=json.dumps({'id': id})
            )
            return response.json()

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self.get()

