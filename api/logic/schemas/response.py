from pydantic import BaseModel, ConfigDict


class ResponseSchema(BaseModel):
    """
    Class representing a schema for Response received from crawler.
    """
    model_config = ConfigDict(strict=True)
    requested_url: dict
    status: str | None
    responded_url: str | None = None
    server: str | None = None
    elapsed: int | None = None
    visited: int | None = None
    text: str | None = None
    page_title: str | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    on_page_urls: list[dict] | None = None
    processed_urls: dict | None = None


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
