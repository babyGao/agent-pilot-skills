# Dispatching agents — Codex/GPT CLI + parallel fan-out

Default heavy work to a second model via `codex exec` (Codex CLI). You = strategist; agents = executors whose output you re-check deterministically. First confirm `codex --version` and `codex login status` (Logged in using ChatGPT).

## Single call

```
codex exec -C . --model gpt-5.5 --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  --output-schema schema.json \    # force final output to match a JSON Schema
  -o out.json \                    # save the structured final message
  "$prompt" \
  > run.events.jsonl 2> run.stderr.log   # --json events + logs; add --search for web
```

- **Schema strict**: every field `required`, `additionalProperties:false`; prefer **string** values (ranges as `"lo~hi"`) — least likely to be rejected.
- **Windows sandbox trap**: `--sandbox read-only` fails with `CryptUnprotectData failed` (codex can't even read files). On a controlled dev box use `--dangerously-bypass-approvals-and-sandbox`.
- No `jq`? Redirect the `--json` event stream to a file and parse it yourself.

## Parallel fan-out (N agents at once)

```
tpl=$(cat prompt_tpl.txt)                 # template with a __SLICE__ placeholder
for i in $(seq -w 0 19); do
  slice="slices/slice_${i}.json"
  prompt="${tpl//__SLICE__/$slice}"
  codex exec -C . -m gpt-5.5 --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
    --output-schema schema.json -o "part_${i}.json" \
    "$prompt" > ".codex-runs/${i}.events.jsonl" 2> ".codex-runs/${i}.stderr.log" &
done
wait
```

- Run the whole batch in the **background** (you get notified on completion) — don't foreground-wait.
- Progress / triage: `tasklist | grep codex.exe` (how many left); read each `.stderr.log`.
- After: merge `part_*.json` → **you** verify deterministically (align / dedup / score). Never let agents self-score.
- Flow: `big task → split into N slices → N agents × M items → merge → you verify/synthesize`.

## Prompt contract (话少、给清、不教做事)

A dispatch prompt needs only:
1. **Role + task** — 1–2 sentences.
2. **Input** — file paths + what the data looks like.
3. **Output** — strict schema, each field's meaning stated.
4. **Rules** — a few hard constraints, concise.
5. **Self-check tool** — one command it can run to calibrate and fix itself, e.g. `echo '<result JSON>' | python check.py`.
6. **Where this step sits** — the agent can't see the global pipeline; you can. Give its position + up/downstream, plus an **outline / pseudocode**.
7. Close: **"output only the schema JSON, no chatter."**

Do NOT teach it step-by-step or pile on "don't do X" anti-error clauses — flag risks lightly, then let it think.

## "Giving an agent skills"

Codex has no skill system → "configure skills" = name in the prompt the **scripts / commands / tools it may use** and how to call them (a self-check CLI, an allowed read-only python). It can read files and run commands in its own workspace.

## Alternative: MCP dispatch (interactive, live progress, threads)

For a single different-model sub-agent with live progress and a reusable thread, use the Codex **MCP server** (`mcp__gpt-codex__codex` / `codex-reply`) instead of the CLI — see the `dispatching-codex-gpt` skill. CLI batch (above) is better for N-way autonomous fan-out; MCP is better for one interactive back-and-forth.
