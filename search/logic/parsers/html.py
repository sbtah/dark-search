from httpx import Response
from lxml.html import HtmlElement, HTMLParser, fromstring, tostring
from lxml.html.clean import Cleaner
from logic.objects.url import Url


class HtmlExtractor:
    """
    Class designed to work with httpx Response.
    The Main purpose is to convert text response to HtmlElement and extract data like:
    - Cleaned html body,
    - Page title
    - Metadata (title, description),
    - On page urls.
    """

    def __init__(self) -> None:
        pass

    def parse(self, html_element: HtmlElement) -> dict:
        """
        Parse HtmlElement.
        Return dictionary with extracted data.
        - :arg html_element: Lxml HtmlElement.
        """
        html: str = self.extract_html_body(html_element)
        page_title: str | None = self.extract_page_title(html_element)
        meta_title: str | None = self.extract_meta_title(html_element)
        meta_description: str | None = self.extract_meta_description(html_element)
        # on_page_urls: list[str] | None  = self.extract_urls(html_element)
        on_page_urls: list[Url] | None = self.extract_urls_with_texts(html_element)
        favicon_url: str | None = self.extract_favicon_url(html_element)
        return {
            'html': html,
            'page_title': page_title,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'on_page_urls': on_page_urls,
            'favicon_url': favicon_url,
        }

    def page(self, response: Response) -> HtmlElement | None:
        """
        Parse response object and return HtmlElement on success.
        - :arg response: httpx Response object.
        """
        try:
            hp = HTMLParser(encoding='utf-8')
            element: HtmlElement = fromstring(
                response.text,
                parser=hp,
            )
            return element
        except Exception:
            return None

    def extract_urls(self, html_element: HtmlElement) -> list[str] | None:
        """
        Search for urls in body of provided HtmlElement.
        - :arg html_element: Lxml HtmlElement.
        """
        urls: list[str] = html_element.xpath('/html/body//a[@href and not(@href="")]/@href')
        return [url.strip() for url in urls] if urls else None


    def extract_urls_with_texts(self, html_element: HtmlElement) -> list[dict[str: str, str: str]] | None:
        """
        Search for urls in body of provided HtmlElement.
        - :arg html_element: Lxml HtmlElement.
        """
        urls: list[HtmlElement] = html_element.xpath('/html/body//a[@href and not(@href="") and not(@href=" ")]')
        return [{'url': url.xpath('./@href')[0], 'anchor': url.text_content().strip()} for url in urls] if urls else None


    def extract_favicon_url(self, html_element: HtmlElement) -> str | None:
        """
        Search for possible favicon in head of requested page.
        - :arg html_element: Lxml HtmlElement.
        """
        # Sometimes this may be a list of urls with different icon for different resolutions.
        favicon_urls: list[str] = html_element.xpath('/html/head/link[contains(@href, "favicon")]/@href')
        # We want only 1 url and usually 1st url if the smallest one in terms of resolution.
        return favicon_urls[0].strip() if favicon_urls else None


    def extract_page_title(self, html_element: HtmlElement) -> str | None:
        """
        Extract h1 text content from requested webpage.
        Sometimes h1 can contain other nested elements,
            because of that we want to extract entire text contained within h1 tag.
        Return parsed content.
        - :arg html_element: Lxml HtmlElement.
        """
        h1: list[HtmlElement] = html_element.xpath('.//h1')
        return h1[0].text_content().strip() if h1 else None


    def extract_meta_title(self, html_element: HtmlElement) -> str | None:
        """
        Extract meta-title content from the requested webpage.
        Return parsed content.
        - :arg html_element: Lxml HtmlElement.
        """
        title_element: list[HtmlElement] = html_element.xpath('/html/head/title/text()')
        return title_element[0].strip() if title_element else None

    def extract_meta_description(self, html_element: HtmlElement) -> str | None:
        """
        Extract description content from the requested webpage.
        Return parsed content.
        - :arg html_element: Lxml HtmlElement.
        """
        description_element: list[str] = html_element.xpath('/html/head/meta[@name="description"]/@content')
        return description_element[0].strip() if description_element else None

    def extract_html_body(self, html_element: HtmlElement) -> str:
        """
        Extract body part from HtmlElement.
        Clean html of dangerous elements and attributes.
        Return string representing Html content.
        """
        body = html_element.xpath('/html/body')
        cleaner = Cleaner(
                style=True,
                inline_style=True,
                scripts=True,
                javascript=True,
                embedded=True,
                frames=True,
                meta=True,
                annoying_tags=True,
                kill_tags=['img']
            )
        try:
            sanitized_content = tostring(cleaner.clean_html(body[0]))
        except Exception:
            sanitized_content = b''
        return sanitized_content.decode('utf-8')
