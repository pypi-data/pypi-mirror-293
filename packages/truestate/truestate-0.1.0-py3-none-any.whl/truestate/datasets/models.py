

import uuid
import enum
import typing
import pydantic

class FileType(enum.Enum):
    Csv = "Csv"
    Parquet = "Parquet"


class Dataset(pydantic.BaseModel):
    id: uuid.UUID
    current_version_id: uuid.UUID
    name: str
    description: typing.Optional[str] = None
    filetype: FileType
    organisation_id: str


class AliasDataset(pydantic.BaseModel):
    alias: str
    dataset: Dataset

