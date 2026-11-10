# 五阶段落地记录

更新时间：2026-11-10。阶段通过只代表本表列出的检查，不代表已完成真实比赛或全部自动化集成。

| 阶段 | 本次落地 | 已验证 | 仍缺少 |
| --- | --- | --- | --- |
| 1：Codex＋Docker＋Python＋共享目录 | Codex CLI、Python、托管 Docker daemon；`/workspace/ctf-challenges/{inbox,work,evidence}` | 无网络容器读入示例编码、完成解码并写出结果，宿主机回读一致；可重复执行脚本通过 | 独立 Codex CLI 的真实 API 任务未验证 |
| 2：Web／Reverse／Crypto 工具 | Python 工具虚拟环境、Chromium、Ghidra 12.2、独立 JDK 25、SageMath 10.6 Docker 镜像 | HTTP 中文正文和页面交互；良性 ELF 导入/分析/main 定位；RSA/AES 往返；Sage 整数分解与多项式运算 | 这些是工具就绪检查，不等同真实题目成功率 |
| 3：DSH，仅技能起步 | 官方 npm `@deepseek-ai/dsh@0.2.2-rc.1`，自定义 `ctf-skills` 单 Solver 配置；关闭额外代理、后台任务和定时调度 | CLI、组合配置及受进程凭据保护的浏览器界面启动 | 真实模型、复杂题接管收益对照未验证 |
| 4：Sapper 分层配置 | 指挥官、将军、侦察兵、士兵、Watchdog 的角色与模型别名模板 | JSON 层级/引用检查；原有本地事实图查看器保留 | tmux、兼容 Agent CLI/协议适配、模型安全凭据、预算与具体任务；未启动完整军团 |
| 5：BreachWeave `pentest` 备用 | 固定分支提交；备用登录控制台，`maxSolvers=0`，最小启动镜像 | 登录页渲染、认证设置 200、未登录 me 接口 401；项目存储/调度 47 项测试通过 | 完整 Web Solver 工具镜像、模型调用、平台适配及同题互斥的自动接线未验证 |

## 目录与版本

- 主仓库：`/workspace/CTF_WP`。
- 题目数据：`/workspace/ctf-challenges`；原始附件放 `inbox`，中间结果放 `work`，证据放 `evidence`。不把题目数据或凭据提交到 Git。
- 工具缓存、安装包和虚拟环境：`/workspace/ctf-toolchain`。大体积安装包、镜像层、node_modules 不提交。
- Python 依赖：`tools/environment/requirements-toolchain.txt`；二进制 SHA-256 与镜像 digest：`config/toolchain-lock.json`。
- DSH/BreachWeave 来源与版本：`config/frameworks-lock.json`；DSH npm 依赖完整性锁：`config/frameworks/dsh/`。
- 原有 Sapper 本地模式与 68 项开发检查仍使用 `tools/environment/setup.sh`，不会自动执行重型工具安装。

## 第一阶段：最小环境

```bash
cd /workspace/CTF_WP
python3 tools/environment/check-minimal.py
```

脚本显式使用托管 Docker 本地 socket，保留 registry 配置，清除会重定向 daemon 的 endpoint/context/TLS selector。测试容器使用宿主用户 UID、无网络、1 CPU、512 MiB；只挂载临时自检目录，结果回读后保留一份非敏感证据。

Docker CLI 存在不是通过标准，必须由守护进程实际运行容器。当前机器是 4 核/32 GiB，16 核/32GB 仍是目标部署规格。

## 第二阶段：按需工具

```bash
python3 tools/environment/install-toolchain.py --with-sage --with-bun
/workspace/ctf-toolchain/venv/bin/python tools/environment/check-web.py
/workspace/ctf-toolchain/venv/bin/python tools/environment/check-crypto.py
bash tools/environment/check-reverse.sh
bash tools/environment/check-sage.sh
export PATH="$PWD/bin:$PATH"
sage -c 'print(factor(10403))'
```

Ghidra、Temurin JDK、Bun 使用官方发行资产并核对 SHA-256。JDK 25 仅供 Ghidra 使用，不替换系统 Java 21。SageMath 和 Python 镜像按 digest 固定；Python 工具依赖按版本固定。工具重装脚本已在当前实例重复执行验证。

`bin/sage` 默认无网络、2 CPU、4 GiB，挂载共享目录并将 `inbox` 叠加为只读。`bin/ghidra-headless` 提供 headless 入口。Web 检查仅访问本地良性页面，不扫描任何目标；Reverse 检查只分析自建 ELF。

当前基础镜像还提供 Chromium、gcc、Java、Node 和 uv。若换服务器，应先按发行版方式提供这些系统前提，不能把脚本存在误报为工具已安装。

## 第三阶段：DSH 单 Solver＋技能

```bash
bash tools/environment/prepare-frameworks.sh
bin/dsh --dump-config
bin/dsh --no-open --host 127.0.0.1 --port 3080
```

来源：`https://github.com/deepseek-ai/deepseek-harness`。安装采用官方发布的 npm 包，源仓库仅用于核实实现与文档；源仓库 master 提交和发布包版本分别记录，不假定两者字节相同。

`ctf-skills` 是本项目从官方 web profile 创建的自定义单 Solver 预设，不是上游叫“仅技能”的内置开关。覆盖配置为 `config/dsh-skills-only.patch.yml`，关闭 subagent/jobs/schedule 及相关 UI/controller，保留正常 Solver 工具与技能机制。它不代表只加载 Markdown 而没有执行工具。

