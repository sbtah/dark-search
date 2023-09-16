from .html_parser import ParsedHTML


def is_html(parsed: ParsedHTML) -> bool:
    return len(parsed.tags) != 0
