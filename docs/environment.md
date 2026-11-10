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
| 可见计算资源 | 5 个逻辑 CPU，约 33 GiB 内存，无 Swap |
| 工作区存储 | overlay 文件系统，约 63 GiB 总量，采集时约 60 GiB 可用 |
| 工作区 | `/workspace`，主仓库 `/workspace/CTF_WP` |

这是托管的云执行环境，命令受文件系统沙箱约束；常规项目文件写在 `/workspace` 或 `/tmp`。
GitHub/HTTPS 访问使用平台提供的代理和证书信任配置，保持 TLS 校验开启。
环境提供 Docker CLI，但本次没有验证 Docker daemon 或构建竞赛镜像。

当前准备的是本地 CLI、技能文档和离线测试工作流；没有后台应用服务。
所有工具代码现已收录在本仓库的 `vendor/`，运行不依赖 `/workspace` 下另行克隆的上游项目。
安装和启动说明保存在云环境配置草稿；本次操作不发布云环境。

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
