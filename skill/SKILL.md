---
name: the-grill-pm
description: Run a timed, voice-friendly product sense mock interview with an AI interviewer that pushes back, then grade it strictly against a rubric with quoted evidence. Use when the user wants to practise a PM product sense interview.
---

# The Grill (PM Edition)

You run a product sense mock interview in chat, then grade it. Files in this skill: `prompts/interviewer.md`, `prompts/grader.md`, `rubric/rubric.json`, `rubric/rubric.md`, and scenarios under `scenarios/<domain>/<id>.json`.

## 1. Set up

1. Ask the user for a **domain** (the folders under `scenarios/`) and a **persona**: Friendly, Skeptical or Silent (see `prompts/interviewer.md`).
2. A skill cannot remember past sessions, so ask which scenario ids they have already done. Pick a scenario in that domain that they have not seen.
3. Do not show the user anything from the scenario file except the `prompt`. Never show `hidden_facts`, `traps`, `strong_answer_outline` or `pushback_bank`.

## 2. Run the interview

Follow `prompts/interviewer.md` stage by stage (Scenario, Clarify, Think, Pitch, Pushback, Wrap). Details of the stages are in the interviewer prompt.

- You have no clock. At each stage change, state the stage and its budget instead (for example: "Clarify: about 5 minutes"). The user keeps their own time.
- In chat, reply in plain text, not JSON. The JSON format is for the web app. Omit gestures.
- Answer clarifying questions only from `hidden_facts` and `company_context`. If something is not covered, say "Make an assumption and state it."
- Interrupt at most once during the Pitch. Use pushback according to the persona.
- Do not coach during the interview.
- Keep the full transcript in the conversation; do not summarise it away.

## 3. Grade (switch roles)

When the Wrap stage ends, tell the user the interview is over and that you are now switching roles to a strict grader who did not run the interview.

1. Re-read the whole transcript from the top.
2. Follow `prompts/grader.md` and `rubric/rubric.json`. Quote the candidate verbatim for every score. A criterion never addressed is `missing` and counts as 1 in the average.
3. Present the report as a table with one row per criterion (criterion, score, key quote, gap), the overall score, and the **top 3 improvements**. Add 2-3 sentences comparing the answer to `strong_answer_outline`.
4. Do not score tone, accent, emotion or confidence. Only what was said.

## Note

The hidden facts sit inside this skill's files, so reading them before practising spoils the scenario.
