# Reporting standard — readability first, always

Report to the **user / results / analysis**, not to the code.

- **Effect and conclusion**: say what you found, what it means, what to do next. Don't paste where code broke, function/variable names, English identifiers, or implementation detail.
- **Concise**: cut technical noise; if one sentence works, don't write a paragraph.
- **Coherent**: define a term before using it; every argument has a beginning and an end — don't drop jargon cold.
- **Table + one-line takeaway**: data in a table, followed by a single "so what."
- **Length is a signal**: a report over **~4000 chars** means readability is already gone → split by **function / section / time** into several; after writing, compress each table and paragraph once more.

## Paper-quality comparison tables

When comparing methods/results, build it like a paper table so a domain novice sees the point, not a variable dump:

- **Baseline anchors first** (the reference points everything is measured against), then your methods.
- **Clean, fixed column set**; one **takeaway per row**; state the sample size and metric definitions once, up top.
- Group rows by family with italic sub-headers rather than repeating labels.
- **A true three-line table**: markdown can't render one (it draws every border). Use an **HTML table** with only top / header / bottom rules (inline `style`, no vertical or inter-row lines) for in-doc rendering, or **LaTeX `booktabs`** (`\toprule/\midrule/\bottomrule`) for the paper.
