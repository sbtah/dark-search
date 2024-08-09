from httpx import Response
from lxml.html import HtmlElement, HTMLParser, fromstring, tostring
import html2text
from lxml.html.clean import Cleaner


class HtmlExtractor:
    """
    Class designed to work with httpx Response.
    The Main purpose is to convert text response to HtmlElement and extract data like:
    - Text from entire body,
    - Page title
    - Metadata (title, description),
    - On page urls with texts.
    """

    def parse(self, html_element: HtmlElement, favicon: bool = True) -> dict:
        """
        Parse HtmlElement.
        Return dictionary with extracted data.
        - :arg html_element: Lxml HtmlElement.
        - :arg favicon: If set to `True` parser will try extracting favicon url.
        """
        page_title: str | None = self.extract_page_title(html_element)
        meta_title: str | None = self.extract_meta_title(html_element)
        meta_description: str | None = self.extract_meta_description(html_element)
        on_page_urls: list[dict[str, str]] | None = self.extract_urls_with_texts(html_element)
        text: str | None = self.extract_entire_text(html_element)
        result = {
            'text': text,
            'page_title': page_title,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'on_page_urls': on_page_urls,
        }
        if favicon is True:
            favicon_url: str | None = self.extract_favicon_url(html_element)
            result['favicon_url'] = favicon_url
        return result

    @staticmethod
    def page(response: Response) -> HtmlElement | None:
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

    @staticmethod
    def extract_urls_with_texts(html_element: HtmlElement) -> list[dict[str, str]] | None:
        """
        Search for urls in body of provided HtmlElement.
        - :arg html_element: Lxml HtmlElement.
        """
        urls: list[HtmlElement] = html_element.xpath('/html/body//a[@href and not(@href="") and not(@href=" ")]')
        return [
            {
                'value': url.xpath('./@href')[0],
                'anchor': url.text_content().strip()
            } for url in urls if isinstance(url, HtmlElement)
        ] if urls else None

    @staticmethod
    def extract_favicon_url(html_element: HtmlElement) -> str | None:
        """
        Search for possible favicon in head of requested page.
        - :arg html_element: Lxml HtmlElement.
        """
        # Sometimes this may be a list of urls with different icon for different resolutions.
        favicon_urls: list[str] = html_element.xpath('/html/head/link[contains(@href, "favicon")]/@href')
        # We want first url and usually 1st url if the smallest one in terms of resolution.
        return favicon_urls[0].strip() if favicon_urls else None

    @staticmethod
    def extract_page_title(html_element: HtmlElement) -> str | None:
        """
        Extract h1 text content from requested webpage.
        Sometimes h1 can contain other nested elements,
            because of that we want to extract entire text contained within h1 tag.
        Return parsed content.
        - :arg html_element: Lxml HtmlElement.
        """
        h1: list[HtmlElement] = html_element.xpath('.//h1')
        return h1[0].text_content().strip() if h1 else None

    @staticmethod
    def extract_meta_title(html_element: HtmlElement) -> str | None:
        """
        Extract meta-title content from the requested webpage.
        Return parsed content.
        - :arg html_element: Lxml HtmlElement.
        """
        title_element: list[HtmlElement] = html_element.xpath('/html/head/title/text()')
        return title_element[0].strip() if title_element else None

    @staticmethod
    def extract_meta_description(html_element: HtmlElement) -> str | None:
        """
        Extract description content from the requested webpage.
        Return parsed content.
        - :arg html_element: Lxml HtmlElement.
        """
        description_element: list[str] = html_element.xpath('/html/head/meta[@name="description"]/@content')
        return description_element[0].strip() if description_element else None

    @staticmethod
    def extract_entire_text(html_element: HtmlElement) -> str | None:
        """
        Extract body from HtmlElement.
        Return entire text from all nodes on success.
        - :arg html_element: Lxml HtmlElement
        """
        body: list[HtmlElement] = html_element.xpath('/html/body')
        if len(body) == 0:
            return None
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
        cleaned_body: HtmlElement = cleaner.clean_html(body[0])
        body_text: str = tostring(cleaned_body).decode('utf-8')
        content: str = html2text.html2text(body_text)
        return content
