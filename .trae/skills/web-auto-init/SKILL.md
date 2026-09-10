---
name: web-auto-init
description: web ui自动化框架初始化技能, 用于初始化web ui自动化框架, 包括目录和文件, 以及库的配置。
license: MIT
metadata:
    author: fzoo.cn@hotmail.com
    version: 0.1.0
    tags:
        - web
        - automation
        - init
---

# web-auto-init

通过 `web-auto-init` 初始化一个基于 **Playwright + Pytest-BDD** 的 Web UI 自动化测试框架。
框架采用 **POM（页面对象模型）+ BDD（行为驱动）** 组织用例，结构参考 `auto-demo` 项目。

本 skill 自带一套 `templates/` 模板，初始化时将模板复制到新项目对应路径即可。

> **项目位置**：所有新项目统一创建在**当前工作目录下的相对路径 `tmp/`** 中（即 `tmp/<project_name>`），不要使用系统绝对路径 `/tmp`。
> `tmp/` 已被工作区根 `.gitignore` 忽略（`tmp/`），临时项目不会进入版本控制；需要长期保留时，再迁移到正式目录。
> 由于项目位于已有 uv workspace 目录树内，`uv init` **必须加 `--no-workspace`**，否则会被自动收编为 workspace member。

## 初始化流程

### 1. 前置：检测 uv

```bash
uv --version
```

若未安装 uv，则执行以下命令安装：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 新建项目（位于相对路径 tmp/ 下）

项目统一创建在**当前工作目录的 `tmp/` 子目录**下（相对路径），使用 `--no-package`（不打包，仅作测试工程）与 `--no-workspace`（保持独立，不被当前 uv workspace 收编）。
如果有输入项目名，会使用输入的项目名，否则使用默认的 `web-demo-$(date +%Y%m%d%H%M%S)`。
```bash
mkdir -p tmp
uv init --no-package --no-workspace tmp/<project_name>
cd tmp/<project_name>
```

`uv init --no-package` 会生成 `README.md`、`main.py`、`pyproject.toml`，后续步骤会覆盖/补全这些文件。

> 下文步骤 3 ~ 8 的所有命令，均在已进入的项目目录 `tmp/<project_name>` 内执行（路径均为相对路径）。

### 3. 创建框架目录结构

```bash
mkdir -p common/utils configs/staging core pages/web \
         test_cases/add test_cases/steps \
         test_resource/data test_resource/objects logs
```

目录说明：
- `common/` 通用工具（日志、YAML、字符串处理）
- `configs/` 环境配置（按环境名分目录，如 `staging/hosts.yaml`）
- `core/` 核心扩展预留
- `pages/` POM 页面对象（按平台分目录，如 `web/`）
- `test_cases/` 测试用例（含 BDD feature 与 steps）
- `test_resource/` 测试资源（`data/` 测试数据、`objects/` 页面对象数据）
- `logs/` 运行日志与报告（运行时按 `<env>_<datetime>` 生成子目录）

### 4. 复制模板文件

本 skill 的模板位于 `templates/` 目录（路径：`<skill_dir>/templates/`）。将下表「模板路径」对应的文件复制到新项目的「目标路径」。模板内容均已在 skill 中备好，直接读取并写入即可，不要自行改写。

| 模板路径 (templates/) | 目标路径 | 说明 |
|---|---|---|
| `conftest.py` | `conftest.py` | 根 pytest 配置：CLI 选项、日志、host、报告路径初始化 |
| `pytest.ini` | `pytest.ini` | pytest 警告过滤 |
| `Makefile` | `Makefile` | `make formatted` / `make run` |
| `main.py` | `main.py` | 入口（覆盖 uv init 默认） |
| `.env.example` | `.env.example` | 环境变量示例 |
| `.gitignore` | `.gitignore` | git 忽略 |
| `.python-version` | `.python-version` | Python 版本 |
| `README.md` | `README.md` | 项目说明（覆盖 uv init 默认） |
| `common/logger.py` | `common/logger.py` | loguru 日志初始化（含敏感信息脱敏） |
| `common/use_yaml.py` | `common/use_yaml.py` | YAML 读取工具 |
| `common/utils/tools.py` | `common/utils/tools.py` | 字符串模板替换工具 |
| `configs/staging/hosts.yaml` | `configs/staging/hosts.yaml` | staging 环境 host 配置 |
| `pages/base_page.py` | `pages/base_page.py` | 页面对象基类 |
| `pages/web/__init__.py` | `pages/web/__init__.py` | Web 平台页面对象聚合（WebPages） |
| `pages/web/common_page.py` | `pages/web/common_page.py` | Web 通用页面操作 |
| `pages/web/baidu_page.py` | `pages/web/baidu_page.py` | 示例：百度页面 |
| `pages/web/search_result_page.py` | `pages/web/search_result_page.py` | 示例：搜索结果页 |
| `test_cases/conftest.py` | `test_cases/conftest.py` | 浏览器 fixture 与 BDD 钩子 |
| `test_cases/test_web.py` | `test_cases/test_web.py` | BDD scenarios 加载入口 |
| `test_cases/add/add.feature` | `test_cases/add/add.feature` | 示例 BDD feature |
| `test_cases/steps/__init__.py` | `test_cases/steps/__init__.py` | steps 重导出 |
| `test_cases/steps/add_steps.py` | `test_cases/steps/add_steps.py` | 示例 step 定义 |

