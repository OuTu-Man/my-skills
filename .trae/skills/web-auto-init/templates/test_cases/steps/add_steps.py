import os

from loguru import logger
from pytest import fixture
from pytest_bdd import when

from pages.web import WebPages


@fixture(scope="function")
def scenario_pages(global_data, request):
    current_test = os.environ.get("PYTEST_CURRENT_TEST") or request.node.nodeid
    node_id = request.node.nodeid
    pages: WebPages = global_data.get(current_test, {}).get("pages") or global_data.get(node_id, {}).get("pages")
    if pages is None:
        raise KeyError(f"No page data for scenario: {current_test} / {node_id}")
    return pages


@when("the user navigates to baidu")
def click_and_go_to_target_page(scenario_pages: WebPages):
    baidu_page = scenario_pages.baidu_page
    baidu_page.open_home()
    baidu_page.wait_seconds(1)
    baidu_page.assert_home_title()
