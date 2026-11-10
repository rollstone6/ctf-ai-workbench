---
name: project-analysis
description: 分析项目架构、运行流程、模块职责和依赖边界。适用于接手仓库、理解 Sapper 工作机制、评估部署条件和变更影响；以代码及现有测试为证据，使用中文反馈。
---

# 项目分析

1. 先读取适用的 AGENTS.md、README、环境说明、版本记录和工作区状态，保留现有改动。
2. 用 `rg --files` 找入口、依赖声明、配置、测试；区分项目自有代码与 vendor 上游代码。不要扫描或输出凭据值。
3. 从实际入口沿调用链追踪：参数/环境变量 → 配置 → 核心处理 → 存储或外部服务 → 用户反馈。不得仅根据 README 推断功能已可用。
4. 为关键结论给出文件和行号，记录已验证行为、代码推断及尚缺的运行条件。只运行与分析目标有关的现有测试或离线最小复现。
5. 用中文交付：项目目标、模块图、主要流程、状态/数据结构、启动方法、边界与待确认问题。命令、标识符、路径、JSON 字段保持原样。

## 本仓库导航

- CLI：`bin/sapper` → `vendor/sapper-v2/lib/sapper.py`。
- 图存储：`Store`；项目状态：`.sapper/`（本地运行数据，不提交）。
- 模型输出约束：`vendor/sapper-v2/templates/`；平台接口：`lib/arena.py`；知识库：`lib/kb.py`。
- 本地部署：`tools/environment/start-sapper.sh`；验证：`tools/environment/setup.sh`。
- 上游版本与本地补丁：`vendor/SOURCES.json`。

需要逐函数追踪时继续读取同级 `code-read` 技能。没有具体题目或授权目标时，不启动竞赛、代理调度或网络攻击。
