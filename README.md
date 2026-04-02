# Gen AI HW2 — Sales Follow-Up Email Generator

## Overview
A Python prototype that uses Google Gemini 2.0 Flash (via OpenRouter) to generate personalized sales follow-up emails from CRM-style notes. The system takes brief sales call notes and produces professional, context-aware follow-up emails ready for human review.

## Business Workflow
- **Workflow:** Drafting sales follow-up emails after prospect calls
- **User:** A sales representative who has just finished a call with a prospect
- **Input:** Brief CRM notes from a sales call (prospect name, company, discussion points, next steps, tone/context)
- **Output:** A ready-to-send follow-up email that references the conversation, reinforces value, and includes a clear call to action
- **Why automate:** Sales reps spend significant time writing follow-up emails after calls. Automating the first draft lets reps focus on relationship-building while ensuring timely, consistent follow-ups.

## Setup

No external dependencies required — uses only Python standard library.

```bash
# 1. Get an API key from https://openrouter.ai/keys
# 2. Set the environment variable:
export OPENROUTER_API_KEY="your-openrouter-key-here"
```

## Usage

```bash
python app.py                    # Run all eval set cases
python app.py --case 1           # Run a single case by index
python app.py --interactive      # Enter your own notes interactively
```

## Files
- `app.py` — Main script that calls Gemini 2.0 Flash via OpenRouter API
- `prompts.md` — Prompt versions and iteration notes
- `eval_set.json` — Evaluation test cases
- `report.md` — Analysis report

## Video Walkthrough
https://youtu.be/mCIe6nB9UE8
