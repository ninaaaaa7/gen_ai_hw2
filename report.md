# Report — Sales Follow-Up Email Generator

## Business Use Case

Sales representatives spend significant time drafting follow-up emails after prospect calls. This prototype automates the first draft by taking brief CRM-style notes and generating a professional, context-aware follow-up email. The target user is an individual sales rep who wants to send timely follow-ups without spending 10-15 minutes writing each one.

## Model Choice

I used **Google Gemini 2.0 Flash** via OpenRouter. I initially attempted the direct Gemini API but encountered regional free-tier restrictions, so I switched to OpenRouter which provides access to the same model. I chose Gemini 2.0 Flash because it is fast, inexpensive, and followed instructions well for a drafting task that still requires human review.

## Baseline vs. Final Design

**Baseline (Prompt V1):** A minimal prompt ("Write a follow-up email based on these notes") produced emails that were inconsistent in length and structure, frequently hallucinated details not in the notes, and included sensitive information verbatim.

**Final (Prompt V3):** After two rounds of iteration, the final prompt added: explicit anti-hallucination rules, a 200-word limit, structural guidance, tone-matching instructions, a sensitivity filter for confidential information, and a `[REVIEW FLAGS]` section that highlights issues for human review.

Key improvements observed across the 7-case eval set:
- **Normal cases (1-3):** Structure and consistency improved significantly. Emails correctly referenced only stated details and included appropriate next steps.
- **Edge case — sparse notes (4):** V1 fabricated entire conversations; V3 produced a brief, honest email without invented specifics.
- **Edge case — objection-heavy (5):** V3 adopted a respectful, non-pushy tone and delivered the promised case study. V1 was overly aggressive.
- **Failure case — contradictions (6):** V3 produced a conservative email and flagged contradictions for review. V1 confidently stated contradictory things.
- **Failure case — sensitive info (7):** V3 omitted layoff details, lawsuit mention, and leaked pricing. V1 included all of them.

## Where the Prototype Still Fails

The system is not reliable enough to send emails without human review. Specific weaknesses:
- On heavily contradictory inputs, the output is safe but too vague to be useful — a human still needs to rewrite substantially.
- The review-flags section occasionally over-flags normal cases, which could cause flag fatigue.
- Tone calibration is imperfect — the model sometimes uses slightly pushy language on objection-heavy calls despite instructions to be gentle.
- The system has no memory of prior interactions with a prospect, so it cannot reference relationship history beyond what is in the current notes.
- The model sometimes adds a subject line even though the prompt does not explicitly request one. While useful, this is an example of the model going beyond the stated instructions — something to be aware of when evaluating output consistency.

## Deployment Recommendation

I would recommend deploying this as a **draft-assist tool** with mandatory human review before sending — not as a fully automated email sender. Under these conditions:
- **Deploy:** As a time-saving first-draft tool integrated into a CRM, where the rep reviews and edits before sending. The `[REVIEW FLAGS]` section helps reps know where to focus their review.
- **Do not deploy:** As a fully autonomous email sender. The sensitivity filtering and hallucination controls are good but not perfect, and a single email containing leaked confidential information or fabricated commitments could cause serious business harm.
- **Required guardrails:** Human approval before send, logging of all generated drafts for audit, and a feedback loop so reps can flag bad outputs for prompt improvement.
