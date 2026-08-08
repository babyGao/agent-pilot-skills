# agent-pilot-skills

> Reusable, battle-tested skills for AI coding agents (Claude Code and friends). Capture a proven workflow once as a Skill, and your agent knows *how* to tackle it — instead of improvising from scratch every time.

**English** | [中文](README.zh.md)

## Skills

| Skill | What it does | Status |
|---|---|---|
| [dispatching-codex-gpt](skills/dispatching-codex-gpt/SKILL.md) | Let the agent hand a task to GPT (via Codex) as an independent second model — adversarial review, parallel execution, cross-checking | ✅ Ready |
| [orchestrating-parallel-research](skills/orchestrating-parallel-research/SKILL.md) | Act as the coordinator running many independent tasks in parallel across isolated workspaces — split, isolate, dispatch, observe; covers Codex/GPT fan-out, full-folder isolation, remote GPU/SSH, and reporting | ✅ Ready |
| [sketch-tech-illustration](skills/sketch-tech-illustration/SKILL.md) | A hand-drawn, warm-toned illustration style spec for AI / tech storytelling — locked four-color palette, per-element drawing rules, composition, and a do/don't checklist | ✅ Ready |
| [publishing-to-cnblogs](skills/publishing-to-cnblogs/SKILL.md) | Publish or cross-post an article to 博客园 (cnblogs) — local Markdown or scraped from 51cto — with images re-hosted to cnblogs' own CDN and publishing via the REST API | ✅ Ready |
| [huopan-listing-search](skills/huopan-listing-search/SKILL.md) | Search real Chinese commercial-real-estate listings (shops, offices, warehouses, apartments, hotels) through the 火盘 MCP service in a single call — no handshake, no tool probing — and render the results as HTML cards | ✅ Ready |
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

## sketch-tech-illustration — a hand-drawn look for AI / tech storytelling

### The problem

Ask an agent (or a designer) for "AI / tech" visuals and you usually get slick vector art: gradients, glows, a second accent color, faces — cold and templated. There's no shared spec for the warm, hand-drawn "someone is sketching this on paper for you" look, so every attempt drifts somewhere different.

### What you get

- **A four-color system, locked** — sand `#E5DBCA` ground, terracotta `#D2703F` as the *only* accent (never more than ~10% of the frame), warm ink `#16140F` for linework and dark scenes, paper `#F4EFE6` for panels. No gradients, no glow, no second accent.
- **Per-element drawing rules** — exactly how to draw thought / speech bubbles, cut-paper hands (the only way "people" ever appear — no faces), skeuomorphic UI, the search pill, hand-drawn charts, the toolbox card, dark-scene stars, and motion ticks — down to brush, line weight, end caps, wobble, and fills.
- **State by fill, not motion** — the core animation logic: express *selected / active / hit* by flipping a fill white → terracotta, never by moving things or introducing new colors.
- **Composition + a Do/Don't checklist** — center-single, diagonal split, full-bleed color, before/after — plus a copy-ready replication checklist so the look stays consistent across frames and hands.

### Install

Same one-liner — it installs from this repo:
## publishing-to-cnblogs — reliable 博客园 cross-posting

### The problem

Cross-posting to 博客园 with a generic browser-automation tool breaks in two places: source images (e.g. from 51cto) are blocked by anti-leech and show up as dead links, and the 2024-era editor's `send_keys` selectors rot as the DOM changes. You end up with a post full of broken images and unrendered markdown.

### What you get

- **API-based publishing** — create or update posts through cnblogs' own REST API with `isMarkdown: true`; no fragile editor scripting.
- **Image re-hosting** — download source images (bypassing anti-leech) and upload them to cnblogs' own CDN, then rewrite the markdown. Images that would otherwise 404 now display permanently.
- **HTML grid layout** — multiple wide images become a real side-by-side `<img width>` grid instead of a vertical stack.
- **Optional scraping** — pull a JS-rendered source article (51cto, …) into clean markdown, or publish a local `.md` directly.
- **Minimal browser use** — the debug browser is only for logging in (cookies) and optional scraping; everything else is plain HTTP.

### Install

Same one-liner:

```bash
npx skills add babyGao/agent-pilot-skills -g -y
```

No MCP server or extra runtime needed — it's a pure reference skill.

### Usage

The agent loads it whenever you ask for illustrations, storyboards, slides, cover art, or animation in this aesthetic. Or trigger explicitly:

> "Draw this in the hand-drawn warm-tech style — sand ground, terracotta accent only, no faces."
Then install its Python deps: `pip install selenium requests markdownify pyyaml` (needs Chrome; selenium 4.6+ auto-fetches the matching chromedriver). **No MCP server required.**

### Usage

Trigger explicitly:

> "把这篇 51cto 文章转发到博客园" · "publish this markdown to 博客园 and re-host the images"

The agent launches an isolated debug Chrome, has you log into 博客园 once, then scrapes / cleans / re-hosts images / publishes via the API.

---

## huopan-listing-search — one-call listing search, rendered as cards

### The problem

Point a model at a bare MCP endpoint and it burns a round trip discovering it: `initialize`, `tools/list`, read the schema, *then* search. On chat platforms (豆包 / Kimi / 千问 / WorkBuddy) that shows up as a visibly slow answer — and you have to tell it "check the MCP first, then call it" every time. Worse, it doesn't know the library's shape, so it guesses hard filters that silently return zero, and it dumps raw JSON at the user.

### What you get

- **One call, no probing** — endpoint, transport and a paste-ready request body are in the skill, so the very first request is the search itself. The service is stateless and unauthenticated: no handshake, no `tools/list`.
- **Knows what the library actually holds** — 998 listings, 748 for sale / 250 for lease, Shanghai-heavy, offices most common. Stated as facts, so the model can tell a thin result set from a failed call.
- **Filters that don't silently zero out** — the three optional filters are hard filters; the skill says so, and says to leave them empty unless the user was explicit. Chinese values (「出租」「上海市」「写字楼」) are accepted too.
- **Cards, not JSON** — a compact self-contained HTML skeleton, plus the field table with the fields that are frequently absent marked as such (area and price often simply aren't in the source data).
- **Honest empty results** — a zero-hit response carries a ready-made inventory summary, so the model can say what the library covers and which constraint to relax.

### Install

Same one-liner:

```bash
npx skills add babyGao/agent-pilot-skills -g -y
```

No MCP server registration and no runtime needed — the skill calls a public HTTP endpoint. On chat platforms that have no skills directory, paste `SKILL.md` into the custom-instructions / system-prompt field instead.

### Usage

Triggered by any commercial-property search. Or explicitly:

> "查一下上海陆家嘴旁边适合开火锅店的店铺" · "find me offices for lease in Hangzhou, around 500㎡, and show them as cards"

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
  sketch-tech-illustration/
    SKILL.md              # the hand-drawn warm-tech style spec
  publishing-to-cnblogs/
    SKILL.md              # the publish workflow
    scripts/              # scrape · clean · get_cookies · rehost_images · to_html_rows · publish
    references/           # cnblogs-api · gotchas
  huopan-listing-search/
    SKILL.md              # endpoint · params · field table · HTML card skeleton
```

## Contributing

Issues and PRs welcome — new skills, fixes, and better docs. Each skill lives in its own folder under `skills/` with a `SKILL.md` and any supporting files it needs.

## License

MIT — see [LICENSE](LICENSE).
