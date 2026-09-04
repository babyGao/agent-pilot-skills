# Business registries

Lookup tables only. What each source objectively gives you — no rules.
Entity-resolution grading and collection discipline live in `SKILL.md`.

---

## 1. By region

| Region | Source | Objective characteristics |
|---|---|---|
| China | Tianyancha | ~6 page views without logging in; logged in it serves long sessions (70+ lookups at 2.4s intervals observed); phone numbers shown unmasked once logged in; carries trademarks, officers, related entities, risk records |
| China | Aiqicha (Baidu) | Free; slightly fewer fields than Tianyancha |
| China | Qichacha | Same class; some fields paywalled |
| China | National enterprise credit information system | **Official, free, authoritative.** Exact-name lookup only — **no aggregated search and no brand reverse-lookup** |
| United States | SEC EDGAR | Official, free; **public companies only**, so SMEs are absent |
| United States | Secretary of State registries | Official, free; 50 states, 50 different formats |
| United Kingdom | Companies House | **Official free API**, cleanest structured data; **no email field** |
| European Union | National business registers | Fragmented per country. Germany additionally mandates an Impressum, published on the company's own site and often carrying an email |
| Japan | National Tax Agency corporate number site | Official, free, bulk downloadable |
| Cross-jurisdiction | OpenCorporates | Aggregates 1,400+ registries and ~220M companies; **the free API key is public-benefit only** (journalists, NGOs, academics) — commercial use is paid |

---

## 2. Which field comes from where

| Field you want | Where it usually lives |
|---|---|
| Legal name, registration number | Registry |
| Status (active / dissolved / revoked) | Registry |
| Registered capital, incorporation date, company size, headcount | Registry (annual filings) |
| Registered scope, industry code | Registry — this is how you check whether the company actually does this category |
| **Email, phone** | Registry contact fields in China; the Impressum in much of Europe; **usually absent in UK/US registries**, so fall back to the company's own contact page |
| Officers, legal representative | Registry |
| Trademark holder | Registry trademark tab, or the national trademark office |
| Manufacturer name, address, licence number | Product-page specifications (a statutory disclosure for food and several other categories) |
| Store tier (official brand store / authorised / individual) | The platform's own storefront page |

---

## 3. Coverage observed

Numbers from a run over 290 candidate products and 74 query keys. **They shift by industry —
measure your own.**

| Metric | Observed |
|---|---|
| Product pages disclosing a manufacturer name | ~30% |
| Product pages yielding a brand name | ~93% |
| 74 query keys resolved to an operator with an email | 58 companies |
| Small firms using a phone number as the email local-part | Common (`<mobile>@163.com`, `<mobile>@139.com`) |

**Hence the primary key is the brand name, not the manufacturer name** — the first two rows are
why.

---

## 4. Platform anti-abuse, observed

Observed on a large Chinese marketplace; other platforms behave similarly.

**Three tiers**: endpoint refusal -> forced logout -> **identity verification demanded**
(the last tier is effectively irreversible for that account).

Trigger likelihood, highest first:

1. Rotating the User-Agent mid-session (most account-theft-like)
2. Repeatedly hitting licence or credential endpoints
3. Off-screen iframe loading
4. Concurrent requests
5. Mechanically fixed intervals

**Other observations**: the business licence is not viewable on the web client at all (app-only;
the web endpoint returns an anti-abuse code). Once logged in, product specifications, parameters,
reviews, sales figures and category rankings are all retrievable.
