# PRD: Weekly Status Report Compressor

**Owner:** [Your Name] · **Status:** MVP · **Last updated:** [Date]

## Problem

Retail IT project managers spend 1–3 hours every Friday synthesizing a week's worth of scattered inputs — Jira updates, Slack threads, engineer DMs, incident notes, vendor emails — into a clean weekly status report for leadership, business partners, and peer teams. The synthesis is repetitive, low-leverage, and often the last thing standing between a PM and their weekend. Reports are also inconsistent in structure and detail, making them hard to read week-over-week.

## Target users

**Primary:** Retail IT project managers running a program or portfolio (store systems rollouts, POS refreshes, e-commerce platform migrations, ERP upgrades).

**Secondary:** Engineering managers writing similar updates; program managers in adjacent IT domains (infra, security, data).

## User story

> As a retail IT PM, I want to paste my messy week's inputs and get a clean, audience-appropriate status report in under 60 seconds — so I can spend Friday afternoon on real project work instead of report-writing.

## Solution

A single-page web app where the PM:

1. Pastes raw inputs (Jira exports, Slack copy-pastes, notes, emails) into a large text box
2. Sets context: project name, reporting week, target audience (Exec / Peers / Engineering)
3. Picks report length (Short / Medium / Detailed)
4. Clicks **Generate Report**
5. Receives a structured markdown report they can copy, download, or paste into email/Confluence/Teams

Every report includes: executive summary, overall RAG status with rationale, accomplishments, in-flight work, risks & issues, asks/blockers, next-week focus.

## Success metrics

**For this MVP (leading indicators):**
- Time from paste to usable report: < 60 seconds
- Report requires < 2 edits before sending (self-reported)
- User willing to run it again on a real report next week

**For a hypothetical productionization:**
- % of PMs using it 3+ weeks in a row (habit formation)
- Time saved per report (target: 45 minutes)
- Sean Ellis PMF test: "would you be very disappointed if this went away?" → >40% "yes"

## Non-goals (v1)

- Integrations with Jira, Slack, or email (v2)
- Multi-project portfolio rollups (v2)
- Team-wide sharing and history (v2)
- Fine-tuning on a user's past reports (v3)
- Full PII/DLP handling (would matter for real deployment; this is a PoC)

## Model choice

**Claude Sonnet 4.6** via Anthropic API.

Rationale:
- Strong long-context synthesis (which is exactly the task)
- Reliable structured markdown output
- Cost and latency acceptable for a single-shot generation (~$0.01/report)

Alternatives considered:
- **GPT-4o** — comparable quality, slightly weaker at holding to a fixed section template in noisy input tests
- **Claude Haiku 4.5** — faster and cheaper, but noticeably weaker on messy multi-source synthesis
- **Local model (Llama 3)** — attractive for data-sensitive deployments, out of scope for v1

## Evals (v0 sanity check)

Five hand-crafted input packets covering:

1. Clean "green week" with obvious progress
2. "Red week" with a P1 incident
3. Mostly-empty week (edge case)
4. Very long input (5+ pages of noise)
5. Ambiguous status (some wins, some real risks)

**Pass criteria per case:** report is factually grounded in the input; RAG status matches human judgment; zero hallucinated projects, people, or dates.

## Risks

| Risk | Mitigation |
|---|---|
| Hallucination — model invents specifics not in input | System prompt requires grounding; eval set catches regressions |
| PII leakage — real inputs contain names, emails, ticket IDs | v1 is BYO-input to a personal instance; v2 would add PII scrubbing pre-API-call |
| Over-reliance — PMs stop reading their own inputs | Not a v1 concern; monitor in user research if this reaches real users |
| Vendor lock-in on Anthropic | Abstract the LLM call so swap to another provider is < 1 hour |

## Rollout (hypothetical)

- **v1 (this repo):** Personal-use MVP, deployed to Streamlit Cloud
- **v2:** Jira + Slack read integrations, project memory across weeks
- **v3:** Team rollups, exec dashboard view, PII scrubbing
