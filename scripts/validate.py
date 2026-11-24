#!/usr/bin/env python3
"""Validate scenarios and the rubric. Standard library only."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIFFICULTIES = {"easy", "medium", "hard"}
REQUIRED_TOPICS = {
    "users", "business_goal", "market", "constraints",
    "current_product", "data_metrics", "competition", "timeline_resources",
}
TOP_KEYS = {
    "id", "version", "domain", "sub_domain", "difficulty", "time_budget_minutes",
    "title", "prompt", "company_context", "hidden_facts", "traps",
    "strong_answer_outline", "pushback_bank", "reviewed_by_human",
}


def load(path, errors):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{path.relative_to(ROOT)}: cannot parse JSON ({exc})")
        return None


def check_rubric(errors):
    path = ROOT / "rubric" / "rubric.json"
    if not path.exists():
        errors.append("rubric/rubric.json: missing")
        return None
    data = load(path, errors)
    if data is None:
        return None
    criteria = data.get("criteria")
    if not isinstance(criteria, list) or len(criteria) != 8:
        errors.append("rubric/rubric.json: must have exactly 8 criteria")
        return None
    ids = [c.get("id") for c in criteria]
    if len(set(ids)) != 8:
        errors.append("rubric/rubric.json: criterion ids must be unique")
    return set(ids)


def check_scenario(path, rubric_ids, errors, seen_ids):
    rel = path.relative_to(ROOT)
    s = load(path, errors)
    if s is None:
        return
    if not isinstance(s, dict):
        errors.append(f"{rel}: top level must be an object")
        return

    def err(msg):
        errors.append(f"{rel}: {msg}")

    missing = TOP_KEYS - set(s)
    if missing:
        err(f"missing keys: {sorted(missing)}")
        return
    sid = s["id"]
    if sid != path.stem:
        err(f"id '{sid}' does not match file name '{path.stem}'")
    if sid in seen_ids:
        err(f"duplicate id '{sid}'")
    seen_ids.add(sid)
    if s["domain"] != path.parent.name:
        err(f"domain '{s['domain']}' does not match folder '{path.parent.name}'")
    if s["difficulty"] not in DIFFICULTIES:
        err(f"difficulty must be one of {sorted(DIFFICULTIES)}")
    words = len(str(s["prompt"]).split())
    if not 60 <= words <= 120:
        err(f"prompt has {words} words, expected 60-120")
    if not isinstance(s["reviewed_by_human"], bool):
        err("reviewed_by_human must be a boolean")

    facts = s["hidden_facts"]
    if not isinstance(facts, list) or len(facts) < 8:
        err("hidden_facts must have at least 8 entries")
    else:
        topics = set()
        for i, f in enumerate(facts):
            if not isinstance(f, dict) or not {"topic", "question_hint", "fact", "fictional_data"} <= set(f):
                err(f"hidden_facts[{i}] needs topic, question_hint, fact, fictional_data")
                continue
            topics.add(f["topic"])
        gap = REQUIRED_TOPICS - topics
        if gap:
            err(f"hidden_facts missing topics: {sorted(gap)}")

    traps = s["traps"]
    if not isinstance(traps, list) or not 3 <= len(traps) <= 5:
        err("traps must have 3 to 5 entries")
    else:
        for i, t in enumerate(traps):
            if not isinstance(t, dict) or not {"trap", "probe"} <= set(t):
                err(f"traps[{i}] needs trap and probe")

    bank = s["pushback_bank"]
    if not isinstance(bank, list) or len(bank) < 5:
        err("pushback_bank must have at least 5 entries")

    outline = s["strong_answer_outline"]
    if not isinstance(outline, dict):
        err("strong_answer_outline must be an object")
    elif rubric_ids is not None and set(outline) != rubric_ids:
        err(f"strong_answer_outline keys must equal rubric ids {sorted(rubric_ids)}")


def main():
    errors = []
    rubric_ids = check_rubric(errors)
    files = sorted((ROOT / "scenarios").glob("*/*.json"))
    seen = set()
    for path in files:
        check_scenario(path, rubric_ids, errors, seen)
    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    print(f"OK {len(files)} scenarios")


if __name__ == "__main__":
    main()
