"""
Sales Follow-Up Email Generator
Uses Google Gemini API to draft follow-up emails from CRM-style sales call notes.
"""

import json
import argparse
import os
import sys
from google import genai

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


def generate_email(notes: str, model_name: str = "gemini-2.0-flash") -> str:
    """Call Gemini to generate a follow-up email from sales notes."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=model_name,
        contents=f"{SYSTEM_PROMPT}\n\nNotes:\n{notes}",
    )
    return response.text


def load_eval_set(path: str = "eval_set.json") -> list[dict]:
    """Load the evaluation set from JSON."""
    with open(path, "r") as f:
        return json.load(f)


def run_eval(cases: list[dict], model_name: str) -> list[dict]:
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


def run_interactive(model_name: str):
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
    parser.add_argument("--model", default="gemini-2.0-flash", help="Gemini model name")
    parser.add_argument("--output", default="output.json", help="Output file for results")
    args = parser.parse_args()

    if "GEMINI_API_KEY" not in os.environ:
        print("Error: Set the GEMINI_API_KEY environment variable.")
        print("  export GEMINI_API_KEY='your-api-key-here'")
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
