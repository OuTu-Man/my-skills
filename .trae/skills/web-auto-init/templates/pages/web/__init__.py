from pages.web.baidu_page import BaiduPage
from pages.web.common_page import CommonPage
from pages.web.search_result_page import SearchResultPage


class WebPages:
    def __init__(self, *args, **kwargs):
        self.common_page = CommonPage(*args, **kwargs)
        self.baidu_page = BaiduPage(*args, **kwargs)
        self.search_result_page = SearchResultPage(*args, **kwargs)


Pages = WebPages
