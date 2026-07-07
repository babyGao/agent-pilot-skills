# Remote GPU + SSH discipline

For research that runs on a shared remote GPU box over SSH.

## One serial channel

- Single shared card, **single serial SSH** — one connection at a time. Multi-task = loop inside one connection, not many parallel connections (they cut each other off).
- Long jobs: server-side `nohup` + a status file; poll the log at **≥60 s** intervals, don't hold the connection open.
- **Rate-limit backoff**: a failed connect (`Socket is closed` / auth error) = gateway throttling → wait **~40 s** and retry at a fixed interval, capped (≤~12 tries). Never hammer — dense retries extend the ban.
- Store no credentials on the server.

## Files: thin back, heavy stays

- Return **only thin files** (`.md` / `.csv` / `.json`, small — e.g. ≤200 KB): summaries, metrics, calibration tables. Heavy artifacts (checkpoints, traces, raw logs) stay on the server under a fixed artifact dir.
- Need analysis on heavy data? **Ship the analysis code up** (CPU, can run alongside the GPU), don't pull the data down.
- Every transfer: verify **both-ends md5 per file**; a mismatch = failed transfer, don't run on it.

## Deploy checklist (no step skippable)

1. **GPU idle?** (`ps aux | grep python` — no run in progress). Never deploy during a batch — it corrupts files a running process reads.
2. **Back up** the target dir (cheap; data disk survives reboot).
3. **Push** → both-ends md5 per file.
4. **Smoke gate**: a no-flag minimal run (a 1–2 item subset) must match the reference on the same items before you trust the deploy. Fails → roll back.
5. **Record** deploy time / file list / md5 / source commit in the run report.

## Acceptance gates (every run, or the result is void)

- **Invariant gate**: output still satisfies your project's correctness contract (output-equivalence, quality parity, or a golden-result match) by the agreed metric.
- **Trigger gate**: every switched-on mechanism actually fired (**count > 0**). "Ran and was equivalent" is meaningless if the new path never executed — this trap recurs, so always report `triggered N / total M`.
- **Single-variable gate**: a comparison run differs from its control by exactly one switch.
- **Grids/sweeps go offline** (CPU), not on the GPU. Reserve the GPU for first-run verification, one-off collection, and final adjudication of offline-picked winners.
