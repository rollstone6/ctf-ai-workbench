# 当前任务交接

更新日期：2026-11-10。仓库：`rollstone6/ctf-ai-workbench`；当前实例路径仍为 `/workspace/CTF_WP`。本文件为人工/代理维护的交接记录，不会由 Codex 自动同步。

## 1. 当前目标

为已整合的 CTF/Sapper 项目建立长期协作与短期交接约定，降低重复读取代码、日志和长 Thread 历史的成本。

## 2. 已完成

- CTF Skills 和 Sapper 已完整收录于 `vendor/`，保留许可证和来源版本记录。
- Sapper 已提供本地启动脚本、中文常用 CLI 反馈、中文网页标签和中文优先模型模板。
- 现有 15 项技能包括仓库原创的 `project-analysis` 和 `code-read`。
- 已创建根目录 `AGENTS.md`，约定上下文控制、验证与交接维护；两个项目阅读技能已补充交接流程。

## 3. 未完成与可选配置

- 当前协作约定任务无功能性遗留项；提交状态以 `git status` / `git log` 为准。
- 完整竞赛编队、模型网关、比赛平台凭据未配置；不属于当前任务的必做项。
- 云配置草稿上次返回 `draft_not_editable`，更新未确认保存；提案已保留于 `docs/cloud-environment.json`。不要假定该文件自动应用到平台。

## 4. 关键决策

- 长期规则、短期交接、本机事实图分别存于 `AGENTS.md`、本文件、`.sapper/`。
- 交接内容保持简短、替换过期状态；不复制聊天和完整日志。不按固定 Compaction 百分比安排换 Thread。
- 阅读交接后核对工作区与当前用户目标；旧记录不授权新动作。
- Sapper JSON、ID、状态枚举保持兼容。中文模型反馈目前只有模板约束，尚无真实模型调用验证。

## 5. 本次修改文件

- `AGENTS.md`、`.codex/TASK.md`：协作规则与当前交接。
- `.agents/skills/project-analysis/SKILL.md`、`.agents/skills/code-read/SKILL.md`：加入交接读取、分阶段记录和限定搜索范围。
- `docs/environment.md`：添加新 Thread 继续工作的入口。

## 6. 验证结果

- 上一代码阶段执行 `bash tools/environment/setup.sh`：68 项检查通过；浏览器已验证中文页面、实时图及 JSON 协议。
- 本次只改文档/技能说明：检查路径和 `git diff --check`；不重跑未受影响的代码测试。
- 上次 Sapper 在回环端口 8765 运行；跨 Thread/新实例必须重新检查，不假定进程仍在。

## 7. 下一步

1. 阅读适用 `AGENTS.md` 与本文件，检查 `git status` 和用户最新目标。
2. 有具体开发任务时按目标选择项目分析或代码阅读技能，避免重新加载全部历史。
3. 若用户要查看 Sapper，按 `docs/environment.md` 检查/启动服务并验证真实页面；若要完整竞赛模式，再核对缺少的配置。

详细背景：[项目分析](../docs/project-analysis.md)、[环境与启动](../docs/environment.md)。
