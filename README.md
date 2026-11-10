# CTF AI Workbench

面向 Web、Reverse、Crypto 的 AI 辅助解题工作台，整合 CTF 技能、Sapper 事实意图图、中文反馈和可复用的云环境流程。

## 推荐架构

题目进入 → Codex 分诊与单 Solver 快路 → 复杂 Crypto/Reverse 转 DSH → Web 专项由 Kimi 求解、批量由 BreachWeave 编排 → 独立 Flag/证据验证。

Sapper 作为可选的长期编排和事实图层。黑产链路题归入 Web，SQL 注入不在本次范围。模型路由按能力、成本与可用性选择，安全拒绝不触发自动跨模型重试。

- [五阶段落地、工具安装、自检与运行状态](docs/staged-rollout.md)
- [组合架构、范围、框架比较和模型分工](docs/architecture.md)
- [配置规划模板](config/architecture-plan.json)：设计草案，尚无运行时加载器，不会自动启动 Agent 或调用模型。
- [当前环境与启动说明](docs/environment.md)：当前实例 4 核/32 GiB；16 核/32GB 是目标部署规格。
- [项目分析与代码阅读](docs/project-analysis.md)
- [历史学习笔记](docs/legacy-notes.md)

DSH 单 Solver＋技能预设和 BreachWeave `pentest` 备用控制台已安装验证；真实云 API 模型、接管收益与完整多角色调度尚未验证。模型 ID/推理参数需在选定网关核验。所有模型通过云 API 使用，不计划在本机部署大模型。

## CTF AI 技能与 Sapper


现已将 CTF Skills、Sapper 和可复用环境脚本统一收录到本仓库。
源码与许可证位于 `vendor/`，15 项技能入口位于 `.agents/skills/`。

```bash
bash tools/environment/setup.sh
export PATH="$PWD/bin:$PATH"
sapper --help
```

详见 [环境说明](docs/environment.md) 和 [上游版本记录](vendor/SOURCES.json)。
