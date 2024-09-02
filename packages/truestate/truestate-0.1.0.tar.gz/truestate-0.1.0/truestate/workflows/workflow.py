

class Workflow:

    def __init__(self, name, description, jobs, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.jobs = jobs

    def __str__(self):
        return f"Workflow: {self.name} - {self.description}"

    def push(self, client):
        response = client.create_workflow(self)
        self.id = response['id']
        return response