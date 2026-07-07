import json
import os
import re
import time
from datetime import date

import streamlit as st
import streamlit.components.v1 as components
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Weekly Status Report Compressor", page_icon="📊", layout="wide")

SYSTEM_PROMPT = """You are an expert project communications assistant for retail IT project managers.

The report must have these sections in this order:
1. Executive Summary (2-3 sentences)
2. Overall Status — one of 🟢 Green / 🟡 Amber / 🔴 Red — with a one-line rationale
3. Key Accomplishments (bullets)
4. In-Flight Work (bullets, with status)
5. Risks & Issues (bullets, each tagged severity: High/Med/Low)
6. Asks & Blockers (what the audience needs to do)
7. Next Week Focus (bullets)

Rules for the model:
- Only use facts present in the input.
- If something is unclear, say so rather than inventing.
- Adapt tone and detail to the selected audience and length.
- Output clean markdown.
"""

SAMPLE_INPUTS = """Slack thread: Andrea from store ops says the pilot rollout in the North Region is on track, but the second wave of cash drawer updates is slipping because the POS vendor still hasn’t delivered the latest config package. Maria in engineering flagged that three stores are waiting on a test certificate rollover before they can finish activation. Jira board is noisy this week: POS-1847 completed the UI text updates for the new loyalty prompt, POS-1848 moved to QA after the payment gateway patch, and POS-1851 is blocked by a missing approval from the security team. We also had an incident on Wednesday morning when the kiosk reboot script caused a temporary outage in two stores; support was able to recover quickly, but it added extra validation steps for the next deployment window.

Vendor email from Fiserv: they confirmed the patch for the card-present fallback flow will arrive Friday, but only if we approve the non-production test plan by end of day Thursday. They also noted that the earlier device firmware issue might affect the self-checkout terminals if we push too early. I wrote a personal note to myself that the business team wants a clear summary of rollback readiness before we greenlight the Friday morning rollout window. Another note: the regional manager asked for a short executive summary because leadership is worried about the weekend traffic spike and whether the new receipt format will create customer confusion.

More Slack context: Ben said the pilot stores are mostly stable, and the store managers reported that the new receipt prompts are being accepted, though one location is still getting mixed results on the scanner handoff. In the team standup, we agreed to keep the deployment window narrow and to avoid touching the payment service on Thursday afternoon. There was also a side conversation about the store training deck needing a final review by tomorrow. One engineer mentioned that the device imaging task is taking longer than expected because the older terminals are running a legacy image that the migration script doesn’t handle well. We should probably mention that to leadership as a risk, especially since the next wave depends on a successful image refresh.

Personal note: I need to follow up with procurement on the additional printer cables for the test lab, and I should mention to the PMO that the training sign-off is still pending from the retail operations lead. The week felt mixed overall: lots of forward motion, but several dependencies are still holding the line. I also want to make sure the report calls out the incident and the vendor slip so we do not overstate readiness for the next phase.
"""


def copy_to_clipboard(text: str) -> None:
    components.html(
        f"""
        <script>
            navigator.clipboard.writeText({json.dumps(text)});
        </script>
        """,
        height=0,
    )


def extract_overall_status(report: str) -> str:
    heading_match = re.search(r"(?im)^\s*(?:#{1,6}\s*)?(?:\d+\.\s*)?(?:\*\*|__)?overall status(?:\*\*|__)?\s*[:\-]*\s*$", report)
    if not heading_match:
        heading_match = re.search(r"(?im)^\s*(?:\*\*|__)?overall status(?:\*\*|__)?\s*[:\-]*", report)

    if heading_match:
        start = heading_match.end()
        next_heading_match = re.search(r"(?im)^\s*(?:#{1,6}\s*)?(?:\d+\.\s*)?(?:\*\*|__)?(?:executive summary|key accomplishments|in-flight work|risks & issues|asks & blockers|next week focus)(?:\*\*|__)?\s*[:\-]*", report[start:])
        if next_heading_match:
            end = start + next_heading_match.start()
            section_text = report[start:end]
        else:
            section_text = report[start:]
    else:
        section_text = report

    if "🟢" in section_text:
        return "green"
    if "🟡" in section_text:
        return "amber"
    if "🔴" in section_text:
        return "red"

    status_match = re.search(r"(?is)(green|amber|red)", section_text)
    if status_match:
        return status_match.group(1).lower()

    return "unknown"


