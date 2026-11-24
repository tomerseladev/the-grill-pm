# Scenario schema

One JSON file per scenario at `scenarios/<domain>/<id>.json`.

```json
{
  "id": "cyber-001",
  "version": 1,
  "domain": "cybersecurity",
  "sub_domain": "security-operations",
  "difficulty": "medium",
  "time_budget_minutes": 25,
  "title": "short title",
  "prompt": "What the candidate sees and hears. 60-120 words. Fictional company.",
  "company_context": "2-4 sentences about the fictional company, shown on request only",
  "hidden_facts": [
    {"topic": "users", "question_hint": "who uses it", "fact": "...", "fictional_data": true}
  ],
  "traps": [
    {"trap": "jumping to solutions before choosing a user", "probe": "the question the interviewer asks when it happens"}
  ],
  "strong_answer_outline": {
    "clarify_goal": "...", "user_segment": "...", "pain_points": "...", "solutions": "...",
    "tradeoffs": "...", "metrics": "...", "structure": "...", "pushback": "..."
  },
  "pushback_bank": ["5 or more pressure questions specific to this scenario"],
  "reviewed_by_human": false
}
```

## Constraints

- `id` is unique across all scenarios and matches the file name (`<id>.json`).
- `difficulty` is one of `easy`, `medium`, `hard`.
- `prompt` is 60-120 words and uses a fictional company.
- `hidden_facts`: at least 8, covering at least these topics: `users`, `business_goal`, `market`, `constraints`, `current_product`, `data_metrics`, `competition`, and `timeline_resources`.
- `fictional_data: true` marks numbers and facts that are scenario data, not real-world statistics.
- `traps`: 3 to 5.
- `pushback_bank`: at least 5 questions specific to the scenario.
- The keys of `strong_answer_outline` are exactly the 8 rubric criterion ids in `rubric/rubric.json`: `clarify_goal`, `user_segment`, `pain_points`, `solutions`, `tradeoffs`, `metrics`, `structure`, `pushback`.
- `reviewed_by_human` stays `false` until a person has reviewed the scenario.

Run `python scripts/validate.py` before opening a PR.
