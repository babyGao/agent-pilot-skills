# agent-pilot-skills

> 面向 AI 编码 Agent（Claude Code 等）的可复用、经过验证的 Skill 集合。把一套跑通的工作流沉淀成 Skill，让 Agent 直接知道"该怎么做"，而不是每次都从零摸索。

[English](README.md) | **中文**

## Skill 一览

| Skill | 一句话介绍 | 状态 |
|---|---|---|
| [dispatching-codex-gpt](skills/dispatching-codex-gpt/SKILL.md) | 让 Agent 把任务派给 GPT（通过 Codex），获得独立第二模型的对抗审查、并行执行与交叉验证能力 | ✅ 可用 |
| [orchestrating-parallel-research](skills/orchestrating-parallel-research/SKILL.md) | 作为总协调者并行推进多个独立任务：拆分 / 隔离 / 派活 / 观测，覆盖 Codex/GPT 并行分发、整目录隔离、远程 GPU/SSH、报告规范 | ✅ 可用 |
| [sketch-tech-illustration](skills/sketch-tech-illustration/SKILL.md) | 面向 AI / 科技叙事的「手绘暖调」插画风格规范——锁定四色系、逐元素画法、构图与 Do/Don't 清单 | ✅ 可用 |
| [publishing-to-cnblogs](skills/publishing-to-cnblogs/SKILL.md) | 把文章发布/转发到博客园：本地 Markdown 或从 51cto 抓取，图片重托管到博客园图床，走官方 REST API 发布 | ✅ 可用 |
| 自动化科研系列 | 文献调研、实验设计、论文复现、结果验证等科研工作流 | 🚧 筹备中 |

---

## dispatching-codex-gpt — 双模型协作

### 它解决什么问题

同一个模型审查自己的产出，往往看不出自己的盲区。这个 Skill 教会 Claude 在合适的时机，把任务派给 **GPT（通过 Codex MCP server）** 作为一个真正独立的第二模型——不是"再开一个自己"，而是引入一个视角确实不同的协作者。

### 装上之后的效果

- **对抗式代码审查**：Claude 写完代码后，让 GPT 以全新视角挑错，交叉发现单模型漏掉的 bug。
- **有边界任务的并行外包**：实现一个独立模块、跑一组实验、修一个定位清晰的 bug——派给 GPT 自主完成，Claude 只负责验收 diff 和测试结果。
- **跨模型结论验证**：同一个问题让两个模型独立作答，结果一致才可信。
- **自动规避常见坑**：Claude 会遵循 Skill 内置规则——给 GPT 构造自包含的任务描述（它看不到当前会话）、始终指定工作目录、用 `threadId` 续聊而不是重开空会话、默认最小沙箱权限、绝不盲信 GPT 的修改。

### 安装

**安装 skill —— 一行命令：**

```bash
npx skills add babyGao/agent-pilot-skills -g -y
```

