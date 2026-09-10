# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 沟通语言

与用户沟通一律使用**中文**（见 [AGENT.md](AGENT.md)），代码与命令保持英文。

## 仓库性质

这不是一个应用，而是一个 **uv workspace + Trae 技能集合**：

- [.trae/skills/](.trae/skills/) 存放技能（Skill），[.trae/rules/](.trae/rules/) 存放规则。新增/修改技能时遵循各目录下 `SKILL.md` 的 frontmatter 与正文约定。
  - `web-auto-init`：Web UI 自动化框架脚手架，`templates/` 下是可直接复制的模板，初始化时**逐字读取并写入，不要自行改写模板内容**。
  - `playwright-cli`：浏览器交互式自动化 CLI 用法文档（含 `references/`）。
  - `zentao-cli`：禅道 CLI 用法文档。
- 各测试工程是 workspace 成员，根 [pyproject.toml](pyproject.toml) 的 `[tool.uv.workspace].members` 列出。`token-price-page/` 是当前唯一实际存在的成员；它由 `web-auto-init` 模板生成，是 **Playwright + pytest-bdd** 的 Web UI 自动化框架（POM + BDD）。根目录的 `main.py` 仅为 `uv init` 占位，无实际逻辑。

> 注意：根 `pyproject.toml` 仍列有 `web-demo-*`、`web-verify-*` 等已不存在的成员；在根目录跑 `uv sync` 前需留意，日常命令都在具体成员目录（如 `token-price-page/`）内执行。

## 常用命令（在成员工程目录内，如 token-price-page/）

```bash
uv sync                              # 安装依赖（Python >= 3.14，见 .python-version）
uv run playwright install chromium   # 首次需安装浏览器
uv run pytest -s test_cases/         # 运行全部 BDD 用例
uv run pytest -s test_cases/ -k baidu1          # 按场景名运行单个用例
uv run pytest -s test_cases/ --env staging --platform web --browser_type chrome --headless
make run                             # = uv run pytest -s test_cases/
make formatted                       # black . + ruff check --fix（行宽 120，忽略 E501）
```

pytest 自定义 CLI 参数（在根 `conftest.py` 注册）：`--env`（默认 staging，对应 `configs/<env>/hosts.yaml`）、`--platform`（默认 web，对应 `pages/<platform>/`）、`--browser_type`（chrome/firefox/safari）、`--headless`。

## 框架架构（token-price-page，理解多文件协作的关键）

一次 BDD 场景的完整生命周期：

1. **入口**：[test_cases/test_web.py](token-price-page/test_cases/test_web.py) 用 `scenarios(os.getcwd())` 递归加载所有 `.feature`，并 `from test_cases.steps import *` 注册 step。新增 step 文件要在 [test_cases/steps/__init__.py](token-price-page/test_cases/steps/__init__.py) 中重导出，否则不会被加载。
2. **场景前置钩子** `pytest_bdd_before_scenario`（[test_cases/conftest.py](token-price-page/test_cases/conftest.py)）：
   - 启动 Playwright，按 `--browser_type` 建 browser/context/page；
   - 用 `importlib.import_module(f"pages.{platform}")` **动态加载平台包**并取其 `Pages` 属性实例化所有页面对象，传入 `(page, env, test_data)`；
   - 把 browser/page/pages 等存入 session 级 `global_data` 字典，键为测试名与 nodeid；场景结束的 `pytest_bdd_after_scenario` 负责关闭浏览器并清理该键。
3. **step 取页面对象**：step 通过 `scenario_pages` fixture 从 `global_data` 取出 `WebPages` 实例（`global_data[当前测试]["pages"]`），再访问具体页面，如 `scenario_pages.baidu_page`。
4. **POM 分层**：`BasePage`（持有 page/env/test_data）→ `CommonPage`（导航、定位、输入、点击、标题断言等通用操作）→ 具体页面（如 `BaiduPage`，用 `@property` 暴露选择器与 URL）。新增页面继承 `CommonPage`。
5. **平台聚合约定**：每个平台包（如 [pages/web/__init__.py](token-price-page/pages/web/__init__.py)）必须定义一个聚合类并赋值 `Pages = WebPages`，在其构造里实例化该平台全部页面——这是动态加载能找到 `Pages` 的契约。新增平台时照此建立 `pages/<platform>/` 并暴露 `Pages`。

其他跨文件约定：

- **环境配置**：`configs/<env>/hosts.yaml`（如 `base_url`）在根 `conftest.py` 的 session fixture 中读出并 `os.environ.update(...)`，页面经环境变量取主机地址。敏感信息放 `.env`（参照 `.env.example`），不要写进 hosts.yaml。
- **测试数据**：按 feature 名组织。feature 名取下划线前的部分作为目录，数据文件为 `test_resource/data/<feature前缀>/<feature名>_data.yaml`，再以场景标签（如 `@AT-0001`）为键。项目代号固定为 `pytest.project_code = "AT"`。
- **日志**：[common/logger.py](token-price-page/common/logger.py) 基于 loguru，拦截标准库 logging，对 password/token/secret 等字段正则脱敏；输出到控制台与 `logs/<env>_<启动时间戳>/`，pytest-xdist 并发时按 worker 分文件。
- **xdist 适配**：根 `conftest.py` 的 `pytest_runtest_makereport` 在并发下用 `@AT-xxxx` 标签重命名 nodeid，保证报告可追溯。
- 示例用例（百度搜索）开箱可跑，但**需能访问 baidu.com**；实际项目中替换 `pages/web/baidu_page.py`、`search_result_page.py` 与 `test_cases/add/` 下示例即可。
