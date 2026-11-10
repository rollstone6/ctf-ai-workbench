# 项目分析与代码阅读

## 项目定位

本仓库将 CTF 专项技能和 Sapper 工具集中在一起。技能是供 AI 阅读的 Markdown 工作流；Sapper 是纯 Python 标准库实现的事实图 CLI 和可视化工具。加载技能不会自动启动模型或完成题目。

## 已核对的调用链

| 场景 | 代码路径与职责 |
| --- | --- |
| CLI 调用 | `bin/sapper` 定位仓库 → `vendor/sapper-v2/lib/sapper.py:main` 解析参数 → 对应 `cmd_*` 执行 |
| 数据存储 | `Store` 读写 `.sapper/project.json`、facts、intents 等 JSON，使用文件锁保护并发写入 |
| 状态反馈 | `cmd_status` → `render_status_zh` 或 `render_status` → 显示统计和可执行任务；不改变存储中的状态枚举 |
| 任务规划 | `cmd_dispatch`/`cmd_auto` 读取 `templates/`，填充事实图、任务和提示后请求模型；模型配置是独立运行条件 |
| 网页查看 | `start-sapper.sh` 初始化/复用本地图 → 校验 → `view --serve`；HTML 通过随机路径轮询实时图 JSON |
| 比赛与知识库 | `lib/arena.py` 对接比赛平台；`lib/kb.py` 提供离线知识库操作，并不是网页登录后端 |

## 分析技能

仓库原创的 `.agents/skills/project-analysis/SKILL.md` 用于建立模块和运行条件地图；`.agents/skills/code-read/SKILL.md` 用于具体行为的调用链、边界和证据分析。可直接要求 AI “使用 project-analysis 分析项目”或“使用 code-read 追踪某个入口”。这两项不是下载的第三方同名技能。

## 中文反馈与兼容边界

- `sapper status`、`validate`、空任务提示及顶层错误说明默认中文；`SAPPER_LANG=en` 可恢复这些 CLI 文案的英文模式。
- 网页主要标签、图例、统计及刷新状态使用中文。
- 模型模板默认要求简体中文反馈，用户明确指定其他语言时遵从用户；JSON 字段名、ID、布尔值、状态枚举、代码、命令与原始证据不翻译。
- JSON 输出和命令参数保持原协议。尚未翻译全部 argparse 帮助、底层错误、比赛编队日志和第三方服务的返回文本；底层英文诊断保留以方便定位问题。
- 当前没有配置模型网关，模板的语言要求已加入，尚未通过真实模型调用验证其遵循情况。

运行 `bash tools/environment/setup.sh` 可执行原有 64 项检查和新增 4 项中文/英文切换与协议兼容回归测试。
