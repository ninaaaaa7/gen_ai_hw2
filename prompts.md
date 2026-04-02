# Prompt Iteration Log

## Version 1 — Initial Prompt

```
You are a helpful sales assistant. Write a follow-up email based on these sales call notes.

Notes:
{notes}
```

### Observations
- Produced generic, overly enthusiastic emails
- Tended to fabricate details not present in the notes (e.g., inventing product features or specific things said in the call)
- No structure — sometimes very long, sometimes too short
- Did not handle edge cases well (minimal notes led to hallucinated context)
- Included sensitive information when present in notes without filtering

---

## Version 2 — Added Role, Structure, and Constraints

```
You are an experienced sales development representative drafting a follow-up email after a sales call.

Based on the CRM notes below, write a professional follow-up email.

Rules:
- Only reference information explicitly stated in the notes
- Do not fabricate product features, quotes, or details not mentioned
- Keep the email under 200 words
- Use this structure: greeting, reference to conversation, value reinforcement, clear next step, sign-off
- Use a warm but professional tone

Notes:
{notes}
```

### What changed
Added explicit role definition, structural guidance, a word limit, and a constraint against fabrication.

### What improved
- Emails became more consistently structured
- Hallucination decreased significantly on normal cases
- Length became more appropriate and consistent
- Edge case with minimal notes improved — less fabrication

### What stayed the same or got worse
- Still included sensitive information (layoffs, lawsuits) when present in notes
- Contradictory notes still produced confident-sounding but inconsistent emails
- Tone was sometimes too formal for casual scenarios (e.g., conference meeting)

---

## Version 3 (Final) — Added Sensitivity Filter and Tone Matching

```
You are an experienced sales development representative drafting a follow-up email after a sales call.

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

After the email, add a section called "[REVIEW FLAGS]" listing any concerns: contradictions found, sensitive info omitted, sparse input, or anything else a human should verify before sending.

Notes:
{notes}
```

### What changed
Added sensitivity filtering rules, tone-matching guidance, contradiction handling, sparse-input handling, and a review-flags section for human oversight.

### What improved
- Sensitive information (layoffs, lawsuit, competitor pricing) now omitted from emails
- Contradictory notes now produce hedged language and flag issues for review
- Tone better matches context (casual for conference, formal for enterprise)
- Review flags section provides clear signal for when human review is critical
- Minimal-notes case produces appropriately brief emails

### What stayed the same or got worse
- Review flags sometimes over-flag normal cases (minor false positives)
- Model occasionally still uses slightly aggressive CTAs on objection-heavy cases
- The email for contradictory notes is safe but may feel too vague to be useful without human editing
