# Agent Handoff — The Friction Audit

**Project:** *The Friction Audit: What Your Phone Policy Cannot Do* — three-hour online workshop for PD365
**Delivery:** October 27, 2026, 9:00 a.m.–12:00 p.m. Central, on Zoom
**Facilitator:** Micah J. Miner, M.Ed., Ed.S., CETL
**Handoff written:** September 9, 2026

Read this before touching anything in the repo. Sections 3 and 4 contain the things most likely to waste your time or damage the work.

---

## 1. What this project is

An Illinois-specific district leadership workshop built around Public Act 104-0657 (SB 2427), signed July 28, 2026, which requires districts to adopt a bell-to-bell wireless communication device policy before the 2027–28 school year.

**The thesis, in one sentence:** the statute regulates personal devices and exempts school-issued ones by definition, so compliance is guaranteed on adoption day while nothing about instructional design is touched.

The argument is not anti-restriction. The session is explicitly policy-neutral beyond what the law requires and is built to be equally useful to a district adopting bell-to-bell and one revising an existing policy. **Do not let edits drift it into an anti-ban or pro-ban piece.** That neutrality is a commitment made to the client in writing.

The strongest single piece of evidence is ISBE's own: its *Model Cell Phone Policy* (August 2026) reports, from the Phones in Focus study run with Harvard's Center for Education Policy Research, that teachers estimate **1 in 3 students** use laptops at school for nonacademic purposes. The state named the second problem in the document directing districts to solve the first.

---

## 2. Current state

| Asset | Location | Status |
| :--- | :--- | :--- |
| Session hub | `/index.html` | Complete |
| Deck (participant copy) | `/deck/index.html` | Complete — 34 slides, 7 segments, 4 activities |
| Policy-to-Practice Crosswalk | `/crosswalk/index.html` | Complete |
| Illinois Resource Set | `/resources/index.html` | Complete |

Live at **https://minerclass.github.io/pd365-friction-audit/**. Static pages, no build step for deployment, no dependencies, no analytics. Participant entries in the deck are held in `localStorage` on the participant's own device and are never transmitted.

### The agenda is fixed, not yours to restructure

These seven segments and their timings come from the workshop brief PD365 already holds and will promote from. Content within a segment is editable; the structure is not.

| Offset | Clock | Segment |
| :--- | :--- | :--- |
| 0:00–0:20 | 9:00 | Policy context |
| 0:20–0:50 | 9:20 | Friction framework |
| 0:50–1:20 | 9:50 | Cases and evidence |
| 1:20–1:30 | 10:20 | Break |
| 1:30–2:20 | 10:30 | District audit studio |
| 2:20–2:45 | 11:20 | System alignment |
| 2:45–3:00 | 11:45 | Commitments |

### The five participant takeaways are contractual

The brief promises these by name. Participants have been told they receive them.

1. **Phone Policy Friction Audit tool** — the deck's audit instrument covers this in-session. A standalone re-scoped version is still outstanding; see §6.
2. **Policy-to-practice crosswalk** for phones, one-to-one devices, and generative AI — done, `/crosswalk/`.
3. **Board-ready rationale template** plus stakeholder discussion prompts — the deck's Commitments segment covers the template; the discussion prompts are thin.
4. **Implementation questions** for storage, enforcement, exceptions, access, and communication — partially covered by the "Five implementation questions" slide. Storage is the weakest.
5. **Curated research and Illinois policy resource set** — done, `/resources/`.

---

## 3. Non-obvious things that will trip you up

### 3.1 The deck exists in two forms, and one is generated from the other

- **The artifact copy** is what Micah presents from. It carries facilitator notes on every slide (toggled with `N`) and a working export button backed by the Claude `downloads` capability.
- **The repo copy** at `/deck/index.html` is a *participant* build. Facilitator notes, the notes panel, the `N` key binding, and the Notes button are stripped out. The export button degrades to "use your browser's print dialogue."

**They are not independently maintained.** The repo copy is generated from the artifact source by a strip script. If you edit `/deck/index.html` directly, your change will be silently destroyed the next time anyone regenerates it.

### 3.2 The deck workflow — edit the source, never the build

`src/deck.source.html` is the **canonical deck**. It carries facilitator notes on all 34 slides. `deck/index.html` is generated from it and is what GitHub Pages serves.

```bash
# edit src/deck.source.html, then:
python tools/build_participant_deck.py src/deck.source.html deck/index.html
# commit both
```

The script refuses to write if any notes markup survives the strip or if the slide count changes during the build, so a broken edit fails loudly rather than shipping notes to participants. The build is verified byte-reproducible against the published deck.

Committing the source was a deliberate decision by Micah on September 9, 2026, accepting that the facilitator notes are readable in a public repo in exchange for the source surviving independently of the artifact host. **The notes are still stripped from the served deck** — that has not changed, and should not change without asking. Some of them plan contingencies that read poorly beside a partner's event listing.

The source is also an artifact-style fragment: bare `<title>`, `<link>` and `<style>` followed by body content, with no `<html>`/`<head>`/`<body>` wrapper. That is intentional — the artifact host supplies the skeleton, and the build script supplies it for Pages. Do not "fix" it by adding a doctype.