def build_prompt(project_name: str, reporting_week: str, audience: str, report_length: str, raw_inputs: str) -> str:
    return f"""Create a weekly status report based on the following raw inputs.

Project name: {project_name or 'Not provided'}
Reporting week: {reporting_week or 'Not provided'}
Audience: {audience}
Report length: {report_length}

Raw inputs:
{raw_inputs}
"""


def generate_report(project_name: str, reporting_week: str, audience: str, report_length: str, raw_inputs: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("Please set ANTHROPIC_API_KEY in your .env file before generating a report.")
        return ""

    client = Anthropic(api_key=api_key)
    prompt = build_prompt(project_name, reporting_week, audience, report_length, raw_inputs)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1800,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # pragma: no cover - runtime safety
        st.error(f"Report generation failed: {exc}")
        return ""

    text_parts = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            text_parts.append(block.text)

    return "".join(text_parts).strip()


st.title("Weekly Status Report Compressor")
st.caption("Turn scattered project updates into a clean weekly status report in seconds.")
st.markdown("---")

with st.sidebar:
    st.markdown("### Report settings")
    project_name = st.text_input("📋 Project name", placeholder="e.g. POS Refresh Rollout")
    current_week = f"Week of {date.today().strftime('%Y-%m-%d')}"
    reporting_week = st.text_input("📅 Reporting week", value=current_week)
    audience = st.selectbox("👥 Audience", ["Executive", "Peer PMs", "Engineering team"])
    report_length = st.radio("📏 Report length", ["Short", "Medium", "Detailed"], horizontal=True)
    st.caption("Model: Claude Sonnet 4.6")

if "raw_inputs" not in st.session_state:
    st.session_state["raw_inputs"] = ""

with st.expander("Try it with sample data", expanded=False):
    if st.button("Load sample retail POS rollout inputs"):
        st.session_state["raw_inputs"] = SAMPLE_INPUTS
        st.toast("Sample retail inputs loaded")
    st.caption("Load a realistic week of POS rollout notes for a quick demo.")

st.subheader("Paste your week's raw inputs")
raw_inputs = st.text_area(
    "Paste your week's raw inputs — Jira updates, Slack messages, notes, emails, anything",
    value=st.session_state["raw_inputs"],
    key="raw_inputs",
    height=320,
    placeholder="Example: Completed backlog grooming, deployed config change on Tuesday, risk around vendor SLA, etc.",
)

if st.button("Generate Report", type="primary"):
    if not raw_inputs.strip():
        st.warning("Please paste some raw inputs so I can draft a report.")
    else:
        with st.spinner("Generating your report..."):
            start_time = time.time()
            report = generate_report(project_name, reporting_week, audience, report_length, raw_inputs)
            generation_time = round(time.time() - start_time, 1)

        if report:
            st.session_state["report"] = report
            st.session_state["report_metrics"] = {
                "generation_time": generation_time,
                "input_length": len(raw_inputs.split()),
                "report_length": len(report.split()),
            }

if "report" in st.session_state and st.session_state["report"]:
    report = st.session_state["report"]
    metrics = st.session_state.get("report_metrics", {})
    st.divider()

    overall_status = extract_overall_status(report)
    print(f"DEBUG: overall_status={overall_status}")
    if overall_status == "green":
        st.success("🟢 Overall Status: Green")
    elif overall_status == "amber":
        st.warning("🟡 Overall Status: Amber")
    elif overall_status == "red":
        st.error("🔴 Overall Status: Red")
    else:
        st.info("Status not detected — see report body")

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Generation time", f"{metrics.get('generation_time', 0):.1f}s")
    with metric_col2:
        st.metric("Input length", f"{metrics.get('input_length', 0)} words")
    with metric_col3:
        st.metric("Report length", f"{metrics.get('report_length', 0)} words")

    st.markdown(report)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Copy to clipboard"):
            copy_to_clipboard(report)
            st.toast("Report copied to clipboard")
    with col2:
        st.download_button(
            "📥 Download report (.md)",
            report,
            file_name=f"{(project_name or 'weekly-status').replace(' ', '_')}_{(reporting_week or 'week').replace(' ', '_')}.md",
            mime="text/markdown",
        )
elif "report" in st.session_state:
    st.info("The report could not be generated. Please check your API key and try again.")

st.markdown("<div style='text-align:center; margin-top: 2rem; color: #6b7280;'>Built by Taha Hassan · Powered by Claude Sonnet 4.6 · View source on GitHub</div>", unsafe_allow_html=True)
