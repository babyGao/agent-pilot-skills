---
name: hello-boss
description: Turns the agent into your outbound salesperson. Use it when you need to reach a batch of companies you have no introduction to — it maps every industry that could buy what you do, resolves each prospect's operating company and email from public business registries, writes one cold email that earns replies, and sends the batch.
---

# hello-boss

Cold outreach breaks at both ends. You cannot **reach** people — you do not know which
industries could even use what you sell, or which legal entity actually operates a brand, or
which address a decision-maker reads. And you cannot **land** — mail bounces or lands in spam.
The middle part, writing well, is the easy part, and it is the only part most tools help with.

Four stages, three deliverables, then it stops.

```
1. Demand discovery -> 2. Data mining -> 3. Message design -> 4. Send
   industries worth       companies +       one cold email      batch it out
   selling to             products + emails
```

| # | Deliverable | Path | Definition of done |
|---|---|---|---|
| 1 | Demand research report | `01_research/report.md` | 10+ candidate industries enumerated, ranking backed by data |
| 2 | Prospect list | `02_list/prospects.csv` | Every row has company name, product, usable email |
| 3 | Email template | `03_template/letter.txt` | One letter, one per-recipient variable |

Anything not in that table is out of scope.

Bundled lookup tables — facts only, every rule is in this file:
`references/target-pools.md` (the 20 industry divisions, how to read an input-output table,
platform and demand-signal maps) · `references/registries.md` (registry sources per region,
which field comes from where, anti-abuse tiers) · `references/field-notes.md` (measurements from
the real run) · `templates/` (fill-in skeletons for all three deliverables).

## When to Use This Skill

- You want to contact a batch of companies and have no warm introduction
- You do not yet know **which industries** could buy what you do — this is the hard part
- You are doing outbound BD, channel partnerships, reseller recruitment, or agency prospecting
- You have a lead list that needs verifying, grading, and turning into something deliverable

## What This Skill Does

1. **Demand discovery** — reframes your identity as a *job*, then runs five independent
   enumeration paths so you surface industries you would never have thought of.
2. **Data mining** — pulls companies from public business registries, then converges four
   independent signals to decide who actually operates each brand.
3. **Message design** — a four-part, 200-250 character letter with exactly one per-recipient
   variable, plus the phrasings that reliably kill replies.
4. **Send** — hands list and template to an existing mailer; three checks before the batch.

## How to Use

### Basic Usage

```
I run a logistics company. Map every industry I could serve and write the research report.
```

### Advanced Usage

```
I run a logistics company. Enumerate serviceable industries using all five discovery paths,
rank by purchase intensity and measured email coverage, then build the prospect list for the
top industry. Show me the letter before anything goes out.
```

### Entering in the middle

The stages are not a required sequence. Each is a valid entry point: "turn this spreadsheet
into a proper prospect list" (stage 2), "what's wrong with this cold email?" (stage 3),
"which of these industries is actually worth doing?" (the convergence step).

---

## Stage 1 — Demand Discovery

**Output is a list of industries, not companies.** Quality is measured by how many "never
occurred to me but they genuinely need this" industries you surface. Dig narrow and the other
three stages are just fishing in a small pond.

### Reframe the capability as a job, not an identity

"I run a logistics company" only ever produces "other logistics companies." **"I move things
that have volume and weight from A to B and carry the risk on time and damage"** immediately
expands the set to anyone with volume and weight to move: furniture, building materials,
plastics, fresh produce, bulky e-commerce, exhibition build-out, cold-chain pharma.

**Strip every industry noun out of the phrasing; keep only the verb and the constraints.**

### Five enumeration paths — run all of them

One path reveals one slice.

**1. Value chain.** Ask *whose cost structure contains my line item.* National input-output
tables show inter-industry purchase flows; the **direct consumption coefficient** tells you how
much of your sector's output each other sector consumes. Read your row across — the large
coefficients are your customer industries, already ranked.

> *Why is plastics a good customer for logistics?* Intuition misses it; the table shows it.
> Plastic goods are bulky and cheap per unit, so freight is a large share of their cost. That is
> the difference between a ranking backed by numbers and a guess.

**2. Walk the classification tree.** Brainstorming misses branches; a tree does not. Take the
official classification for your market (China's GB/T 4754-2017 has 20 top-level divisions;
NAICS and ISIC work the same way) and ask of each division: *is there anyone in here who needs
my job done?* Second payoff: registries index companies by these same codes, so a leaf code
converts "I thought of it" into "I can pull the list."

**3. Move the same job elsewhere.** Strip the industry nouns and see who else does the identical
thing. "Turn product data into charts buyers can verify" also describes tender documents,
renovation quotes, insurance policy explainers, and medical report summaries.

**4. Read the pain signals.** **Job postings are the most honest demand signal there is.** A
company advertising five data-entry or quoting roles is telling you the volume is large enough
to hire for *and the budget is already approved.* Same family: support answering one question
repeatedly, forums repeating the same how-do-I, reviews repeating the same complaint.

