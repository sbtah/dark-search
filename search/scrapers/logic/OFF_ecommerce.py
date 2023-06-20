from typing import Callable, Dict, Iterator, List, Union

from lxml.html import HtmlElement
from selenium.webdriver.remote.webelement import WebElement

from scrapers.logic.base_scraper.base import BaseSeleniumScraper


class EcommerceSeleniumScraper(BaseSeleniumScraper):
    """
    General Ecommerce scraper.
    """

    def __init__(self, requested_url, store_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requested_url = requested_url
        self.store_url = store_url

    @property
    def cookies_close_xpath(self) -> str:
        """Xpath to element that closes cookies policy banner on click."""
        raise NotImplementedError

    @property
    def store_picked_xpath(self) -> str:
        """
        Xpath to element that will return text value,
        for currently picked Local Store.
        """
        raise NotImplementedError

    def categories_discovery_map(self) -> dict:
        """
        Dictionary that will map Categories structure of store.

        - :category_xpath:
        Xpath that returns list of Category HtmlElements or Webelements.
        - :category_parser: Callable that will extract
        'url', 'name' and 'category_id' for Category
        - :has_children:
        True if Category have child Categories.
        - :has_products:
        True if Category have products to scrape.
        - :use_webelements: If set to True we will return Category elements as
        Selenium's Webelements. Otherwise, we will work on HtmlElements.

        Should return dict with schema like:
        {
            0: {
                "category_xpath": str,
                "category_parser": callable,
                "has_children": bool,
                "has_products": bool,
                "use_webelements": bool,
            },
        }

        Where Keys 0 - 2 implies Category level.
        """
        raise NotImplementedError

    def products_discovery_map(self) -> dict:
        """
        Dictionary that will map Products structure of store.

        - :product_xpath:
        Xpath that returns list of Product HtmlElements or Webelements.
        - :product_parser:
        Callable that will extract 'url', 'name' and 'product_id' for Product.
        - :use_webelements: If set to True we will return Product elements as
        Selenium's Webelements, otherwise we will work on HtmlElements.

        Should return dict with schema like:
        {
            0: {
                "product_xpath": str,
                "product_parser": callable,
                "product_current_page_xpath": str,
                "product_next_page_button_xpath": str,
                "product_last_page_xpath": str,
                "use_webelements": bool,
            },
        }

        Where Keys 0 - 2 implies Category level.
        If for example Products are only on Categories level 3.
        Then we define dictionary with key: "3".
        """
        raise NotImplementedError

    def pick_local_store_by_name(
            self,
            store_name: str,
            html_element: HtmlElement
    ) -> bool:
        """
        Searches for element that is used to pick local store.
        Properly pick local store.
        Should return True on success and False on fail.
        Needs to be implemented on specific store SeleniumScraper level.

        - :arg store_name: string representing Local Store name.
        - :arg html_element: Lxml HtmlElement to process.
        """
        raise NotImplementedError

    def visit_page(self, url: str) -> HtmlElement:
        """
        Entrypoint for all scraping logic.
        Visits requested page by url.
        Since we don't store session or cookies,
        each time with have to close cookies banner.
        Returns HtmlElement generated after banner was closed.
        """
        try:
            request = self.selenium_get(url=url)
            if request is not None:
                element = self.generate_html_element()
                self.close_cookies_banner(html_element=element)
                after_element = self.generate_html_element()
                return after_element
            else:
                self.logger.error('Failed at requesting page URL.')
                raise ValueError
        except Exception as e:
            self.logger.error(f'(visit_page) Some other Exception: {e}')
            raise

    def close_cookies_banner(self, html_element: HtmlElement) -> None:
        """
        Finds Cookies Policy in provided HtmlElement and closes it.
        Needs self.cookies_close_xpath to work.
        """
        try:
            self.find_and_click_selenium_element(
                html_element=html_element,
                xpath_to_search=self.cookies_close_xpath,
            )
            self.logger.info('Closing the cookies banner step has been successfully completed')  # noqa
        except Exception as e:
            self.logger.error(
                f'(close_cookies_banner) Some other Exception: {e}'
            )

    def get_current_store(
            self,
            html_element: HtmlElement,
    ) -> Union[str, None]:
        """
        Returns text value for currently picked Local Store.

        - :arg html_element: Lxml HtmlElement to process.
        """
        try:
            store = self.find_element(
                html_element=html_element,
                xpath_to_search=self.store_picked_xpath,
            )
            self.logger.info(
                f'Successfully returned a store element: {store}'
            )
            return store
        except Exception as e:
            self.logger.error(f'(get_current_store) Some other Exception: {e}')
            raise

    def validate_store_picked(self, store_name: str) -> bool:
        """
        Validates value of chosen store,
        with current value of Local Store on site.
        Returns True on success.
        """
        element = self.generate_html_element()
        current_store = self.get_current_store(html_element=element)
        if current_store:
            if current_store == store_name:
                self.logger.info(
                    f'Validation of Local Store successful: Current Store:{current_store} ; Chosen Store: {store_name}'
                )
                return True
            else:
                return False
        else:
            self.logger.error(
                f'(validate_store_picked) Failed at getting Store name value, Received: {current_store}'
            )
            return False

    def find_categories_data(
            self,
            category_level: int,
            html_element: HtmlElement,
    ) -> Union[Iterator[Dict], None]:
        """
        Looks for Category Elements in given HtmlElement.
        Return generator of dictionaries with Category data..

        - :arg category_level:
            Level of Category, used to get data from categories_map.
        - :arg html_element: Lxml HtmlElement to process.
        """
        self.logger.info(
            f"Discovery process for Categories of level: {category_level} started."  # noqa
        )
        # Get category map.
        categories_map = self.categories_discovery_map()
        # Get list of Webelements or HtmlElements.
        elements_type = categories_map[category_level]['use_webelements']
        if elements_type is True:
            # Using Webelements.
            self.logger.info('Looking for Webelements for Categories.')
            categories_elements_list = self.find_selenium_elements(
                xpath_to_search=categories_map[category_level]['category_xpath'],  # noqa
            )
        elif elements_type is False:
            # Or HtmlElements.
            self.logger.info('Looking for HtmlElements for Categories.')
            categories_elements_list = self.find_all_elements(
                html_element=html_element,
                xpath_to_search=categories_map[category_level]['category_xpath'],  # noqa
            )
        else:
            self.logger.error(
                '(find_categories_data) Error while getting \'use_webelements\'. Quiting.'  # noqa
            )
            raise ValueError
        if categories_elements_list:
            self.logger.info(
                f'Successfully found: {len(categories_elements_list)} Categories elements. Processing.'  # noqa
            )
            return self.prepare_categories_discovery_data(
                list_of_elements=categories_elements_list,
                custom_parser=categories_map[category_level]['category_parser'],  # noqa
                has_children=categories_map[category_level]['has_children'],
                has_products=categories_map[category_level]['has_products'],
            )
        else:
            self.logger.error(
                f'Searching for Category elements failed. Quiting.'
            )
            raise ValueError

    def find_products_data(
            self,
            category_level: int,
            html_element: HtmlElement,
            products_mapper: Callable = None,
    ) -> Iterator[dict]:
        """
        Looks for Products Elements in given HtmlElement.
        Return generator of dictionaries with Product data.

        - :arg category_level:
            Level of Category, used to get data from products_map that relates
            Products to Category by level.
        - :arg html_element: Lxml HtmlElement to process.
        """
        self.logger.info(
            f'Starting discovery process for Products on Category page: {self.current_url}'  # noqa
        )
        # Here we check if Products map is provided from other method.
        if products_mapper is None:
            products_map = self.products_discovery_map()
        else:
            products_map = products_mapper

        if category_level not in set(products_map.keys()):
            self.logger.error(
                f'The Product map does not contain a category level: {category_level}'  # noqa
            )
            raise ValueError
        else:
            elements_type = products_map[category_level]['use_webelements']
            if elements_type is True:
                # Using Webelements.
                self.logger.info('Looking for Webelements for Products.')
                products_elements_list = self.find_selenium_elements(
                    xpath_to_search=products_map[category_level]['product_xpath'],  # noqa
                )
            elif elements_type is False:
                # Or HtmlElements.
                self.logger.info('Looking for HtmlElements for Products.')
                products_elements_list = self.find_all_elements(
                    html_element=html_element,
                    xpath_to_search=products_map[category_level]['product_xpath'],  # noqa
                )
            else:
                self.logger.error(
                    '(find_products_data) Error while getting \'use_webelements\'. Quiting.'  # noqa
                )
                raise ValueError

        if products_elements_list:
            self.logger.info(
                f'Successfully found: {len(products_elements_list)} Products elements. Processing.'  # noqa
            )
            return self.prepare_products_discovery_data(
                list_of_elements=products_elements_list,
                custom_parser=products_map[category_level]['product_parser'],  # noqa
            )
        else:
            self.logger.error(
                f'Searching for Product elements failed. Quiting.'
            )
            raise ValueError

    def prepare_categories_discovery_data(
            self,
            list_of_elements: List[Union[WebElement, HtmlElement]],
            custom_parser: Callable,
            has_children: bool,
            has_products: bool,
    ) -> Iterator[Dict]:
        """
        Takes list of HtmlElements or Webelements
        and returns generator of dictionaries with prepared data containing:
        urls, names, has_children, has_products for found Categories.

        - :arg list_of_elements:
        List of HtmlElements or Selenium Webelement to process.

        - :arg custom_parser:
        Method that will be used to extract 'url', 'name'
        from single given element.
        Should return dict with,
        "url": value_for_url, "name": value_for_name,

        - :arg has_children: True or False, should be set in:
        categories_discovery_map property.

        - :arg has_products: True or False, should be set in:
        categories_discovery_map property.
        """
        if isinstance(list_of_elements, list):
            assert len(list_of_elements) > 0, 'Received an empty list, Nothing to extract.'  # noqa
            try:
                return ({**custom_parser(element), 'has_children': has_children, 'has_products': has_products} for
                        element in list_of_elements)  # noqa
            except Exception as e:
                self.logger.error(
                    f'(prepare_categories_discovery_data) Some other exception: {e}'  # noqa
                )
                raise
        else:
            self.logger.error(
                f'(prepare_categories_discovery_data) Argument received for list of elements should be of type list. Received: {type(list_of_elements)}' # noqa
            )
            raise TypeError

    def prepare_products_discovery_data(
            self,
            list_of_elements: List[Union[WebElement, HtmlElement]],
            custom_parser: Callable,
    ) -> Iterator[Dict]:
        """
        Takes list of HtmlElements or Webelements
        and returns generator of dictionaries with prepared data containing:
            urls, names, scraped_id for found Products.

        - :arg list_of_elements:
            List of HtmlElements or Selenium Webelement to process.
        - :arg custom_parser:
            Method that will be used to extract 'url', 'name' and 'product_id',
            from single given element.
            Should return dict with,
            "url": value_for_url, "name": value_for_name,
            "product_id": value_for_name.
        """
        if isinstance(list_of_elements, list):
            assert len(list_of_elements) > 0, 'Received an empty list, Nothing to extract.'  # noqa
            try:
                return ({**custom_parser(element)} for element in list_of_elements)  # noqa
            except Exception as e:
                self.logger.error(
                    f'(prepare_products_discovery_data) Some other exception: {e}'  # noqa
                )
                raise
        else:
            self.logger.error(
                f'(prepare_products_discovery_data) Argument received for list of elements should be of type list. Received: {type(list_of_elements)}' # noqa
            )
            raise TypeError

    def find_all_products_data(
            self, category_level=1,
    ) -> Iterator[dict]:
        """
        Parses all products for all pages on specified ProductPage.
        Relies on Selenium since it's only clicking next page button.
        """

        self.logger.info(f'Products discovery Process for Category level: {category_level} started.')  # noqa
        current_page = 1
        products_map = self.products_discovery_map()
        element = self.generate_html_element()

        current_page_number_from_xpath = self.find_element(
            html_element=element,
            xpath_to_search=products_map[category_level]['product_current_page_xpath'],  # noqa
            ignore_not_found_errors=True,
        )
        last_page_number_from_xpath = self.find_element(
            html_element=element,
            xpath_to_search=products_map[category_level]['product_last_page_xpath'],
            ignore_not_found_errors=True,
        )
        self.logger.info(
            f'Current page; XPath: {current_page_number_from_xpath if current_page_number_from_xpath is not None else 1}, Counted: {current_page}, Total Pages: {last_page_number_from_xpath if last_page_number_from_xpath is not None else 1}' # noqa
        )

        products = self.find_products_data(
            html_element=element,
            category_level=category_level,
            products_mapper=products_map
        )

        if products is not None:
            for prod in products:
                yield prod
        else:
            self.logger.error(
                f'(find_all_products_data) Returned: \'{products}\' Products at URL: {self.current_url} - Quiting.'
            )
            pass

        next_page_button = self.find_selenium_element(
            # Next Page Xpath
            xpath_to_search=products_map[category_level]['product_next_page_button_xpath'],  # noqa
            ignore_not_found_errors=True,
        )
        while next_page_button is not None:

            self.logger.info(f'Found another product page, proceeding.')
            self.initialize_html_element(selenium_element=next_page_button)
            next_page_button = self.find_selenium_element(
                # Next Page Xpath
                xpath_to_search=products_map[category_level]['product_next_page_button_xpath'],  # noqa
                ignore_not_found_errors=True,
            )
            current_page += 1
            new_element = self.generate_html_element()
            current_page_number_from_xpath = self.find_element(
                html_element=new_element,
                # Current Page Xpath
                xpath_to_search=products_map[category_level]['product_current_page_xpath'],  # noqa
                ignore_not_found_errors=True,
            )
            self.logger.info(
                f'Current page; XPath: {current_page_number_from_xpath if current_page_number_from_xpath is not None else 1}, Counted: {current_page}, Total Pages: {last_page_number_from_xpath if last_page_number_from_xpath is not None else 1}' # noqa
            )
            products = self.find_products_data(
                html_element=element,
                category_level=category_level,
                products_mapper=products_map,
            )
            if products is not None:
                for prod in products:
                    yield prod
            else:
                self.logger.error(
                    f'(find_all_products_data) Returned: \'{products}\' Products at URL: {self.url} - Quiting.'  # noqa
                )
                pass
        else:
            self.logger.info(
                'Next page element not found. Parsing products - finished.'
            )
