from pydantic import BaseModel, Field, ConfigDict


class SingleHttpStatusLogSchema(BaseModel):
    """
    Class representing a schema for single log in 'last_http_status_logs'.
    """
    model_config = ConfigDict(strict=True)
    date: str = Field(pattern=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}')
    status: str = Field(pattern=r'\d{3}')


class LastHttpStatusLogsSchema(BaseModel):
    """
    Class representing a schema for a Webpage JsonField 'last_http_status_logs'.
    Example:
    {
        'status_logs': [
            {'date': '22-07-2024 03:12', 'status': '404'},
            {'date': '20-07-2024 13:48', 'status': '200'},
        ]
    }
    """
    model_config = ConfigDict(strict=True)
    status_logs: list[SingleHttpStatusLogSchema]


class SingleLinkingToWebpagesLogSchema(BaseModel):
    """
    Class representing a schema for single log in 'lining_to_webpages_logs'.
    """
    model_config = ConfigDict(strict=True)
    date: str = Field(pattern=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}')
    urls: list[str]


class LinkingToWebpagesLogsSchema(BaseModel):
    """
    Class representing a schema for Webpage JsonField 'linking_to_webpages_logs'.
    Example:
    {
        'webpages_logs':[
            {'date': '20-11-2021', 'urls': ['https://test.onion.page1', 'http://test.onion/page-2']},
            {'date': '20-11-2021', 'urls': ['https://test.onion.page1',]}
        ]
    }
    """
    model_config = ConfigDict(strict=True)
    webpages_logs: list[SingleLinkingToWebpagesLogSchema]
