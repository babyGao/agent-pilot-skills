# Directory standardization + full-folder isolation

## Directory: trunk fixed, extend by new folders

- Before creating any file, decide **where it goes and whether a new folder is needed** — never dump in the repo root or a temp dir.
- **Trunk set once, then frozen**: code / docs / artifacts / third-party each in a fixed zone.
- **One new point = one new subfolder** under an existing zone; the trunk shape never changes. A good layout absorbs *all* future output by adding subfolders, not by editing the trunk (scales to dozens of points without restructuring).
- **Artifact paths fixed**: dirs the code reads/writes by default are never moved or renamed.

## Isolation: one workspace per agent, zero cross-pollution

- **(A) Local software**: isolate via **git branch or worktree** per agent/feature.
- **(B) Research / remote**: each agent gets a **full checkout of the main branch into its own folder** + its own branch, **local and remote** (e.g. one project dir per agent on the GPU box). Code edits AND experiment artifacts live in that agent's folder → they can't touch another agent's tree.
- **Merge-back is optional.** For isolated experiments you usually do NOT merge back — the main branch is a read-only template. Merge only in collaborative software dev, and then a single integrator (you) serializes the merges; agents never merge the trunk themselves.

## Why front-load this

Deciding the cut and the layout **before** launch is exactly what lets N agents run at once conflict-free. Patching layout per-agent mid-run is how parallel work loses control — you end up reconciling divergent structures instead of reading results.
