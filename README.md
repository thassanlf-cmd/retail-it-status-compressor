# Weekly Status Report Compressor

An AI-powered tool that turns a week of scattered project inputs into a clean status report — built by a retail IT program manager, for retail IT program managers.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B)
![Anthropic Claude](https://img.shields.io/badge/Anthropic-Claude%20Sonnet%204.6-8A2BE2)
![Streamlit Cloud](https://img.shields.io/badge/Deployed-Streamlit%20Community%20Cloud-2B6CB0)

🔗 [Live demo](https://taha-retail-it-compress.streamlit.app/)

![Screenshot](docs/screenshot.png)

## The problem

Retail IT project managers often spend hours each week stitching together updates from Jira, Slack, email, notes, and incident logs into a readable status report. The work is repetitive, time-consuming, and prone to inconsistency when deadlines are tight.

## The solution

This app lets you paste raw weekly inputs and instantly generate a structured, audience-aware markdown report in under a minute. It is designed to help PMs move from messy context to a polished update without starting from a blank page.

## Features

- Audience-tuned output for Executive, Peer PMs, and Engineering teams
- Configurable report length: Short, Medium, or Detailed
- Automatic RAG status detection from the generated report
- Built-in sample data for a quick demo experience
- One-click download as markdown

## Tech stack

- Streamlit
- Claude Sonnet 4.6
- Python
- Deployed on Streamlit Community Cloud

## How I built it

I chose Claude Sonnet 4.6 because it performs especially well on long-context synthesis and structured markdown output, which is critical for this use case. Streamlit was the fastest way to ship a polished MVP without building a full web app from scratch. For v1, I kept the scope focused on single-report generation and did not add direct integrations with Jira or Slack. You can read the product context in [PRD.md](PRD.md).

## Run it locally

```bash
git clone <your-repo-url>
cd retail-it-status-compressor
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

## Roadmap

- v2: Jira and Slack integrations
- v3: Team rollups and portfolio views
- v4: PII scrubbing and stronger governance

## About me

Built by Taha Hassan, Sr Program Manager (AI, Tech). LinkedIn: [https://www.linkedin.com/in/taha-hassan-aa773214/]
