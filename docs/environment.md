# CTF 环境

## 当前云环境背景

以下信息采集于 2026-11-10，描述本次 Codex Cloud 的 Linux 执行环境；后续实例的资源和版本可能不同。

| 项目 | 当前实例 |
| --- | --- |
| 系统发行版 | Debian GNU/Linux 13.6，代号 trixie |
| 内核与架构 | Linux 6.18.57，x86_64（GNU/Linux） |
| 默认终端 | Bash 5.2.37，普通用户 `agent` |
| Python | 3.12.14 |
| Git | 2.52.0 |
| Node.js | 24.22.1；基础 CTF/Sapper 流程不依赖 Node |
| 实际 CPU 配额 | 4 核 CPU（cgroup 配额） |
| 实际内存配额 | 32 GiB（34,359,738,368 字节） |
| 系统可见资源 | 5 个逻辑 CPU、约 33 GiB 内存；不代表容器可用配额 |
| Swap | 无 |
| 工作区存储 | overlay 文件系统，约 63 GiB 总量，采集时约 60 GiB 可用 |
| 工作区 | `/workspace`，主仓库 `/workspace/CTF_WP` |

实际配额以容器 cgroup 限制为依据：`/sys/fs/cgroup/cpu.max` 为 `400000 100000`，即每 100,000 微秒周期允许使用 400,000 微秒 CPU 时间，相当于 4 核；`/sys/fs/cgroup/memory.max` 为 `34359738368`，即 32 GiB。`free` 和逻辑 CPU 数量反映系统可见资源，不能替代配额信息。

这是托管的云执行环境，命令受文件系统沙箱约束；常规项目文件写在 `/workspace` 或 `/tmp`。
GitHub/HTTPS 访问使用平台提供的代理和证书信任配置，保持 TLS 校验开启。
环境提供 Docker CLI，但本次没有验证 Docker daemon 或构建竞赛镜像。

基础工作流包含本地 CLI、技能文档和离线测试；另可按下文启动 Sapper 事实图可视化服务。
所有工具代码现已收录在本仓库的 `vendor/`，运行不依赖 `/workspace` 下另行克隆的上游项目。
可复用的云配置提案保存在 `docs/cloud-environment.json`。本次草稿更新被平台以不可编辑状态拒绝，尚未确认保存；本次操作不发布云环境。

## 仓库布局与使用

本仓库已包含完整的 CTF Skills 和 Sapper 源码，无需另外克隆依赖仓库。

- `vendor/ctf-skills/`：12 项 CTF 专项技能及其参考资料、模板、测试。
- `vendor/sapper-v2/`：Sapper CLI、项目技能、文档、Docker 配置及测试。
- `.agents/skills/`：12 项 CTF 技能和 `sapper-setup` 的仓库内相对链接。
- `bin/sapper`：可从任意目录调用的 Sapper CLI 入口。
- `vendor/SOURCES.json`：上游来源和固定提交；许可证保留于各上游目录的 `LICENSE`。

Linux 环境需要 Python 3.12+ 和 Bash，基础工作流没有 pip 依赖。

```bash
bash tools/environment/setup.sh
export PATH="$PWD/bin:$PATH"
sapper --help
```

验证包括 16 项技能元数据/引用/分流测试、48 项 Sapper 测试，以及临时目录中的事实图生命周期检查。
脚本不会启动攻击、AI 代理或服务，不会为当前项目注册 hooks 或创建真实任务图。

需要启用具体任务图时，阅读 `vendor/sapper-v2/skill/SKILL.md`。
完整 Docker 竞赛编队、模型网关和比赛平台的配置见 `vendor/sapper-v2/docker/ENV.md`，不属于基础环境验证。
可选 Tavily 搜索需要额外凭据和包；PayloadsAllTheThings 数据未下载。

每个云任务已经隔离，使用现有 checkout，无需创建额外 Git worktree。

## 启动 Sapper 本地模式

```bash
cd /workspace/CTF_WP
bash tools/environment/start-sapper.sh
```

该命令可重复运行初始化步骤：保留已有事实图，配置本项目的 Claude hooks，校验事实图，然后在本机回环地址的 8765 端口前台启动可视化服务。
如需换端口，可设置 `SAPPER_VIEW_PORT`。按 Ctrl-C 停止前台服务；进程不会随云快照保存，新实例需重新运行启动命令。

当前实例已初始化 `.sapper/`，默认目标为“维护 CTF AI 工作台的解题记录与任务状态”。事实图和项目级 hooks 不提交 Git。
本次部署的后台进程 PID 记录在 `.runtime/sapper/view.pid`，日志位于 `.runtime/sapper/view.log`；这些运行文件同样不提交。
验证服务时，应请求页面并读取页面引用的实时图 JSON，确认返回当前任务目标；仅有进程或端口不能证明启动成功。

该服务展示和跟踪任务图；自动解题需要另行提供具体任务。完整竞赛编队还需要平台地址、模型网关和凭据，当前未配置。

## 项目理解与中文反馈

目前提供 15 项技能：12 项 CTF 专项技能、Sapper 初始化技能，以及仓库原创的 `project-analysis`、`code-read`。
Sapper 常用反馈默认中文，英文 CLI 模式示例：`SAPPER_LANG=en bin/sapper status`。
详细代码调用链、中文化范围及兼容性限制见 [项目分析说明](project-analysis.md)。

## 跨 Thread 继续工作

长期项目规则见根目录 `AGENTS.md`，当前进度见 `.codex/TASK.md`。后者是项目自定义交接文件，不具备内置自动读取/更新机制；本项目通过 AGENTS.md 的约定要求代理维护它。

新 Thread 可使用以下提示：

```text
先阅读 AGENTS.md 和 .codex/TASK.md，核对 git status 与当前代码，
再按我本次给出的目标继续；不要根据旧记录自动执行新的任务。
```

长任务交接前压缩更新 TASK.md，保留目标、完成/未完成项、关键决策、修改文件、验证结果和下一步。详细设计放在 docs，日志保存在临时文件；不把交接文件当作聊天归档。
