# web-demo

基于 Playwright + Pytest-BDD 的 Web UI 自动化测试框架，采用 POM（页面对象模型）+ BDD（行为驱动）组织用例。

## 快速开始

```bash
uv sync                                   # 安装依赖
uv run playwright install chromium       # 安装浏览器
uv run pytest -s test_cases/             # 运行用例
```

## 常用命令

```bash
make formatted   # 代码格式化 (black + ruff)
make run         # 运行 test_cases/ 下用例
```

## 运行参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--env` | `staging` | 环境名，对应 `configs/<env>/hosts.yaml` |
| `--platform` | `web` | 平台，对应 `pages/<platform>/` |
| `--browser_type` | `chrome` | 浏览器：`chrome` / `firefox` / `safari` |
| `--headless` | `False` | 无头模式 |

```bash
uv run pytest -s test_cases/ --env staging --platform web --browser_type chrome --headless
```

## 目录结构

```
├── common/          通用工具 (日志/YAML/字符串处理)
├── configs/         环境配置 (按环境分目录)
├── core/            核心扩展预留
├── pages/           POM 页面对象 (按平台分目录)
├── test_cases/      BDD 用例 (feature + steps)
├── test_resource/   测试数据 / 对象
├── logs/            运行日志
├── conftest.py      根 pytest 配置
└── pytest.ini       pytest 警告过滤
```
