import pydantic

class SQLTransform(pydantic.BaseModel):
    query: str