该版本技能发现实现识别项目 `.agents/skills`。本仓库现有 15 个技能入口；目前验证到预设组合与界面启动，尚未把真实模型会话的技能调用或复杂题收益记为通过。

数据使用支持的 `DSH_HOME=/workspace/ctf-toolchain/state/dsh`，不改写系统 HOME。启动地址带进程级访问凭据，保留在本地私有日志，不贴入聊天、截图地址栏或交接文件。进程重启后需重新获取本地访问地址。

接管收益实验应使用同模型、同推理档位、同工具、同题目、同预算的 Codex 基线与 DSH 对照，记录人工介入、耗时、token、费用和独立验证。当前基础工具夹具不能替代复杂 Crypto/Reverse 题集；本次没有执行真实 API 收益实验。

## 第四阶段：Sapper 层级模板

配置：`config/sapper-layered.example.json`。层次保留为：

```text
Commander：全局规划与分派
└─ General：复杂路径和任务分解
   ├─ Scout：限时初筛与证据
   └─ Soldier：执行明确步骤与交付
Watchdog：独立脚本保活、预算/截止管理和交接
```

模型别名引用组合架构规划。当前机器初始活跃 Solver 上限为 2；角色数量模板不等于并发执行数量。Watchdog 不使用语言模型作策略判断。

该 JSON 是层级设计模板，不是可直接传给 `sapper fleet up` 的原生 fleet.json。上游 native fleet 与 Docker commander 入口不同；启动前需将角色映射到已验证的 CLI/网关，补齐 tmux、预算、截止时间和授权题目。

现有 `run_claude()` 支持用 `SAPPER_BIN` 指定兼容 CLI，仍要求 Claude 风格参数及 JSON envelope。用户提供的网关是 OpenAI 兼容候选接口，不能直接当作已经验证的 Anthropic 接口；需要协议/CLI 适配后才能启动对应模型角色。本次没有把模型别名当成已可运行的 Commander。

## 第五阶段：BreachWeave pentest 备用

来源：`https://github.com/m-sec-org/BreachWeave/tree/pentest`。该分支是本地资产/项目/报告平台，和此前讨论的 CTF 主分支接口并非同一产品契约。

```bash
bash tools/environment/start-breachweave-standby.sh
```

- 控制台绑定回环端口 18765，登录/注册由上游提供；本次没有创建或打印用户密码。
- 数据根使用上游默认 `~/.tch-agent` 的链接，实际位于 `/workspace/ctf-toolchain/state/breachweave`。首次创建用户目录链接可能需要托管沙箱授权；存在其他部署时保留并停止，不替换系统 HOME。
- 固定 `maxSolvers=0`，采用 bridge 网络配置。没有向平台登记任何题目/资产，没有实际 Solver，不能据此宣称 Web 求解或平台自动化成功。
- 固定版本的控制台启动会强制准备镜像并编译 Solver binary。为满足备用控制台的范围，本项目预先构建独立命名的最小镜像，再配置它；镜像不含完整 Web 攻击工具，不能作为完整 Solver 镜像使用。
- 该提交的实际代码总是同步 builtin Dockerfile；README 所述的用户 Dockerfile 优先级在此实现中不成立。只改配置目录下的 Dockerfile 不能可靠避免完整 Kali 构建，因此本项目使用已构建镜像的受支持配置入口。
- 冻结 Bun 锁安装后，原生 `cpu-features` 依赖通过自身 npm rebuild 脚本构建，才完成 Linux Solver binary 的编译。

Sapper 与 BreachWeave 同时显示页面不等于同时控制同一题。目前 Sapper 只有本地图查看器、BreachWeave Solver 数为 0，因此没有双重控制。将来启用自动调度前，必须为每题指定唯一 controller；跨框架的自动互斥适配仍待实现，不能仅凭两个配置声明当成已强制执行。

## 模型与安全凭据

非敏感配置：`config/model-providers.example.json`；可供云设置使用的凭据要求：`config/model-secret-requirements.json`。不保存 Key 值。

| Provider | 网关 | 候选模型 | 安全变量名 |
| --- | --- | --- | --- |
| moonshotai-cn | https://api.moonshot.cn/v1 | kimi-k3.1-pro-highspeed / kimi-k3.1-pro | `KIMI_API_KEY` |
| openai（用户别名） | https://api.3366.ai | gpt-6.1-sol | `CTF_OPENAI_API_KEY` |
| aliyun-coding-plan（用户别名 dsh） | https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1 | deepseek-v4.1-flash-1017 | `ALIYUN_DASHSCOPE_API_KEY` |

3366 是用户指定的第三方网关，不是 OpenAI 官方域名；是否需要 `/v1` 和具体协议仍待核验。模型 ID、推理参数和 token-plan 接口可用性均待真实 API 验证。不要把 Provider 名称 `dsh` 与 Harness 本身混淆。

用户在聊天贴出的 Key 没有写入文件或用于调用；应撤销/轮换后将新值填入安全环境设置。当前三项变量均未注入，故模型测试、DSH 收益实验和完整 Sapper 军团仍有外部前提。凭据存在也不自动授权对外扫描，应先给定题目范围及预算。

## 重启与配置持久化

运行进程不随快照恢复。新实例先安装/验证工具，再按需启动 Sapper 本地查看器、DSH 单 Solver profile 或 BreachWeave 备用控制台。运行文件、访问凭据和日志都留在本地工具状态目录。

云配置草稿此前处于不可编辑状态；仓库内保存的提案不是平台已应用的配置。文档明确记录已完成、部分完成和未执行项，不自动发布环境。
