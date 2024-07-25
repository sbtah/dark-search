from pydantic import BaseModel, ConfigDict


class UrlSchema(BaseModel):
    """
    Class representing a schema for Url.
    """
    model_config = ConfigDict(strict=True)
    value: str
    anchor: str


class OnPageUrlsSchema(BaseModel):
    """
    Class representing a schema for Data JsonFields for storing urls.
    Example:
    {
        'on_page_urls': [
            {'href': 'http://test.com', 'anchor': 'Some Text'},
            {'href': 'http://test-other.com/page', 'anchor': 'text!'}
        ]
    }
    """
    model_config = ConfigDict(strict=True)
    on_page_urls: list[UrlSchema]
