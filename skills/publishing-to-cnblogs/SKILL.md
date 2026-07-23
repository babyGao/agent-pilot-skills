---
name: publishing-to-cnblogs
description: Use when publishing or cross-posting an article to 博客园 (cnblogs) — from a local Markdown file or scraped from another platform such as 51cto — and images show as broken links, markdown won't render, or the old browser-automation tool's selectors have stopped working.
---

# Publishing to 博客园 (cnblogs)

## Overview

Reliably publish a Markdown article to 博客园, or cross-post one from another platform (51cto, etc.). The browser is used only to **log in and (optionally) scrape**; the actual publish goes through cnblogs' own **REST API**, which is far more robust than driving the editor with selenium `send_keys`.

**Core principle:** Re-host every image on cnblogs' own CDN, and publish via the API with `isMarkdown: true`. Hotlinked source images break (anti-leech) and the 2024-era `send_keys` tool rots as the editor DOM changes.

## When to Use

- Cross-posting an already-published article (e.g. on 51cto) to 博客园
- Publishing a local `.md` (with front matter) to 博客园
- Symptoms: images on the published post show **只有链接/裂图**, markdown renders as raw text, or a browser-automation publisher fails on missing selectors

**Not for:** other platforms (CSDN/掘金/知乎…). This skill is cnblogs-specific.

## One-Time Setup

1. **Install deps:** `pip install selenium requests markdownify pyyaml` (Chrome required; selenium>=4.6 auto-fetches the matching chromedriver — else set `CHROMEDRIVER` env var).
2. **Launch an isolated debug Chrome** (coexists with the user's normal Chrome — own profile, no need to close anything):
   ```bash
   chrome --remote-debugging-port=9222 --user-data-dir=/tmp/cnblogs-debug --no-first-run
   ```
   (Windows: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir=%TEMP%\cnblogs-debug`)
3. **Ask the user to log into 博客园** in that window (`https://i.cnblogs.com`). Confirm the DevTools endpoint: `curl http://127.0.0.1:9222/json/version`.

## The Pattern

Run scripts from `scripts/`. Steps 1–2 only for scraping; skip to 3 if you already have a local `.md`.

1. **Scrape** a source article → markdown: `python scrape.py --url <URL> --out article.md`
2. **Clean** page noise (review the result!): `python clean.py --md article.md --cut-before '!\[' --cut-after '\*\*赞\*\*'`
3. **Get cookies:** `python get_cookies.py --out cookies.json`
4. **Re-host images (critical):** `python rehost_images.py --md article.md --cookies cookies.json`
5. **Grid layout for multi-image rows (optional):** `python to_html_rows.py --md article.md`
6. **Publish:**
   - new: `python publish.py --md article.md --cookies cookies.json`
   - update existing: `python publish.py --md article.md --cookies cookies.json --post-id <id>`
7. **Verify:** open the returned URL, scroll, confirm images load. Don't trust `naturalWidth=0` in a background tab — that's lazy-load, not a broken image (see `references/gotchas.md`).

Front matter drives `title` and `tags`:
```markdown
---
title: "文章标题"
tags:
  - 前端
  - claude
---
```

## Quick Reference

| Script | Does | Needs |
|---|---|---|
| `scrape.py` | source URL → markdown (JS-rendered) | debug Chrome |
| `clean.py` | strip page chrome / code gutters / footer | — |
| `get_cookies.py` | export cnblogs cookies + XSRF | debug Chrome, logged in |
| `rehost_images.py` | download (bypass anti-leech) → cnblogs CDN → rewrite URLs | cookies |
| `to_html_rows.py` | multi-image lines → `<div><img width>` grid | — |
| `publish.py` | create/update post via API, `isMarkdown:true` | cookies |

API details: `references/cnblogs-api.md`. Pitfalls: `references/gotchas.md`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Leaving source (51cto) image URLs in the post | Re-host — source anti-leech blocks cnblogs referer (HTTP 567) |
| Multiple wide images on one markdown line | Won't render / stacks — use `to_html_rows.py` HTML grid |
| `page_load_strategy='normal'` when scraping | Hangs on ad scripts — use `eager` + page-load timeout |
| Non-zero implicit wait during scrape | Each missing selector blocks full timeout — set `implicitly_wait(0)` |
| Driving the editor with `send_keys` | Brittle — use the REST API instead |
| Reporting images broken from a background tab | Lazy-load artifact — curl the CDN URL or force `src=data-src` |

## Verification

1. `publish.py` prints the post `url` and `id`.
2. Open the url in a real browser, scroll top→bottom; every image loads.
3. Spot-check: `curl -I <cnblogs-image-url>` → `200` (referer-independent).
4. Post body renders (headings/code), images are `<img>` not literal `![...]`.
