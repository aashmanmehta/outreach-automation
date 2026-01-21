# outreach-automation

Generate personalized professor outreach emails by:
1) fetching a professor’s most recent papers from *OpenAlex* that are likely to interest you (based on keyword match)
2) using an *LLM* to draft a tailored cold email that introduces you, mentions specific parts of their research, and requests a quick meeting
3) creating a **Gmail draft** via the Gmail API (OAuth)

This tool **only creates email drafts** — it does **not** send any emails.

---

## What it does
- Searches OpenAlex for a professor/author profile
- Pulls recent publications relevant to your profile using your resume + keyword list
- Builds a prompt using your interests + example emails
- Generates a short outreach email (subject line + email body)
- Creates a Gmail **draft** in your account (optionally attaches your resume)

---
## Configuration

This script expects:

- `OPENAI_API_KEY` in a `.env` file (not committed)
- `client_secret.json` in the project root (Google OAuth credentials)
- Update the recipient email in `workflow.py` (`to = "..."`)
- (Optional) Place your resume PDF locally and set `resume_path = "..."` in `workflow.py`

## How to customize 
- Change email_examples to sample emails in your tone, relevant to your goals
- Replace resume_text with your resume's text
- 
## Quickstart

### 1) Install

Create and activate a virtual environment, then install dependencies.

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

