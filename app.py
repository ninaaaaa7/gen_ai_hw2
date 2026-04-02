"""
Sales Follow-Up Email Generator
Uses Google Gemini API (via OpenRouter) to draft follow-up emails from CRM-style sales call notes.
"""

import json
import argparse
import os
import sys
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Prompt (Version 3 — final, see prompts.md for iteration history)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an experienced sales development representative drafting a follow-up email after a sales call.

Based on the CRM notes below, write a professional follow-up email.

Rules:
- Only reference information explicitly stated in the notes
- Do not fabricate product features, quotes, or details not mentioned
- Keep the email under 200 words
- Use this structure: greeting, reference to conversation, value reinforcement, clear next step, sign-off
- Match the tone to the context: casual for informal meetings, professional for enterprise/formal calls
- NEVER include confidential, legally sensitive, or non-public information in the email (e.g., upcoming layoffs, lawsuits, leaked competitor pricing). If such details appear in the notes, omit them from the email.
- If the notes contain contradictions or unclear information, note what is unclear and write a conservative email that avoids committing to conflicting details.
- If the notes are very sparse, write a brief, general follow-up without inventing specifics.

After the email, add a section called "[REVIEW FLAGS]" listing any concerns: contradictions found, sensitive info omitted, sparse input, or anything else a human should verify before sending."""

DEFAULT_MODEL = "google/gemini-2.0-flash-001"


def generate_email(notes, model_name=DEFAULT_MODEL):
    """Call Gemini via OpenRouter API to generate a follow-up email."""
    api_key = os.environ["OPENROUTER_API_KEY"]
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = json.dumps({
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Notes:\n{notes}"},
        ],
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API Error {e.code}: {error_body}")
        sys.exit(1)


def load_eval_set(path="eval_set.json"):
    """Load the evaluation set from JSON."""
    with open(path, "r") as f:
        return json.load(f)


def run_eval(cases, model_name):
    """Run all eval cases and return results."""
    results = []
    for case in cases:
        print(f"\n{'='*60}")
        print(f"Case {case['id']}: {case['label']}")
        print(f"{'='*60}")
        print(f"\nInput notes:\n{case['notes']}\n")
        print(f"Expected behavior:\n{case['good_output']}\n")
        print("-" * 40)

        output = generate_email(case["notes"], model_name)
        print(f"Generated email:\n{output}")
        results.append({
            "id": case["id"],
            "label": case["label"],
            "input": case["notes"],
            "output": output,
        })
    return results


def run_interactive(model_name):
    """Interactive mode: user enters notes, gets an email."""
    print("Sales Follow-Up Email Generator (interactive mode)")
    print("Enter your sales call notes (press Enter twice to submit):\n")
    lines = []
    while True:
        line = input()
        if line == "":
            if lines:
                break
            continue
        lines.append(line)
    notes = "\n".join(lines)
    print(f"\n{'='*60}")
    print("Generated follow-up email:")
    print(f"{'='*60}\n")
    print(generate_email(notes, model_name))


def main():
    parser = argparse.ArgumentParser(description="Sales Follow-Up Email Generator")
    parser.add_argument("--case", type=int, help="Run a single eval case by index (1-based)")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name on OpenRouter")
    parser.add_argument("--output", default="output.json", help="Output file for results")
    args = parser.parse_args()

    if "OPENROUTER_API_KEY" not in os.environ:
        print("Error: Set the OPENROUTER_API_KEY environment variable.")
        print("  1. Go to https://openrouter.ai/keys")
        print("  2. Create a free account and generate an API key")
        print("  3. export OPENROUTER_API_KEY='your-key-here'")
        sys.exit(1)

    if args.interactive:
        run_interactive(args.model)
        return

    eval_cases = load_eval_set()

    if args.case:
        eval_cases = [c for c in eval_cases if c["id"] == args.case]
        if not eval_cases:
            print(f"Error: No case with id {args.case}")
            sys.exit(1)

    results = run_eval(eval_cases, args.model)

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
