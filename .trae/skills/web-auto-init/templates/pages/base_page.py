from time import sleep

from loguru import logger
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page, env: str, test_data: dict, page_name: str = None):
        self.page = page
        self.env = env
        self.test_data = test_data
        self.page_name = page_name

    def wait_seconds(self, seconds: float = 3):
        logger.info(f"wait for {seconds}s")
        sleep(seconds)