**5. Work backwards from the constraint.** Ask *what constraint do I remove, and who is stuck
behind it.* Payment terms point at factoring customers; compliance deadlines at tax and legal
customers; seasonal peaks at flexible-capacity customers.

### Converge — the ranking needs evidence

Five paths produce 30+ candidates. **Ranking by feeling is not allowed:**

| Basis | How you get it | Strength |
|---|---|---|
| Purchase intensity | Direct consumption coefficient, input-output table | Strong, numeric |
| **Email coverage rate** | **Measure it on a 10-company sample** | Strong, numeric |
| Decision-chain length | Company size field in the registry | Medium |
| Sample fit | Have we built this, can we show it | Medium |
| Signal density | Job-posting counts, complaint frequency | Weak, verifiable |

**If you cannot measure coverage, write "unmeasured" — never fill in an estimate.** An industry
at 20% coverage means 100 prospects yields 20 sends. That number decides go/no-go.

### Exclude three kinds that look right

**The decision-maker never sees the mail** (large corporates and state entities register an
administrative or tender-only mailbox — favour small and owner-operated firms). **The deal is
smaller than acquisition cost** (count your own time, not just sending). **Real demand, no
budget** (many job postings but a tiny company means the owner absorbs the work personally).

### Definition of done

`01_research/report.md`: the **full candidate table including everything excluded**, one line
of reasoning each; per industry, which path surfaced it, purchase-intensity evidence, measured
coverage, and what you can offer that you have actually built; the ranking with a one-line
justification per position.

**Failure looks like:** fewer than 10 candidates; winners only, no exclusion list; an estimated
coverage rate; an industry you cannot trace to a path.

---

## Stage 2 — Data Mining

Registries are blunt and useful: company size, registered scope, capital, published email and
phone in one place. The work is not the fetching — raw registry data is dirty with identical
names, outsourced operators, dissolved shells, and contract manufacturers posing as operators.

**Sources by region; the method does not change.** China: Tianyancha / Aiqicha / Qichacha, plus
the free official national enterprise credit system (no brand reverse-lookup). US: SEC EDGAR
(public companies only) and state registries. UK: Companies House — free official API, cleanest
data, no email field. EU: national registers; Germany also mandates an Impressum, often with an
email. Japan: National Tax Agency corporate number site. Cross-jurisdiction: OpenCorporates
(1,400+ registries; the free API key is public-benefit only). Treat the source as a replaceable
layer — access rules and quotas change without notice.

### Brand name to company name: converge four independent signals

Ownership documents are usually not exposed, so no single lookup confirms anything.

| Signal | How to get it |
|---|---|
| **A** Brand to company | Search the registry for the brand, count **active** companies. Exactly one is strongest |
| **B** Trademark holder | Is the holder in that goods class this company, or one of its officers |
| **C** Address match | Address published on the product page or site vs. registered address |
| **D** Store tier | Official brand stores generally require a trademark or exclusive authorisation |

