# Weekly Status Report Compressor

A Streamlit app for retail IT project managers to turn scattered weekly updates into a polished markdown status report.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example environment file and add your Anthropic API key:
   ```bash
   copy .env.example .env
   ```
4. Start the app:
   ```bash
   streamlit run app.py
   ```

## Configuration

- Set your Anthropic key in [.env](.env.example).
- The app uses the Claude Sonnet 4.6 model via the Anthropic SDK.

## Usage

- Enter a project name, reporting week, audience, and report length.
- Paste your raw notes and click Generate Report.
- Copy the markdown report to your clipboard or download it as a .md file.
