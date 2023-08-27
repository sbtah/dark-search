from lxml.html import HtmlElement, HTMLParser, fromstring
from typing import List, Union
from utilities.logging import logger


class HtmlExtractor:
    """
    Html extractor built with lxml.
    Extract needed values/data from received HtmlElement.
    """

    def __init__(self, html_element):
        if isinstance(html_element, HtmlElement):
            self.element = html_element
        else:
            raise ValueError(f'HtmlExtractor Error. Wrong object to parse, received type: {type(html_element)}')
        self.logger = logger

    def find_element(
            self,
            html_element: HtmlElement,
            xpath_to_search: str,
            ignore_not_found_errors: bool = False,
    ) -> Union[HtmlElement, None]:
        """
        Needs lxml's HtmlElement as an argument.
        Returns single element/value by Xpath on provided HtmlElement.
        Returns searched value.

        - :arg ignore_not_found_errors:
            - Can be set to True to not produce error logs,
                when elements are not found.
        - :arg html_element: Lxml HtmlElement to process.
        - :arg xpath_to_search:
        """
        if isinstance(html_element, HtmlElement):
            try:
                element = html_element.xpath(xpath_to_search)[0]
                self.logger.debug(
                    f'(find_element) Successfully returned an element.'
                )
                return element
            except IndexError:
                if ignore_not_found_errors:
                    return None
                else:
                    self.logger.error(
                        '(find_element) Returned an empty list.',
                    )
                    return None
            except Exception as e:
                self.logger.error(f'(find_element) Some other Exception: {e}')
                return None
        else:
            self.logger.error(f'(find_element) Element received is not of type HtmlElement.') # noqa
            return None

    def find_all_elements(
            self,
            html_element: HtmlElement,
            xpath_to_search: str,
            ignore_not_found_errors: bool = False,
    ) -> Union[List[HtmlElement], None]:
        """
        Needs lxml's HtmlElement as an argument.
        Finds elements by Xpath on given Element.
        Returns lists of HtmlElements for further processing.

        - :arg html_element: Lxml HtmlElement to process.
        - :arg xpath_to_search: Xpath that leads to desired elements.
        - :arg ignore_not_found_errors:
            - Can be set to True to not produce error logs,
                when elements are not found.
        """
        if isinstance(html_element, HtmlElement):
            try:
                elements_list = html_element.xpath(xpath_to_search)
                if elements_list:
                    self.logger.debug(
                        f'(find_all_elements) Successfully returned: {len(elements_list)} elements.'  # noqa
                    )
                    return elements_list
                else:
                    if ignore_not_found_errors:
                        return None
                    else:
                        self.logger.error(
                            '(find_all_elements) Returned an empty list.',
                        )
                        return None
            except Exception as e:
                self.logger.error(
                    f'(find_all_elements) Some other Exception: {e}'
                )
                return None
        else:
            self.logger.error(
                f'(find_all_elements) Element received is not of type HtmlElement.'  # noqa
            )
            return None

    def if_xpath_in_element(
            self,
            html_element: HtmlElement,
            xpath_to_search: str
    ) -> Union[bool, None]:
        """
        Needs lxml's HtmlElement as an argument.
        Looks for single! object within provided HTMLElement.
        Returns True is successful.

        - :arg html_element: Lxml HtmlElement to process.
        - :arg xpath_to_search: Xpath that leads to desired elements.
        """
        if isinstance(html_element, HtmlElement):
            assert len(html_element.xpath(xpath_to_search)) < 2, self.logger.error(
                '(if_xpath_in_element) Returned more then 1 element.'
            )
            try:
                html_element.xpath(xpath_to_search)[0]
                self.logger.debug(
                    f'(if_xpath_in_element) Found an element. Returning - True.' # noqa
                )
                return True
            except IndexError:
                self.logger.debug(
                    f'(if_xpath_in_element) Search for: (\'{xpath_to_search}\') returned an empty list.'  # noqa
                )
                return None
            except Exception as e:
                self.logger.error(f'(if_xpath_in_element), Exception: {e}')
                return None
        else:
            self.logger.error(
                '(if_xpath_in_element) Element received is not of type HtmlElement.'  # noqa
            )
            return None
