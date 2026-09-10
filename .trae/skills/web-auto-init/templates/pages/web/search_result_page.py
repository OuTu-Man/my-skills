from loguru import logger

from pages.web.common_page import CommonPage


class SearchResultPage(CommonPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_name = "search_result"

    @property
    def result_links(self):
        return "a[href]"

    def assert_keyword_visible(self, keyword: str):
        page_content = self.page.content()
        assert keyword in page_content, f"Expected keyword '{keyword}' in page content, but not found."
        logger.info(f"keyword assertion passed: {keyword}")
        return True

    def get_first_result_title(self):
        first_result = self.find(self.result_links).first
        title = first_result.inner_text()
        logger.info(f"first result title: {title}")
        return title
