from pydantic import BaseModel, ConfigDict
from logic.schemas.url import ResponseUrlSchema, OnPageUrlSchema


class ProcessedUrlsSchema(BaseModel):
    """
    Class representing a Schema for processed_urls key in response.
    """
    internal: list[OnPageUrlSchema] | None = None
    external: list[OnPageUrlSchema] | None = None


class ResponseSchema(BaseModel):
    """
    Class representing a schema for response received from Crawler.
    """
    model_config = ConfigDict(strict=True)
    requested_url: ResponseUrlSchema
    status: str | None
    responded_url: str | None = None
    server: str | None = None
    content_type: str | None = None
    response_time: int | None = None
    visited: int | None = None
    text: str | None = None
    page_title: str | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    on_page_urls: list[OnPageUrlSchema] | None = None
    processed_urls: ProcessedUrlsSchema | None = None


class ProbeResponseSchema(ResponseSchema):
    """
    Class representing a schema for response received from Probe spider.
    """
    favicon_url: ResponseUrlSchema | None = None
    favicon_base64: str | None = None


class SummarySchema(BaseModel):
    """
    Class representing a schema for payload received after finished crawl.
    """
    model_config = ConfigDict(strict=True)
    domain: str
    num_urls_crawled: int
    # num_external_domains_found: int
    time: int
    date: int