这会用 [Skills CLI](https://skills.sh) 把 skill——**连同随附的 MCP 配置**——复制到你的 agent skills 目录（`-g` = 全局/用户级，`-y` = 免确认）。

**剩下的交给 Claude。** 这个 skill 还需要 GPT 运行时（Codex）和 `gpt-codex` MCP server。第一次你让 Claude 用这个 skill 时，它会自动检测缺什么并帮你注册 MCP server。你只需做两件一次性的事：

- **安装并登录 Codex**（会打开浏览器）：`npm install -g @openai/codex && codex login`
- **重启一次 Claude Code**（注册完 server 后）——之后 `claude mcp list` 显示 `gpt-codex: connected`，`mcp__gpt-codex__codex` / `mcp__gpt-codex__codex-reply` 两个工具出现即成功。

<details>
<summary>想手动挂载 MCP server？</summary>

注册为用户级（所有项目可用）：

```bash
# macOS / Linux
claude mcp add gpt-codex -s user -- codex mcp-server -c sandbox_mode="workspace-write" -c approval_policy="never"
```
```powershell
# Windows（在 PowerShell 里执行）
claude mcp add gpt-codex -s user -- cmd /c codex mcp-server -c sandbox_mode="workspace-write" -c approval_policy="never"
```

或把对应系统的配置复制到项目根目录并改名为 `.mcp.json`：
[`references/mcp.json`](skills/dispatching-codex-gpt/references/mcp.json)（macOS/Linux）· [`references/mcp.windows.json`](skills/dispatching-codex-gpt/references/mcp.windows.json)（Windows）。

> **Windows 注意：** 在 PowerShell 里注册（或 Git Bash 加前缀 `MSYS_NO_PATHCONV=1`），否则 `/c` 会被篡改成 `C:/`，服务器显示 `Failed to connect`。Windows 上启动器必须是 `cmd /c codex …`，不能是裸 `codex`（npm shim）。

挂载后重启 Claude Code——MCP server 在启动时加载。
</details>

### 配置说明

附带的配置以如下参数启动 Codex：

- `sandbox_mode=workspace-write` —— GPT 可以在**工作区内**改文件、跑命令，但没有网络访问。
- `approval_policy=never` —— GPT 自主运行；由 Claude 驱动，没有需要人类中途批准的环节。

两者都可在单次调用时通过 `sandbox`、`approval-policy` 工具参数覆盖——纯审查用 `read-only`，`danger-full-access` 默认不要开。

### 使用

安装后无需特殊命令，Claude 会在合适场景自动启用该 Skill。也可以显式触发，例如：

> "用 codex 让 GPT review 一下我刚才的改动。"
>
> "把这个模块的实现派给 GPT，你来验收。"

---

## orchestrating-parallel-research — 你作为并行舰队的总协调者

### 它解决什么问题

一次跑很多实验/任务很容易失控：agent 互相覆盖文件、你陷入逐个微管、边跑边改目录规范。根因是"边跑边打补丁"而不是"开工前就规范好"。

### 装上之后的效果

- **协调者四招**：沿隔离边界*拆分*、物理*隔离*、给方向不给牢笼地*派活*、持续*观测*调整。你当大脑，agent 做执行。
- **整目录隔离**：每个 agent 一份独立 checkout + 分支 + 产物目录，本地与远端各一份，代码改动与产物互不污染；是否合并回主干可选。
- **派单契约**：给每个 agent 输入 / 输出 / 目标 + 大纲或伪代码，剩下让它自己实现。不逐步教、不堆"不许做 X"。
- **远程 GPU / SSH 纪律**：单串通道、薄件回传 / 重产物留服务器，配部署 + 验收门（不变量、触发计数、单变量）清单。
- **报告规范**：可读性第一——效果与分析优先于代码，表格配一句结论，过长即拆分。

### 安装

还是上面那一行命令，从本仓库安装：

```bash
npx skills add babyGao/agent-pilot-skills -g -y
```

**不需要 MCP server**（和 `dispatching-codex-gpt` 不同）：并行分发直接调用 Codex CLI，装好并登录即可——`npm i -g @openai/codex && codex login`——也可以改用 agent 自带的 sub-agent。

### 使用

当你要把 2 个以上独立任务并行铺开时，Agent 会自动启用。也可显式触发：

> "把这些实验并行铺开——你负责拆分、隔离、派活，我来看汇报。"

---

## sketch-tech-illustration — 面向 AI / 科技叙事的手绘暖调风格

### 它解决什么问题

让 Agent（或设计师）画「AI / 科技」题材，八成会得到光鲜的矢量图：渐变、高光、第二强调色、人脸——又冷又模板化。始终缺一份共享规范来还原那种温暖、手绘、「像有人在旁边给你边画边讲」的质感，于是每次产出都跑偏。

### 装上之后的效果

- **四色系统，写死**：沙米 `#E5DBCA` 打底，陶土橙 `#D2703F` 是*唯一*强调色（面积永不超过画面一成），暖墨黑 `#16140F` 管描边与暗场，纸白 `#F4EFE6` 管面板。没有渐变、没有高光、没有第二强调色。
- **逐元素画法**：思考 / 对话气泡、剪纸的手（画面里「人」唯一的在场方式——不画脸）、拟物界面、搜索胶囊、手绘图表、工具箱卡片、暗场星点、动势短线——每一种都给到笔刷、线宽、收笔、抖动、填色的参数取向。
- **状态靠填色，不靠位移**：核心动效逻辑——用填色白 → 橙表达「选中 / 激活 / 命中」，绝不靠移动或加新颜色。
- **构图 + Do/Don't 清单**：单主体居中、对角分割、满幅色场、before/after，外加一份可直接照抄的复刻清单，保证跨帧、跨人手风格一致。

### 安装

还是上面那一行命令，从本仓库安装：
## publishing-to-cnblogs — 稳定的博客园跨平台转发

### 它解决什么问题

用通用的浏览器自动化工具往博客园转发，会在两处翻车：源站图片（如 51cto）被防盗链拦截、发出来全是裂图链接；2024 年那套往编辑器 `send_keys` 的选择器随博客园改版失效。结果是一篇"图全裂、markdown 没渲染"的废文。

### 装上之后的效果

- **走 API 发布**：通过博客园自己的 REST API 新建/更新文章，`isMarkdown: true`，不依赖脆弱的编辑器脚本。
- **图片重托管**：直连下载源站图片（绕过防盗链）→ 上传到博客园自家图床 → 改写 markdown。原本会 404 的图从此永久可显示。
- **HTML 网格排版**：多张大图排成真正并排的 `<img width>` 网格，而不是竖着堆一列。
- **可选抓取**：把 JS 渲染的源文章（51cto 等）抓成干净 markdown，或直接发本地 `.md`。
- **浏览器只做最少的事**：调试浏览器仅用于登录取 cookie 和可选抓取，其余全是 HTTP 调用。

### 安装

还是那一行：

```bash
npx skills add babyGao/agent-pilot-skills -g -y
```

不需要 MCP server，也没有额外运行时——它是一份纯参考型 skill。

### 使用

当你让 Agent 画这套风格的插画、故事板、幻灯片、封面或动画时会自动启用。也可显式触发：

> "用手绘暖调科技风画这个——沙米打底、只用陶土橙点睛、不画脸。"
再装 Python 依赖：`pip install selenium requests markdownify pyyaml`（需要 Chrome；selenium 4.6+ 会自动匹配 chromedriver）。**不需要 MCP server。**

### 使用

显式触发：

> "把这篇 51cto 文章转发到博客园" · "把这个 markdown 发到博客园，图片帮我重托管"

Agent 会起一个独立的调试 Chrome，让你在里面登录一次博客园，然后抓取 / 清洗 / 重托管图片 / 走 API 发布。

---

## 🚧 即将上架：自动化科研系列

我们正在把一整套科研自动化工作流封装成 Skill，计划覆盖：

- **文献调研**：相关工作检索、领域综述、开源实现发现
- **实验设计**：消融实验规划、基线对比、增量评估策略
- **论文复现**：从 arXiv 链接到可运行的复现实验
- **结果验证**：论文数据与代码交叉核对、数值审计

敬请期待。

## 环境要求

- Claude Code（或其他支持 MCP 的 Agent 运行时）
- Node.js 18+ 及 Codex CLI（[`@openai/codex`](https://www.npmjs.com/package/@openai/codex)），已登录
- 用于 Codex 的 ChatGPT / OpenAI 账号

## 仓库结构

```
skills/
  dispatching-codex-gpt/
    SKILL.md              # skill 本体
    references/
      mcp.json            # gpt-codex MCP 配置 —— macOS / Linux
      mcp.windows.json    # gpt-codex MCP 配置 —— Windows
  orchestrating-parallel-research/
    SKILL.md              # 协调者操作手册
    references/           # dispatch · isolation-and-dirs · remote-gpu-ssh · reporting
  sketch-tech-illustration/
    SKILL.md              # 手绘暖调科技风格规范
  publishing-to-cnblogs/
    SKILL.md              # 发布工作流
    scripts/              # scrape · clean · get_cookies · rehost_images · to_html_rows · publish
    references/           # cnblogs-api · gotchas
```

## 参与贡献

欢迎提 Issue 和 PR——新增 skill、修复问题、改进文档皆可。每个 skill 独占 `skills/` 下的一个文件夹，包含一个 `SKILL.md` 及其所需的辅助文件。

## 许可证

MIT —— 见 [LICENSE](LICENSE)。