空 `__init__.py` 与 `.gitkeep`（用 `touch` 创建）：
- `__init__.py`（根）
- `common/__init__.py`
- `common/utils/__init__.py`
- `core/__init__.py`
- `pages/__init__.py`
- `test_cases/__init__.py`
- `test_cases/add/__init__.py`
- `test_resource/data/.gitkeep`
- `test_resource/objects/.gitkeep`
- `logs/.gitkeep`

```bash
touch __init__.py common/__init__.py common/utils/__init__.py core/__init__.py \
      pages/__init__.py test_cases/__init__.py test_cases/add/__init__.py \
      test_resource/data/.gitkeep test_resource/objects/.gitkeep logs/.gitkeep
```

> 说明：`baidu_page.py`、`search_result_page.py`、`add.feature`、`add_steps.py` 为**可运行示例**，展示 POM + BDD 用法，开箱即可跑通百度搜索场景。实际项目中可删除或替换为目标站点对应的页面对象与用例。

### 5. 配置依赖

在项目根目录通过 `uv add` 安装依赖（uv 会自动写入 `pyproject.toml` 并解析兼容版本，避免手动写版本号导致的解析失败）：
```bash
uv add loguru playwright pydantic pyhamcrest pytest pytest-bdd pytest-xdist python-dotenv pyyaml
uv add --dev black ruff
```

依赖说明：
| 库 | 用途 |
|---|---|
| `loguru` | 日志（替代标准库 logging，模板 `common/logger.py` 基于 loguru） |
| `playwright` | 浏览器自动化 |
| `pydantic` | 数据验证 |
| `pyhamcrest` | 断言 |
| `pytest` | 测试框架 |
| `pytest-bdd` | BDD 行为驱动 |
| `pytest-xdist` | 并行测试 |
| `python-dotenv` | 环境变量 |
| `pyyaml` | YAML 解析 |
| `black` / `ruff`（dev） | 代码格式化 / 代码检查 |

### 6. 配置开发工具

编辑 `pyproject.toml`，追加以下段（与 `auto-demo` 一致）：
```toml
[tool.black]
line-length = 120
target-version = ['py314']

[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I"]
ignore = ["E501"]
```

### 7. 安装 Playwright 浏览器

```bash
uv run playwright install chromium
# 如需其它浏览器：uv run playwright install firefox webkit
```

### 8. 验证

```bash
uv sync                                  # 同步依赖
uv run pytest --version                 # 验证 pytest
uv run playwright --version             # 验证 playwright
uv run pytest -s test_cases/            # 运行示例用例（需可访问 baidu.com）
```

## 框架结构总览

项目根目录为相对于当前工作目录的 `tmp/<project_name>/`：

```
tmp/<project_name>/
├── conftest.py                 # 根配置：CLI 选项、日志/host/报告初始化
├── pytest.ini                  # 警告过滤
├── Makefile                    # 格式化 / 运行
├── pyproject.toml              # 依赖与工具配置
├── main.py
├── .env.example / .gitignore / .python-version / README.md
├── common/                     # 通用工具
│   ├── logger.py               # loguru 初始化 + 敏感信息脱敏
│   ├── use_yaml.py             # YAML 读取
│   └── utils/tools.py          # 字符串模板替换
├── configs/<env>/hosts.yaml    # 环境主机配置
├── core/                       # 核心扩展预留
├── pages/                      # POM
│   ├── base_page.py            # 基类
│   └── web/                    # Web 平台
│       ├── __init__.py         # WebPages 聚合
│       ├── common_page.py      # 通用操作
│       ├── baidu_page.py       # 示例页
│       └── search_result_page.py
├── test_cases/                 # BDD 用例
│   ├── conftest.py             # 浏览器 fixture + BDD 钩子
│   ├── test_web.py             # scenarios 入口
│   ├── add/add.feature         # 示例 feature
│   └── steps/add_steps.py      # 示例 step
├── test_resource/              # 测试数据 / 对象
└── logs/                       # 运行日志（按 env_datetime）
```

## 运行参数

```bash
uv run pytest -s test_cases/ --env staging --platform web --browser_type chrome --headless
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `--env` | `staging` | 环境名，对应 `configs/<env>/hosts.yaml` |
| `--platform` | `web` | 平台，对应 `pages/<platform>/` |
| `--browser_type` | `chrome` | 浏览器：`chrome` / `firefox` / `safari` |
| `--headless` | `False` | 无头模式 |

## 命令

```bash
make formatted   # black 格式化 + ruff 修复
make run         # 运行 test_cases/ 下用例
```

## 设计要点

- **POM 分层**：`BasePage`（持有 page/env/test_data + 通用等待）→ `CommonPage`（通用操作：导航/标题/查找/输入/点击）→ 具体页面（如 `BaiduPage`）。
- **平台聚合**：`pages/web/__init__.py` 的 `WebPages` 聚合该平台所有页面，`test_cases/conftest.py` 通过 `importlib` 按 `--platform` 动态加载 `pages.<platform>.Pages`。
- **环境隔离**：`configs/<env>/hosts.yaml` 按 `--env` 加载对应主机配置并写入环境变量。
- **BDD 流转**：`pytest_bdd_before_scenario` 创建浏览器/上下文/页面/页面对象，存入 `global_data`；`scenario_pages` fixture 取出供 step 使用；`pytest_bdd_after_scenario` 关闭并清理。
- **日志脱敏**：`common/logger.py` 对 password/token/secret 等关键字段做正则脱敏。
- **并行支持**：`pytest-xdist` 下日志按 worker 分文件，报告 nodeid 适配。
