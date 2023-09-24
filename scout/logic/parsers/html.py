from lxml.html.clean import Cleaner
from lxml.html import tostring, HtmlElement



async def sanitize_html(html_element: HtmlElement):
    """
    Utility to clean unsecure HTML.
    """
    cleaner = Cleaner(
        style=True,
        inline_style=True,
        scripts=True,
        javascript=True,
        embedded=True,
        frames=True,
        meta=True,
        annoying_tags=True,
    )
    try:
        sanitized_content = tostring(cleaner.clean_html(html_element))
    except Exception:
        sanitized_content = b''

    return sanitized_content.decode()