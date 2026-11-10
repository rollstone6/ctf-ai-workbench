# 当前任务交接

更新日期：2026-11-10；仓库 `rollstone6/ctf-ai-workbench`，路径 `/workspace/CTF_WP`。先读 AGENTS.md 并核对工作区。本记录不自动应用配置或授权新任务。

## 1. 当前目标

按五阶段方案落地最小做题环境、三类题工具、DSH 单 Solver＋技能、Sapper 层级配置和 BreachWeave pentest 备用控制台。

## 2. 已完成

- Docker daemon、Codex CLI、Python、共享目录 `/workspace/ctf-challenges` 已自检；无网络容器完成示例解码并回写证据。
- Web HTTP/浏览器交互、Python RSA/AES、Ghidra 12.2 ELF 分析、SageMath 10.6 数学运算及包装入口均通过。
- 工具在 `/workspace/ctf-toolchain`；官方二进制校验、镜像 digest、Python/npm/Bun 版本锁和安装/自检脚本已保存。
- DSH `0.2.2-rc.1` 的自定义 ctf-skills profile 已启动验证，关闭额外代理/jobs/schedule；真实接管收益未验证。
- Sapper 五层角色设计保存在 `config/sapper-layered.example.json`，不是可直接执行的 native fleet.json；原有本地查看器保留。
- BreachWeave pentest 固定提交 `6957a55...` 的备用控制台已启动验证，47 项项目状态/调度测试通过，`maxSolvers=0`，采用独立最小启动镜像。
- 用户提供了模型网关和精确 ID；仅记录非敏感配置和安全变量名，三组聊天中暴露的 Key 没有写入文件或用于调用。

## 3. 阻塞与未完成

- 三组 Key 应撤销/轮换，新值须通过安全设置注入 `KIMI_API_KEY`、`CTF_OPENAI_API_KEY`、`ALIYUN_DASHSCOPE_API_KEY`；检查时三变量均未设置。
- GPT 网关 `https://api.3366.ai` 是第三方，路径/协议待确认；所有候选模型、推理参数和 API 可用性仍未验证。
- DSH 复杂 Crypto/Reverse 接管收益需要安全凭据、固定题集、同条件对照；没有执行模型任务。
- Sapper 完整军团未启动；还需 tmux、预算/范围及 Agent CLI/网关协议适配。不能直接把 OpenAI 兼容网关当成 Anthropic 接口。
- BreachWeave 仅备用控制台；完整 Web Solver 镜像、CTF 平台适配和跨框架题目互斥自动接线未验证。目前没有两个框架同时控制题目。
- 云凭据要求草稿保存再次返回 `draft_not_editable`，未确认保存；提案在 `config/model-secret-requirements.json`。进程不随快照恢复。

## 4. 关键决策

- 当前配额 4 核/32 GiB；16 核/32GB 只是目标。模型走云 API，不运行本地大模型。
- 大型工具和框架依赖在工具目录，仓库保存锁文件和可复用安装/启动脚本，不提交镜像、安装包、node_modules、访问凭据或运行日志。
- DSH skills 模式是本项目单 Solver 覆盖预设，非上游同名功能；仅验证配置组合和界面，不夸大技能会话/收益。
- BreachWeave 实际同步 builtin Dockerfile，不能按 README 的自定义 Dockerfile 优先级假定；已使用预构建镜像配置入口，Solver 保持禁用。
- 模型路由不以绕过安全拒绝为目的；每题必须有唯一 controller，启用前还需补齐执行层互斥。

## 5. 本次主要文件

`docs/staged-rollout.md`、`config/toolchain-lock.json`、`config/frameworks-lock.json`、`config/model-providers.example.json`、`config/model-secret-requirements.json`、`config/sapper-layered.example.json`、`config/dsh-skills-only.patch.yml`、`config/frameworks/dsh/`、`bin/dsh` / `sage` / `ghidra-headless`、`tools/environment/` 下新工具脚本，以及架构/README/云配置提案。

## 6. 验证结果

- 第一/二阶段各代表性工具检查和安装重复执行通过；Sage/Ghidra 包装器实跑通过。
- DSH 组合配置的编排插件关闭，浏览器界面验证通过；没有真实模型调用。
- BreachWeave 登录页、认证设置 200、未登录接口 401、禁用 Solver 配置验证通过；47 项选定单元测试通过，未运行全项目回归。
- JSON/文档链接/Python 语法/npm 完整性锁检查通过。原有 68 项检查在上一代码阶段通过，本次不重复无关套件。
- 运行端口上次为 Sapper 8765、DSH 3080、BreachWeave 18765；新会话需重新检查，DSH 的进程访问凭据不得粘贴进交接或聊天。

## 7. 下一步

先完成安全凭据轮换/注入并验证模型协议，再以固定复杂题集比较 Codex 与 DSH；之后按角色模板做 Sapper CLI/网关适配与分层启动。只有完成互斥适配及工具镜像验证后，才启用 BreachWeave Solver。

详情：[五阶段落地](../docs/staged-rollout.md)、[架构](../docs/architecture.md)、[环境](../docs/environment.md)。
