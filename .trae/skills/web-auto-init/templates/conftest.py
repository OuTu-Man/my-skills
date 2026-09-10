import os
from datetime import datetime
from pathlib import Path
from typing import List

import pytest
from _pytest.mark import Mark
from _pytest.python import Function
from _pytest.runner import CallInfo
from loguru import logger

from common.logger import init_logger
from common.use_yaml import UseYaml


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="staging")
    parser.addoption("--platform", action="store", default="web")
    parser.addoption("--browser_type", action="store", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)


def pytest_configure():
    """pytest global vars"""
    pytest.project_code = "AT"
    pytest.my_start_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    pytest.my_init_env = False
    pytest.my_init_data_path = False
    pytest.my_init_report_path = False


@pytest.fixture(scope="session", autouse=True)
def init_env(request):
    if not pytest.my_init_env:
        env_name = request.config.getoption("--env")
        init_logger(env_name, pytest.my_start_datetime)  # init logger
        logger.debug(f"Test env: {env_name}")

        # init host data
        env_file = Path.cwd() / Path("configs") / str(env_name) / Path("hosts.yaml")
        host_data = UseYaml.read_yaml(env_file)
        os.environ.update(host_data)

        pytest.my_init_env = True


@pytest.fixture(scope="session", autouse=True)
def init_data_path(request):
    if not pytest.my_init_data_path:
        data_path = "test_resource/data"
        objects_path = "test_resource/objects"

        # init data path
        os.environ.update({"test_data_path": data_path, "test_pages_objects_path": objects_path})
        logger.debug(f"test data path: {data_path}")
        logger.debug(f"test pages objects path: {objects_path}")

        pytest.my_init_data_path = True


@pytest.fixture(scope="session", autouse=True)
def init_report_path(request):
    if not pytest.my_init_report_path:
        env_name = request.config.getoption("--env")
        _report_path = f"logs/{env_name}_{pytest.my_start_datetime}"
        os.makedirs(name=_report_path, mode=0o777, exist_ok=True)
        os.environ["test_report_path"] = _report_path
        os.environ.update({"test_report_path": _report_path, "start_datetime": pytest.my_start_datetime})
        logger.debug(f"the report path: {_report_path}")

        pytest.my_init_report_path = True


# Hooks
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Function, call: CallInfo):
    """
    pytest_runtest_makereport 是 pytest 框架中一个核心的钩子函数 (Hook Function),
        它的主要作用是在测试用例执行的各个阶段(setup, call, teardown)被调用,
        用于生成并返回一个包含该阶段执行结果的 TestReport 对象

    调用次数: 对于每一个测试用例, 这个钩子函数会被调用 3 次:
      第一次: setup 阶段完成后.
      第二次: 测试用例本身 (call) 执行完成后.
      第三次: teardown 阶段完成后.

    主要参数: 它接收两个关键参数:
      item: 代表当前的测试用例, 包含其名称、所属模块、文档字符串等信息.
      call: 代表当前执行阶段的信息, 如果执行出错, 其 excinfo 属性会包含异常详情.

    返回对象: 它返回一个 TestReport 对象, 其中包含了你非常关心的测试结果信息:
      nodeid: 测试用例的唯一标识符.
      outcome: 执行结果, 如 'passed', 'failed', 'skipped'.
      when: 当前阶段, 如 'setup', 'call', 'teardown'.
      duration: 该阶段的执行耗时.
      longrepr: 失败时的详细错误信息和堆栈跟踪.
      sections: 测试过程中捕获的 stdout/stderr 输出.
    """
    if call.when == "setup" and os.environ.get("PYTEST_XDIST_WORKER"):
        makers: List[Mark] = item.own_markers
        for maker in makers:
            if f"{pytest.project_code}-" in maker.name:
                item.name = maker.name + "::" + item.name

    outcome = yield
    report = outcome.get_result()
    if os.environ.get("PYTEST_XDIST_WORKER"):
        setattr(report, "nodeid", item.nodeid)
    else:
        setattr(report, "nodeid", item.name)