**Strong** (A returns exactly one active company, plus B or C) — add to the list. **Medium**
(one signal) — add, marked medium. **Weak** (no match, several competing active companies, or
only a contract manufacturer's name) — **do not add**; ask the storefront's support channel or
site contact form which address handles partnerships, then add the confirmed one. Guessing costs
a visibly misaddressed email; asking costs a delay, and a confirmed address converts better.

**Two traps.** A contract manufacturer's name is not the operator — it proves who produced the
goods, not who runs the shop, and outsourced production is near-universal in food, cosmetics and
apparel. A company name that reads like an agency ("e-commerce", "network technology") with no
matching activity in its registered scope is probably an outsourced operator; grade it weak.

**Collection discipline.** Platform anti-abuse escalates in tiers and the last tier is
effectively irreversible. **Never rotate the User-Agent mid-session** — it is the most
account-theft-like behaviour and triggers the tightest response. Serial requests, randomised
intervals, no credential endpoints, daily cap, and **stop for the day the first time you see a
rate-limit code**. A dead account ends the whole chain.

### Definition of done

`02_list/prospects.csv` with `brand` (the only name that goes in the letter), `company` (full
legal name, list only), `product` (short name, no spec numbers), `email`, `source`,
`confidence`, `status`.

**Failure looks like:** unverified emails; a company name you cannot source; a product field
stuffed with specifications; weak-grade leads in the list.

---

## Stage 3 — Message Design

**The output is one letter, not a hundred. One variable changes per recipient: the product.**

Deep personalisation does not pay in a first-touch email — its job is to earn a reply, not to
deliver the work. We wrote 58 individually-researched argument paragraphs, checked against
national standards, and threw all of them away. Forty extra words only lengthen the glance. If
the conversation goes deep there is plenty of time after they answer, and by then you know what
they actually care about.

### Four parts, in order, 200-250 characters

| Part | Content |
|---|---|
| 1 | **Introduction and intent** — who I am, how many years, what we do, why I am writing |
| 2 | **Evidence of homework** — "Looking at your [product], there is room on [axis]" — **the only variable** |
| 3 | **Show the muscle** — three service lines, the most relevant one first |
| 4 | **Call to action** — a named artefact they can have by replying |

Part 2 is not analysis; it is proof this is not a blast. Their own product name buys you two
more lines, and that is all it needs to do. Part 3's order is not arbitrary: put the line the
reader recognises first. Part 4's hook needs a name — "happy to chat" is not a hook.

### Do not write

| Do not write | Why |
|---|---|
| An analysis of the recipient's own business data | A cold email is not a deliverable |
| Any percentage promise | You have not run their business |
| The legal entity name or a named officer | Identification has an error rate; getting it wrong costs credibility on the spot |
| "Forgive the intrusion", "hoping to explore collaboration", "your company stands out" | Zero information, occupying the two most expensive lines |
| "Full refund if unhappy", "I won't email you again" | A small vendor swearing oaths reads as small |

**Shortening amplifies sameness** — the shorter the sentences, the larger the shared fraction.
Use any one piece of evidence in only one letter across a batch.

---

## Stage 4 — Send

**Use an existing mailer; do not hand-roll an SMTP loop.** Throttling, backoff, dedupe, open
tracking and unsubscribe are solved problems, and a hand-written loop contains none of them.

Before the batch: **send one to yourself** and confirm every variable rendered and the encoding
is clean; **dedupe** so a re-run never disturbs the same company twice; **do not fire everything
at once** — one measured run hit a temporary rejection at the 11th message at ~2.5 second
spacing, and completed cleanly at 60-90 second intervals. Write the outcome back to `status`.

---

## Directory Convention

Fix the trunk once; extend by adding subfolders, never by reshaping the trunk.

```
<project>/
├─ 01_research/report.md        DELIVERABLE 1   (+ samples/ for the 10-company sample)
├─ 02_list/prospects.csv        DELIVERABLE 2   (+ detail/<brand>/ per prospect)
├─ 03_template/letter.txt       DELIVERABLE 3
└─ archive/<date_topic>/        superseded work, one line on why it was dropped
```

**The three deliverable paths never get renamed or moved.** Folders are named by **brand**,
because the brand is printed on the page and 100% accurate while the company name is inferred.

---

## Three Hard Rules

**Never invent a number.** Every figure in the report and the letter must be checkable by the
recipient. If you cannot get it, write "unmeasured" or skip that prospect. One missing row costs
nothing; one fabricated figure discredits the entire delivery.

**Only the brand name goes outward.** The legal entity name stays in the list. Identification
from public sources always has an error rate, and this makes the worst case one wasted email
rather than visibly addressing the wrong company.

**Prose a human reads is generated by the model.** Code computes structured facts — how many
companies, which grade, what coverage rate. The model turns facts into sentences. Changing the
copy means changing the prompt, not a string literal.

---

## Example

**User**: "I run a logistics company. Who can I actually sell to?"

**Output**:

```
Your capability is not "logistics". Stated as a job it is: "move things with volume and
weight from A to B, carrying the time and damage risk." That reframe opens the target set.

Five paths, 31 candidates. The ones you would not have guessed:

  Value chain    Plastics, glass, building materials - bulky, cheap per unit, so freight
                 is a large share of cost. Highest purchase intensity in the table.
  Class tree     Healthcare division - medical device distributors run scheduled
                 deliveries with damage liability. Nobody lists this.
  Job postings   17 furniture makers in this city are hiring "delivery coordinators".
                 They are absorbing the work in-house today.
  Constraint     Exhibition build-out - extreme seasonal peaks, so they buy flexible
                 capacity rather than owning it.

Top three by purchase intensity plus measured coverage:
  1. Building materials  coefficient high, coverage 7/10 measured
  2. Furniture           coefficient medium, coverage 6/10, 17 hiring signals
  3. Plastics            coefficient high, coverage unmeasured - sampling next

Excluded: 9 industries with reasons. Two examples - state-owned construction (registered
mailbox is tender-only) and single-store retail (deal size below acquisition cost).

Report written to 01_research/report.md. Start the prospect list for building materials?
```

**Inspired by:** a real 58-company outreach run in September 2026. The throttling threshold,
bounce rate and per-domain delivery figures in this skill are measurements from that run, not
estimates — including the parts that went wrong.

## Tips

- **Reframe the identity as a job before you list anything.** This single move is the difference
  between 4 candidate industries and 30.
- **Every candidate must trace back to one of the five paths.** If you cannot say which path
  surfaced it, you guessed it.
- **Keep the exclusion list in the report.** It is the evidence you enumerated rather than
  cherry-picked, and it stops you re-litigating the same industry next quarter.
- **Measure email coverage on 10 companies before committing to an industry.** Estimating it
  wrong wastes everything downstream.
- **One skipped prospect costs nothing. One invented number costs the whole delivery.**

## Common Use Cases

- A software, AI, or forward-deployed engineering team reaching industries that have not adopted
  AI yet
- A logistics company reaching manufacturers with goods to ship
- A design, data, or content team reaching marketplace sellers
- Recruiting resellers, channel partners, or distributors in a new vertical
- Anyone holding a lead list that needs verifying, grading, and turning into a deliverable
