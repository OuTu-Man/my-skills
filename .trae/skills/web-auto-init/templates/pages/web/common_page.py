from loguru import logger

from common.utils.tools import Tools
from pages.base_page import BasePage


class CommonPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_name = "common"

    def open_url(self, base_uri: str, uri: str = ""):
        url = base_uri + Tools.convert_text_from_dict(uri, self.test_data)
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle", timeout=15000)
        logger.info(f"open page: {url}")
        return self.page

    def get_page_title(self) -> str:
        title = self.page.title()
        logger.info(f"page title: {title}")
        return title

    def assert_title_contains(self, expected_text: str):
        title = self.get_page_title()
        assert expected_text in title, f"Expected '{expected_text}' in title, but got '{title}'"
        logger.info(f"title assertion passed: '{expected_text}' in '{title}'")
        return title

    def find(self, selector: str):
        return self.page.locator(selector)

    def wait_for_visible(self, selector: str, timeout: int = 30000):
        locator = self.find(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def input_text(self, selector: str, value: str):
        locator = self.wait_for_visible(selector)
        locator.fill(value)
        logger.info(f"input '{value}' into selector: {selector}")
        return locator

    def click(self, selector: str):
        locator = self.wait_for_visible(selector)
        locator.click()
        logger.info(f"click selector: {selector}")
        return locator

    def navigate_to_url(self, base_uri: str, uri: str = ""):
        return self.open_url(base_uri, uri)
