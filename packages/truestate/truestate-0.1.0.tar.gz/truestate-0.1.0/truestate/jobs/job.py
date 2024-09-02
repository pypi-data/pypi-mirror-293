

class Job:
    
    def __init__(self, operation, name, description, inputs, outputs):
        self.name = name
        self.description = description
        self.operation = operation
        self.inputs = inputs
        self.outputs = outputs

    def __str__(self):
        return f"Job(name={self.name}, description={self.description}, command={self.command}, schedule={self.schedule})"

    def __repr__(self):
        return self.__str__()

    def run(self):
        print(f"Running job: {self.name}")
        # Run the command here
        print(f"Finished running job: {self.name}")