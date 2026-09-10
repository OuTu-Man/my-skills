from loguru import logger

from pages.web.common_page import CommonPage


class BaiduPage(CommonPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_name = "baidu"

    @property
    def url(self):
        return "https://www.baidu.com"

    @property
    def search_input(self):
        return 'input[name="wd"]'

    @property
    def search_button(self):
        return "#su"

    def open_home(self):
        self.open_url(self.url)
        logger.info(f"Baidu page opened: {self.url}")
        return self.page

    def get_title(self) -> str:
        return self.get_page_title()

    def assert_home_title(self):
        return self.assert_title_contains("百度一下")

    def search(self, keyword: str):
        self.input_text(self.search_input, keyword)
        self.click(self.search_button)
        logger.info(f"search for keyword: {keyword}")
        return self.page
