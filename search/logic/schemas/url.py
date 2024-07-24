from pydantic import BaseModel, ConfigDict


class UrlSchema(BaseModel):
    """
    Class representing a schema for Url.
    """
    model_config = ConfigDict(strict=True)
    value: str
    anchor: str
    number_of_requests: int
