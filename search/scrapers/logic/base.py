import time
from datetime import datetime
from random import choice, randint
from typing import List, Union

from lxml.html import HtmlElement, HTMLParser, fromstring
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotVisibleException,
    NoSuchElementException,
)
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
# Local Testing dependencies
from webdriver_manager.chrome import ChromeDriverManager

from search.options.settings import USER_AGENTS
from search.utilities.logging import logger


class BaseSeleniumScraper:
    """Base scraper class for other specialized scrapers."""

    def __init__(self, proxy='127.0.0.1:9050', *args, **kwargs):
        self._driver = None
        self.teardown = True
        self.logger = logger
        self.proxy = proxy
        self.time_started = datetime.now()

    def __str__(self):
        return 'Base Scraper'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.delete_all_cookies()
            self.driver.quit()

    @property
    def potential_popups_xpath(self) -> List[str]:
        """
        Should return a list of Xpath-ses to can appear on the Website randomly.
        """
        raise NotImplementedError

    @staticmethod
    def get_random_user_agent(user_agent_list: List[str]) -> str:
        """
        Return str with random User-Agent.
        - :arg user_agent_list: List of strings with User Agents.
        """
        agent = choice(user_agent_list)
        return agent

    @staticmethod
    def random_sleep_small() -> None:
        """Custom sleep function that sleeps from 1 to 3 seconds"""
        value = randint(1, 3)
        logger.debug(f'Small sleep for: {value} seconds.')
        return time.sleep(value)

    @staticmethod
    def random_sleep_medium() -> None:
        """Custom sleep function that sleeps from 3 to 6 seconds"""
        value = randint(3, 6)
        logger.debug(f'Medium sleep for: {value} seconds.')
        return time.sleep(value)

    @staticmethod
    def random_sleep_long() -> None:
        """Custom sleep function that sleeps from 6 to 8 seconds"""
        value = randint(6, 8)
        logger.debug(f'Long sleep for: {value} seconds.')
        return time.sleep(value)

    @staticmethod
    def random_sleep_deep() -> None:
        """Custom sleep function that sleeps from 15 to 20 seconds"""
        value = randint(15, 20)
        logger.debug(f'Deep sleep for: {value} seconds')
        return time.sleep(value)

    @staticmethod
    def wait(seconds) -> None:
        """Custom sleep function that sleeps for specified amount of seconds"""
        logger.debug(f'Waiting for: {seconds} seconds.')
        return time.sleep(seconds)

    @property
    def user_agent(self) -> str:
        agent = self.get_random_user_agent(USER_AGENTS)
        return agent

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def driver(self) -> webdriver:

        if self._driver is None:
            options = webdriver.ChromeOptions()

            options.add_argument('--no-sandbox')
            options.add_argument('--single-process')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--incognito')
            options.add_argument('--disable-infobars')
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--start-maximized')

            # TODO:
            # Call get_random_proxy to use different proxy server on each request..
            # self.options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
            options.add_argument(f'--proxy-server=socks5://{self.proxy}')

            # User Agent
            options.add_argument(f'--user-agent={self.user_agent}')

            # Bypass Bot detection
            options.add_experimental_option(
                'excludeSwitches', ['enable-automation'],
            )
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument(
                '--disable-blink-features=AutomationControlled'
            )

            # Remote
            # self._driver = webdriver.Remote(
            #     command_executor='http://comptrends-chrome:4444/wd/hub',
            #     options=options,
            #     desired_capabilities=DesiredCapabilities.CHROME,
            # )

            # Locally installed browser just for testing.
            self._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options,
                desired_capabilities=DesiredCapabilities.CHROME,
            )
            self._driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')  # noqa
            self._driver.set_window_size('2560', '1440')
            self._driver.implicitly_wait(10)

        return self._driver

    def selenium_get(self, url: str) -> Union[bool, None]:
        """
        Requests specified url.
        Returns True on success.

        - :arg url: Requested URL.
        """
        try:
            self.driver.get(url)
            self.logger.info(f'Requesting: {url}')
            self.random_sleep_small()
            return True
        except Exception as e:
            self.logger.error(f'(selenium_get) Exception: {e}')
            return None

    def generate_html_element(self) -> Union[HtmlElement, None]:
        """
        Parses current page source and produces a HTMLElement from it.
        """
        try:
            hp = HTMLParser(encoding='utf-8')
            element = fromstring(
                self.driver.page_source,
                parser=hp,
            )
            self.logger.debug(
                f'Parsing page source to HtmlElement at: {self.driver.current_url}'  # noqa
            )
            return element
        except Exception as e:
            self.logger.error(f'Exception while generating HtmlElement: {e}')
            return None

    def quit_and_clean(self) -> None:
        """
        Deletes all cookies and quits Selenium driver.
        """
        if self._driver:
            self.driver.delete_all_cookies()
            self.driver.quit()
            self._driver = None
            self.logger.info('Driver exited, cookies deleted.')
        else:
            self.logger.info('Driver was already closed.')

    def click(self, selenium_element: WebElement) -> None:
        """
        Takes Selenium Webelement as an input and clicks on it.

        - :arg selenium_element: Located Webelement to click on.
        """
        actions = ActionChains(self._driver)
        try:
            actions.click(selenium_element).perform()
            self.logger.debug(
                f'Successfully clicked on desired element.',
            )
        except Exception as e:
            self.logger.error(
                f'(click) Some other exception: {e}',
            )

    def move_to_element(self, selenium_element: WebElement) -> None:
        """
        Takes Selenium Element as an input. Moves to this element.

        - :arg selenium_element: Located Webelement to scroll to.
        """
        actions = ActionChains(self._driver)
        try:
            actions.move_to_element(selenium_element).perform()
            self.logger.debug(
                f'Successfully moved to desired element.',
            )
        except Exception as e:
            self.logger.error(
                f'(move_to_element) Some other exception: {e}',
            )

    def scroll_to_element(self, selenium_element: WebElement) -> None:
        """
        Scrolls to element that is outside the viewport.
        - :arg selenium_element: Located Webelement to scroll to.
        """
        actions = ActionChains(self._driver)
        try:
            actions.scroll_to_element(selenium_element).perform()
            self.logger.debug(
                f'Successfully scrolled to desired element.',
            )
        except Exception as e:
            self.logger.error(
                f'(scroll_to_element) Some other exception: {e}',
            )

    def move_and_click(self, selenium_element: WebElement) -> None:
        """
        Moves pointer to Selenium element and clicks it after a break.
        Waits after successful click.

        - :arg selenium_element: Located Webelement to move to.
        """
        self.move_to_element(selenium_element=selenium_element)
        self.random_sleep_small()
        self.click(selenium_element)
        self.logger.info(
            'Successfully moved and clicked on specified element.'
        )
        self.random_sleep_medium()

    def find_selenium_element(
            self,
            xpath_to_search: str,
            ignore_not_found_errors: bool = False,
            wait: int = 3,
    ) -> Union[WebElement, None]:
        """
        Used with Selenium driver.
        Finds element by specified Xpath.
        Returns Selenium WebElement to interact with.

        - :arg xpath_to_search: Xpath that leads to desired element.
        - :arg ignore_not_found_errors:
            Can be set to True to not produce error logs,
            when element is not found.
        - :arg wait: Seconds to wait until the element is present.
            Default value is: 2 seconds.
        """
        try:
            self.logger.debug(
                f'(find_selenium_element) Looking for WebElement, waiting {wait} seconds.'  # noqa
            )
            self.wait(seconds=wait)
            element = self.driver.find_element(By.XPATH, xpath_to_search)
            self.logger.debug(
                f'(find_selenium_element) Successfully returned an element.'  # noqa
            )
            return element
        except ElementNotVisibleException:
            self.logger.error(f'Selenium element not visible')
            return None
        except NoSuchElementException:
            if ignore_not_found_errors:
                return None
            else:
                self.logger.error(
                    f'(find_selenium_element) Selenium element not found. Is the Xpath ok?'  # noqa
                )
                return None
        except Exception as e:
            self.logger.error(
                f'(find_selenium_element) Some other exception: {e}'
            )
            return None

    def find_selenium_select_element(
            self,
            xpath_to_search: str,
    ) -> Union[WebElement, None]:
        """
        Used with Selenium driver.
        Looks for 'select' (drop-down) element by Xpath.
        Returns element to interact with.

        - :arg xpath_to_search: Xpath that leads to desired Select element.
        """
        try:
            select_element = Select(
                self.find_selenium_element(
                    xpath_to_search=xpath_to_search,
                )
            )
            self.logger.info(
                f'Found select element. Returning...'
            )
            return select_element
        except Exception as e:
            self.logger.error(
                f'(find_selenium_select_element) Some other exception: {e}'
            )
            return None

    def find_selenium_elements(
            self,
            xpath_to_search: str,
            ignore_not_found_errors: bool = False,
            wait: int = 3,
    ) -> Union[List[WebElement], None]:
        """
        Used with Selenium driver.
        Finds elements by specified Xpath.
        Return Selenium web elements to interact with.

        - :arg xpath_to_search: Xpath that leads to desired elements.
        - :arg ignore_not_found_errors:
            Can be set to True to not produce error logs,
            when elements are not found.
        - :arg wait: Seconds to wait until the element is present.
            Default value is: 2 seconds.
        """
        try:
            self.logger.debug(
                f'(find_selenium_elements) Looking for elements, waiting {wait} seconds.'  # noqa
            )
            self.wait(seconds=wait)
            elements = self.driver.find_elements(
                By.XPATH,
                xpath_to_search,
            )
            self.logger.debug(
                f'(find_selenium_elements) Successfully returned: {len(elements)} elements.'  # noqa
            )
            return elements
        except ElementNotVisibleException:
            self.logger.error(f'Selenium element not visible.')
            return None
        except NoSuchElementException:
            if ignore_not_found_errors:
                return None
            else:
                self.logger.error(
                    f'(find_selenium_elements) Selenium elements not found. Is the Xpath ok?'  # noqa
                )
                return None
        except Exception as e:
            self.logger.error(
                f'(find_selenium_element) Some other Exception: {e}'
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

    def initialize_html_element(
            self,
            selenium_element: WebElement
    ) -> Union[bool, None]:
        """
        Used with Selenium driver.
        Initialize a part of content that is loaded on click.

        - :arg selenium_element:
            WebElement to initialize/click to load some content.
        """
        if isinstance(selenium_element, WebElement):
            try:
                self.move_and_click(selenium_element=selenium_element)
                return True
            except NoSuchElementException:
                self.logger.error(
                    'Failed at finding element to click. Maybe element was already clicked?'  # noqa
                )
                return None
            except ElementClickInterceptedException:
                # Sometimes a random popup may appear and intercept our click attempt.
                # We are checking for known Xpathses of those elements and we are closing them.
                self.logger.error(
                    f'Failed at clicking element - interception detected. Trying known popups Xpathses...'  # noqa
                )
                try:
                    self.close_popups_elements_on_error(
                        xpathses_to_search=self.potenial_popups_xpaths
                    )
                    self.move_and_click(selenium_element=selenium_element)
                    return True
                except Exception as ee:
                    self.logger.error(
                        f'(initialize_html_element: ElementClickInterceptedException check) Some other exception: {ee}'
                        # noqa
                    )
                    return None
            except ElementNotVisibleException:
                self.logger.error(
                    'Element is not visible.'
                )
                return None
            except Exception as e:
                self.logger.error(
                    f'(initialize_html_element) Some other Exception: {e}',
                )
                return None
        else:
            self.logger.error(
                'Element is not instance of Selenium\'s Webelement.'
            )
            return None

    def send_text_to_element(
            self,
            text: str,
            selenium_element: WebElement
    ) -> Union[bool, None]:
        """
        Takes Selenium Element as an input, sends specified text to it.
        Returns True on success.

        - :arg selenium_element: WebElement to send text to.
        - :arg text: Text to send.
        """
        if isinstance(selenium_element, WebElement):
            try:
                self.move_and_click(selenium_element=selenium_element)
                selenium_element.clear()
                selenium_element.send_keys(text)
                selenium_element.send_keys(Keys.ENTER)
                self.random_sleep_small()
                self.logger.info(
                    f'Successfully sent text: \'{text}\' to desired element.',
                )
                return True
            except ElementClickInterceptedException:
                self.logger.error(
                    'Interaction with specified element was intercepted.'
                )
                self.close_popups_elements_on_error(
                    xpathses_to_search=self.potenial_popups_xpaths
                )
                try:
                    selenium_element.clear()
                    selenium_element.send_keys(text)
                    selenium_element.send_keys(Keys.ENTER)
                    self.random_sleep_small()
                    self.logger.info(
                        f'Successfully sent text: \'{text}\' to desired element.',  # noqa
                    )
                    return True
                except Exception as ee:
                    self.logger.error(
                        f'(send_text_to_element: ElementClickInterceptedException check) Some other exception: {ee}'
                        # noqa
                    )
                    return None
            except ElementNotVisibleException:
                self.logger.error('Specified element is not visible.')
                return None
            except Exception as e:
                self.logger.error(
                    f'(send_text_to_element) Some other exception: {e}',
                )
                return None
        else:
            self.logger.error(
                'Element is not instance of Selenium\'s Webelement.'
            )
            return None

    def find_and_click_selenium_element(
            self,
            html_element: HtmlElement,
            xpath_to_search: str
    ):
        """
        Given the HtmlElement searches for defined Xpath and tries to click it.
        """
        if isinstance(html_element, HtmlElement):
            if_element_in_html = self.if_xpath_in_element(
                html_element=html_element, xpath_to_search=xpath_to_search
            )
            if if_element_in_html:
                self.logger.info('WebElement found, clicking...')
                try:
                    element_click_button = self.find_selenium_element(
                        xpath_to_search=xpath_to_search
                    )
                    initialized = self.initialize_html_element(
                        selenium_element=element_click_button,
                    )
                    if initialized:
                        self.logger.info('Successfully clicked WebElement.')
                    else:
                        self.logger.error('Failed at clicking WebElement.')
                except Exception as e:
                    self.logger.error(
                        f'(find_and_click_selenium_element) Some other exception: {e}'  # noqa
                    )
            else:
                self.logger.info('No WebElement to click, passing...')
        else:
            self.logger.error(
                '(find_and_click_selenium_element) Element received is not of type HtmlElement.'  # noqa
            )
            raise TypeError

    def close_popups_elements_on_error(self) -> None:
        """
        Searches list of knows Xpathses for popup elements.
        If element is found, closes it.
        """
        for xpath in self.potential_popups_xpath:
            element = self.find_selenium_element(
                xpath_to_search=xpath, ignore_not_found_errors=True
            )
            if element is not None:
                self.logger.info('Found critical popup element. Closing.')
                self.move_and_click(selenium_element=element)
            else:
                self.logger.info('No critical popup elements. Passing.')