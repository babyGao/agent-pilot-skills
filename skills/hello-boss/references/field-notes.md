# Field notes

Measurements only, from one real outreach run. No rules — what to do about these numbers is in
`SKILL.md`.

September 2026. 58 food-category e-commerce merchants, sent from a free consumer mailbox.

---

## 1. Sending pace

| Pace | Result |
|---|---|
| ~2.5 seconds per message | **Temporary rejection (`451`) at message 11-12**, everything after that refused |
| 60-90 seconds, randomised | 57 attempted, completed in **73 minutes**, 51 delivered |

A `451` is an anti-spam **temporary** rejection — not a suspension and not an invalid address.
It clears after a wait and the same message can be retried.

---

## 2. Bounces

| Metric | Number |
|---|---|
| Attempted | 57 |
| Accepted | 51 |
| Permanent failure (`550 User not found`) | 6 |
| **Bounce rate** | **10.5%** |

All six failures were addresses that had **never been verified before sending**.

---

## 3. By recipient domain

| Recipient domain | Accepted / total |
|---|---|
| `@qq.com` | 33 / 33 |
| `@163.com` | 5 / 11 |
| Company-owned domains | all accepted |

---

## 4. Address shape vs. validity

| Shape | Observed |
|---|---|
| Bare mobile number `@qq.com` | Valid — QQ supports a mobile-number alias |
| Bare mobile number `@163.com` | All 3 returned `550`, address does not exist |
| Landline number `@163.com` | Also failed |
| Obvious placeholder (`123456@…`) | Not sent — that mailbox belongs to a real stranger |
| Company-domain mailbox (`name@company.com`) | Valid |

**A registry email being filled in does not mean it is still in use.** Many were entered once at
incorporation and never read again.

---

## 5. What was not measured

| Metric | Status |
|---|---|
| Open rate | **Unknown** — sent from a hand-written script with no tracking |
| Reply rate | Unknown |
| Whether it reached the inbox | Unknown — only that the server returned `250` |

A `250` means the receiving server accepted the message, not that it reached an inbox.
This gap is the biggest single flaw in that run, and the reason the skill says to use an existing
mailer rather than a hand-rolled loop.

---

## 6. Reusable planning figures

Usable for estimation, but **re-measure when the industry or the sending channel changes.**

| Parameter | Observed |
|---|---|
| Usable daily volume, free consumer mailbox | A few dozen, and only if spread out |
| Safe pace, free consumer mailbox | 60+ seconds per message |
| Wall-clock for one 57-recipient batch | ~1.2 hours |
| Funnel from candidates to list | 290 candidate products -> 74 query keys -> 58 companies listed |