### 3.3 Who owns what

PD365 (formerly Illinois ASCD) produces the registration page, the participant emails, and the Zoom room, and pulls registrant reports. **Do not draft registration copy or promotional material** — that is theirs, and this has been the pattern across the relationship since 2023. Micah gives the green light on details and amplifies on his own channels.

The one thing to supply them is a two-sentence pre-work note for their participant email: bring your draft policy or the ISBE template. The audit studio fails without it.

### 3.4 Design system

All four pages share one system. Match it rather than inventing:

- **Type:** Newsreader (display, serif), Public Sans (body — the US government typeface, chosen for the civic subject), IBM Plex Mono (data, clock times, labels).
- **Color:** deep civic blue `--accent: #1d4e6f`; gold `--signal: #8c6014` used only for gaps, risks, and things the policy does not cover. The gold is a verified-accessible value carried over from earlier accessibility work in this ecosystem.
- **Theme:** full light/dark token sets on bare `:root`, under `@media (prefers-color-scheme: dark)` guarded as `:root:not([data-theme="light"])`, and under `:root[data-theme="dark"]`. Never define a color only inside a media or `[data-theme]` block.

---

## 4. Citation integrity — read this before adding any source

An audit on September 9, 2026 found that the companion [evidence hub](https://github.com/minerclass/k12-device-policy-evidence-hub) contained **three fabricated or unresolvable identifiers and one fabricated effect size out of nine entries.** The full audit trail is in that repo's `VERIFICATION.md`.

What was wrong:

- The SMART Schools study was attributed to "Kieling, C., et al. (2024)" with an invented title, volume, article number, and DOI. It is **Goodyear et al. (2025)**, *The Lancet Regional Health – Europe*, 51, 101211, and the design is cross-sectional observational, not quasi-experimental.
- A UNESCO DOI that resolves nowhere and is registered with neither Crossref nor DataCite.
- A Dutch government URL returning 404, attached to an unverifiable title.
- Tamim's direct-instruction effect size listed as **0.16** when Table 3 reports **0.31**, with a "negligible or negative outcomes" characterization built on top of it.

**The pattern matters more than the individual errors.** Every fabrication was in a claim that is hard to verify — grey literature, a recent article, a number inside a paywalled table. Every entry with a long-established DOI and every figure printed in an accessible abstract was accurate. That is the signature of generated citations: correct where checking is easy, invented where it is hard.

### The rule for this project

1. Resolve every DOI before committing a citation. Use content negotiation: `curl -sL -H "Accept: application/vnd.citationstyles.csl+json" https://doi.org/<DOI>` and compare author, year, journal, volume, and pages field by field.
2. Fetch every grey-literature URL before committing it. A 403 under a default user agent is usually bot-blocking — retry with a browser user agent before calling it broken.
3. Treat any numeric claim drawn from behind a paywall as **unverified** until someone has opened the table, however plausible it looks beside the numbers around it.
4. Never substitute a press summary for the cited paper.

### What is verified in the workshop materials

| Claim | Status |
| :--- | :--- |
| PA 104-0657 provisions, exemptions, grandfather clause | Verified against the statute and the ISBE model policy PDF |
| ISBE / Phones in Focus figures (60→74%, 9 in 10, 1 in 3, NCES 52%) | Verified against the ISBE *Model Cell Phone Policy*, August 2026 |
| Goodyear et al. (2025) — SMART Schools | DOI verified; findings match the published study |
| Beland & Murphy (2016) | DOI verified |
| Delgado et al. (2018), *g* = −0.21 | Verified against the abstract; it is the **overall** effect across genres, not an informational-text figure |
| Tamim et al. (2011), 0.42 (k=10) / 0.31 (k=15), overall 0.35 | Verified against Table 3 of the full text |
| Kapur (2016), Pew (2024), Odgers | DOIs verified |

**Arithmetic check worth knowing:** Tamim's 0.42 (k=10) and 0.31 (k=15) weight-average to 0.354, matching the published overall mean of 0.35. The old 0.16 figure was incompatible with the paper's own headline result. That kind of internal consistency check is cheap and catches a lot.

---

## 5. Verification tasks — do these before building anything

### 5.1 Zheng et al. (2016) subject-area effect sizes — **highest priority**

*Review of Educational Research*, 86(4), 1052–1084. Paywalled, no open-access copy (checked via Unpaywall). Micah has NLU library access.

The abstract confirms only "significantly positive average effect sizes in English, writing, mathematics, and science." The values are not published in it. Previously circulated figures — ELA 0.15, writing 0.20, mathematics 0.17, science 0.25 — are **currently marked unverified** in the evidence hub and appear nowhere in the workshop materials.

Get the results table. Confirm the four values and whether the metric is Cohen's *d* or Hedges' *g*. Do not restore them from a media summary.

### 5.2 LAUSD Inspector General claims

The **$1.3 billion** figure and the **48-hour bypass** timing are not traced to the 2015 OIG report the evidence hub cites. Press coverage describes a roughly $1.3-billion iPads-for-all plan and reports students at several campuses removing security filters, but neither establishes OIG attribution, and no accessible source states the 48-hour timing.

Locate the passage in the original document, or re-cite to an accessible source that states the figure. The 48-hour detail should be deleted outright unless a primary source turns up. Not paywalled — this is a document hunt.

### 5.3 Dutch national evaluation primary source

The evidence hub now cites a Eurydice summary because the original ministry URL 404'd and the title could not be verified. The evaluation is real: 317 secondary school leaders, 313 primary schools, 12 focus groups, reported March 2025, with roughly 75% reporting improved concentration, 59% improved climate, and 28% academic gain. Find the actual report and cite it directly.

### 5.4 Re-check the ISBE template before delivery

The *Model Cell Phone Policy* is dated August 2026 and ISBE described it as a toolkit for districts beginning policy development. Confirm no revision has been issued before October 27. If one has, the grandfather clause and the optional-exception structure are the parts most likely to move.

---

## 6. Build tasks

### 6.1 Re-scope the standalone Friction Audit tool

An interactive audit exists at `minerclass/potential-outcomes-artifacts` → `friction-audit.html`. It encodes the four-dimension framework correctly but scopes to *an AI-touched assignment*, not to a device policy. The promised takeaway is a **Phone Policy** Friction Audit tool.

Either re-scope it to policy and host it here, or decide the deck's in-session instrument satisfies the promise and say so plainly to PD365. Do not leave the ambiguity unresolved past mid-October.

### 6.2 Strengthen the storage material

Storage is named in the promised implementation questions and is the thinnest content in the deck. The ISBE template enumerates lockers, backpacks, classroom holders, locked pouches, and the school office, each with different cost, liability, and daily time-tax implications for teachers. One slide currently gestures at this. It deserves better, because it is the decision districts will spend real money on.

### 6.3 Stakeholder discussion prompts

Promised alongside the board-ready rationale template and currently thin. The statute mandates input from the teachers' collective bargaining agent, administrators, and parents or guardians, and *encourages* student input. Prompts should map to those four groups.

### 6.4 Pre-work note for PD365

Two sentences for their participant email. Blocks the audit studio if it does not go out.

---

## 7. Commercial and scheduling items — do not act on these

Fee, contract, W-9 under the new PD365 entity, recording and on-demand licensing, registrant counts, and marketing timing are open and are **Micah's to handle directly with Ryan Nevius**. They are tracked in a private planning document, not here.

An agent should not email Ryan, draft messages to him, or make commitments on Micah's behalf. Surface anything relevant to Micah and stop.

---

## 8. Conventions

- **Git identity:** commits use `minerclass@gmail.com`. Never `mminer@bpd3.org`. Check for per-repo overrides that beat the global config.
- **Commit messages:** explain the *why*, not just the what. Citation corrections should state what was wrong, what it is now, and how it was verified.
- **Never commit** IRB material, participant data, transcripts, vendor tokens, or district-identifiable information. Nothing in this project should ever contain student or staff data.
- **The dissertation framework is theoretical.** The associated research has collected no data. Nothing in these materials may report a classroom or district result, and the deck says so where relevant. Do not add language implying empirical findings.
- **Claims discipline.** The session keeps three questions apart throughout: is the restriction workable (implementation), can students participate (access), and what can students explain or do (learning). Edits that blur these undermine the whole argument.

---

## 9. Source map

**This repo**
- `/index.html` — hub, pre-work, links out
- `/src/deck.source.html` — **canonical deck**, with facilitator notes on all 34 slides
- `/deck/index.html` — generated participant deck; never hand-edit, see §3.2
- `/crosswalk/index.html` — the leave-behind matrix
- `/resources/index.html` — annotated sources
- `/tools/build_participant_deck.py` — source-to-Pages build, with safety checks

**Companion repos**
- [`screen-time-wrong-question`](https://github.com/minerclass/screen-time-wrong-question) → `/pouch-and-bypass/` — the full argument and the six-question district audit protocol this workshop operationalizes. **Audited clean:** four DOIs, all resolving correctly, no effect-size claims. This is the most reliable artifact in the ecosystem and the right thing to hand a board member.
- [`k12-device-policy-evidence-hub`](https://github.com/minerclass/k12-device-policy-evidence-hub) — the evidence matrix and search protocol. See its `VERIFICATION.md` for audit status before citing anything from it.
- [`pedagogical-friction`](https://github.com/minerclass/pedagogical-friction) — the four dimensions in full.
- [`When-Output-Looks-Like-Learning`](https://github.com/minerclass/When-Output-Looks-Like-Learning) — the instructional-design companion, and the basis of a proposed follow-on session for curriculum leaders (targeted January 2027, not yet booked).

**Framework citation**
Miner, M. J. (2026). When the output looks like learning: Pedagogical friction and human agency in the age of generative AI. *i.e.: Inquiry in Education, 18*(1), Article 4.

**Primary statutory sources**
- Illinois Public Act 104-0657 (SB 2427), signed July 28, 2026
- ISBE, *Model Cell Phone Policy*, August 2026 — expressly informational, not legal advice
