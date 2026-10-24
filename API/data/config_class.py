from pydantic import ConfigDict
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(extra='forbid')
