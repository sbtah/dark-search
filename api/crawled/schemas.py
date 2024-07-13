from ninja import Schema


class ResponseSchema(Schema):
    """
    Class representing a schema for Response received from crawler.
    """
    requested_url: dict
    status: str | None
    responded_url: str = None
    server: str | None = None
    elapsed: int = None
    visited: int = None
    text: str | None = None
    page_title: str | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    on_page_urls: list[dict] | None = None
    processed_urls: dict | None = None


class SummarySchema(Schema):
    """
    Class representing a schema for payload received after finished crawl.
    """
    domain: str
    num_urls_crawled: int
    num_external_domains_found: int
    time: int
    date: int
