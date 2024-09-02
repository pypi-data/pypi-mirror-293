import pydantic

class SalesforceLoad(pydantic.BaseModel):
    name: str
    description: str
    subdomain: str
    secret_id: str
    SOQL: str

