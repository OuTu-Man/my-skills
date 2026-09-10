import importlib
import os

import pytest
import yaml
from _pytest.fixtures import FixtureRequest, fixture
from playwright.sync_api import Page, sync_playwright
from pytest_bdd.parser import Feature, Scenario


@fixture(scope="session", autouse=True)
def global_data(request: FixtureRequest):
    # Create a global cache data
    g = dict()
    return g


@fixture(scope="session", autouse=True)
def take_screenshot(request: FixtureRequest, global_data: dict):
    pass


# hooks
@pytest.fixture
def browser(request: FixtureRequest):
    browser_type = request.config.getoption("browser_type", "chrome")
    browser_type = browser_type.lower()
    headless = request.config.getoption("headless", False)
    p = sync_playwright().start()
    if browser_type == "chrome":
        _brower = p.chromium.launch(headless=headless, args=["--start-maximized"])
    elif browser_type == "firefox":
        _brower = p.firefox.launch(headless=headless, args=["--start-maximized"])
    elif browser_type == "safari":
        _brower = p.webkit.launch(headless=headless, args=["--start-maximized"])
    else:
        raise ValueError(f"only suport the 'Chrome, Firefox, Safari', not suport '{browser_type}'")

    browser = _brower.new_context(no_viewport=True)
    yield browser
    browser.close()


def pytest_bdd_before_scenario(request: FixtureRequest, feature: Feature, scenario: Scenario):
    project_code = pytest.project_code
    env = request.config.getoption("env")
    platform = request.config.getoption("platform")
    browser_type = request.config.getoption("browser_type")
    headless = request.config.getoption("headless", False)
    global_data = request.getfixturevalue("global_data")
    test_name = os.environ.get("PYTEST_CURRENT_TEST") or getattr(
        getattr(request, "node", None), "nodeid", "unknown_test"
    )
    node_id = getattr(getattr(request, "node", None), "nodeid", test_name)
    global_data[test_name] = dict()
    global_data[node_id] = global_data[test_name]
    test_data = dict()

    # get test cases' tags
    case_id = f"{project_code}-unknown"
    tags = scenario.tags
    for tag in tags:
        if f"{project_code}-" in tag:
            case_id = tag

    # get the test data
    feature_data: str = feature.name.lower()
    feature_name: str = feature_data.split("_")[0]
    global_data["test_page_name"] = feature_data
    test_data_path = os.environ.get("test_data_path", "test_resource/data")
    td_file_path = test_data_path + feature_name + "/" + feature_data + "_data.yaml"
    if os.path.isfile(td_file_path):
        test_data = yaml.safe_load(open(td_file_path))
        if case_id not in test_data.keys():
            test_data[case_id] = dict()
        else:
            test_data[case_id] = dict()

    playwright = sync_playwright().start()
    if browser_type.lower() == "chrome":
        _brower = playwright.chromium.launch(headless=headless, args=["--start-maximized"])
    elif browser_type.lower() == "firefox":
        _brower = playwright.firefox.launch(headless=headless, args=["--start-maximized"])
    elif browser_type.lower() == "safari":
        _brower = playwright.webkit.launch(headless=headless, args=["--start-maximized"])
    else:
        raise ValueError(f"only suport the 'Chrome, Firefox, Safari', not suport '{browser_type}'")

    context = _brower.new_context(no_viewport=True)
    page: Page = context.new_page()

    package_name = f"pages.{platform}"
    p = importlib.import_module(name=package_name)
    Pages = p.__getattribute__("Pages")
    pages = Pages(page=page, env=env, test_data=test_data.get(case_id, {}))

    temp = {
        "env": env,
        "platform": platform,
        "browser": _brower,
        "page": page,
        "pages": pages,
        "playwright": playwright,
    }
    global_data.setdefault(test_name, {}).update(temp)
    global_data.setdefault(node_id, {}).update(temp)


def pytest_bdd_after_scenario(request: FixtureRequest, feature: Feature, scenario: Scenario):
    global_data = request.getfixturevalue("global_data")
    test_name = os.environ.get("PYTEST_CURRENT_TEST") or getattr(
        getattr(request, "node", None), "nodeid", "unknown_test"
    )

    scenario_data = global_data.get(
        test_name, global_data.get(getattr(getattr(request, "node", None), "nodeid", test_name), {})
    )
    browser = scenario_data.get("browser", None)
    playwright = scenario_data.get("playwright", None)

    if browser is not None:
        try:
            browser.close()
        except Exception:
            pass
    if playwright is not None:
        try:
            playwright.stop()
        except Exception:
            pass
    global_data.pop(test_name, None)
    global_data.pop(getattr(getattr(request, "node", None), "nodeid", test_name), None)
