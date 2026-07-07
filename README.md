# agent-pilot-skills

> Reusable, battle-tested skills for AI coding agents (Claude Code and friends). Capture a proven workflow once as a Skill, and your agent knows *how* to tackle it — instead of improvising from scratch every time.

**English** | [中文](README.zh.md)

## Skills

| Skill | What it does | Status |
|---|---|---|
| [dispatching-codex-gpt](skills/dispatching-codex-gpt/SKILL.md) | Let the agent hand a task to GPT (via Codex) as an independent second model — adversarial review, parallel execution, cross-checking | ✅ Ready |
| [orchestrating-parallel-research](skills/orchestrating-parallel-research/SKILL.md) | Act as the coordinator running many independent tasks in parallel across isolated workspaces — split, isolate, dispatch, observe; covers Codex/GPT fan-out, full-folder isolation, remote GPU/SSH, and reporting | ✅ Ready |
| Research automation (series) | Literature review, experiment design, paper reproduction, result verification | 🚧 In progress |

---

## dispatching-codex-gpt — two-model collaboration

### The problem

A model reviewing its own output rarely catches its own blind spots. This skill teaches Claude *when* and *how* to hand a task to **GPT (through the Codex MCP server)** as a genuinely independent second model — not "another copy of itself," but a collaborator with a different perspective.

### What you get

- **Adversarial code review** — after Claude writes code, GPT inspects it with fresh eyes and surfaces bugs a single model misses.
- **Parallel outsourcing of bounded tasks** — implement an isolated module, run an experiment, fix a well-scoped bug: dispatch it to GPT to complete autonomously; Claude only reviews the diff and test results.
- **Cross-model verification** — ask both models the same question independently; trust the answer only when they agree.
- **Built-in guardrails** — Claude follows the skill's rules automatically: give GPT a self-contained task (it can't see your session), always set the working directory, continue a session with its `threadId` instead of reopening a blank one, default to the least-privilege sandbox, and never blindly trust GPT's edits.

### Install

**Install the skill — one line:**

```bash
npx skills add babyGao/agent-pilot-skills -g -y
```

This uses the [Skills CLI](https://skills.sh) to copy the skill — **and its bundled MCP config** — into your agent's skills directory (`-g` = global/user-level, `-y` = no prompts).

**Then let Claude finish the setup.** The skill also needs GPT's runtime (Codex) and the `gpt-codex` MCP server. The first time you ask Claude to use the skill, it detects what's missing and registers the MCP server for you. You only do two one-time things:

- **Install & log in to Codex** (opens a browser): `npm install -g @openai/codex && codex login`
- **Restart Claude Code once** after the server is registered — then `claude mcp list` shows `gpt-codex: connected` and the tools `mcp__gpt-codex__codex` / `mcp__gpt-codex__codex-reply` appear.

<details>
<summary>Prefer to mount the MCP server manually?</summary>

Register it user-wide (available in every project):

```bash
# macOS / Linux
claude mcp add gpt-codex -s user -- codex mcp-server -c sandbox_mode="workspace-write" -c approval_policy="never"
```
```powershell
# Windows (run from PowerShell)
claude mcp add gpt-codex -s user -- cmd /c codex mcp-server -c sandbox_mode="workspace-write" -c approval_policy="never"
```

Or copy the bundled config for your OS into your project root as `.mcp.json`:
[`references/mcp.json`](skills/dispatching-codex-gpt/references/mcp.json) (macOS/Linux) · [`references/mcp.windows.json`](skills/dispatching-codex-gpt/references/mcp.windows.json) (Windows).

> **Windows note:** register from PowerShell (or prefix `MSYS_NO_PATHCONV=1` in Git Bash), otherwise `/c` is mangled into `C:/` and the server shows `Failed to connect`. On Windows the launcher must be `cmd /c codex …`, not bare `codex` (it's an npm shim).

Restart Claude Code after mounting — MCP servers load at startup.
</details>

### Configuration

The bundled config launches Codex with:

- `sandbox_mode=workspace-write` — GPT may edit files and run commands **within the workspace**, no network access.
- `approval_policy=never` — GPT runs autonomously; Claude drives it, so there's no human to approve mid-run.

Both are overridable per call via the `sandbox` and `approval-policy` tool parameters — use `read-only` for pure reviews, and keep `danger-full-access` off by default.

### Usage

No special command needed — Claude activates the skill on its own when the situation fits. You can also trigger it explicitly:

> "Have GPT review the change I just made, via codex."
>
> "Dispatch the implementation of this module to GPT; you verify it."

---

## orchestrating-parallel-research — you as the coordinator of a parallel fleet

### The problem

Running many experiments or tasks at once turns into chaos: agents overwrite each other's files, you micromanage every one, and you keep re-standardizing the layout mid-run. The failure mode is reactive patching instead of an up-front setup.

### What you get

- **Four coordinator moves** — *split* on isolation boundaries, *isolate* physically, *dispatch* direction (not a cage), *observe* and adjust. You're the brain; the agents execute.
- **Full-folder isolation** — each agent gets its own checkout + branch + artifact dir, local and remote, so code edits and outputs never cross-contaminate; merge-back is optional.
- **Dispatch contract** — hand each agent input / output / goal + an outline or pseudocode, then let it implement. No step-by-step scripting, no pile of "don't do X".
- **Remote GPU / SSH discipline** — one serial channel, thin files back / heavy artifacts stay, plus a deploy + acceptance-gate checklist (invariant, trigger-count, single-variable).
- **Report standards** — readability first: results and analysis over code, tables with one-line takeaways, split long reports.

### Install

Same one-liner as above — it installs from this repo:

```bash
npx skills add babyGao/agent-pilot-skills -g -y
```

**No MCP server needed** (unlike `dispatching-codex-gpt`): the parallel fan-out drives the Codex CLI directly, so just install and log in — `npm i -g @openai/codex && codex login` — or use your agent's own sub-agents.

### Usage

The agent loads it when you fan out 2+ independent tasks across isolated workspaces. Or trigger explicitly:

> "Coordinate these experiments in parallel — you split, isolate, and dispatch; I'll review the reports."

---

## 🚧 Coming soon: research automation series

A full suite of research-automation workflows, packaged as skills:

- **Literature review** — related-work search, domain surveys, finding open-source implementations
- **Experiment design** — ablation planning, baseline comparison, incremental evaluation
- **Paper reproduction** — from an arXiv link to a runnable replication
- **Result verification** — cross-checking paper numbers against code, numerical audits

Stay tuned.

<!--
When adding a new skill: add a row to the "Skills" table above and insert a section here using this template:

## <skill-name> — <one-line positioning>

### The problem
### What you get
### Install
### Usage
-->

## Requirements

- Claude Code (or another MCP-capable agent harness)
- Node.js 18+ and the Codex CLI ([`@openai/codex`](https://www.npmjs.com/package/@openai/codex)), authenticated
- A ChatGPT / OpenAI account for Codex

## Repository structure

```
skills/
  dispatching-codex-gpt/
    SKILL.md              # the skill itself
    references/
      mcp.json            # gpt-codex MCP config — macOS / Linux
      mcp.windows.json    # gpt-codex MCP config — Windows
  orchestrating-parallel-research/
    SKILL.md              # the coordinator playbook
    references/           # dispatch · isolation-and-dirs · remote-gpu-ssh · reporting
```

## Contributing

Issues and PRs welcome — new skills, fixes, and better docs. Each skill lives in its own folder under `skills/` with a `SKILL.md` and any supporting files it needs.

## License

MIT — see [LICENSE](LICENSE).
