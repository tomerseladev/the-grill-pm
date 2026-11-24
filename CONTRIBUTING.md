# Contributing

## Add a scenario

1. Copy the shape in [`scenarios/schema.md`](scenarios/schema.md) into `scenarios/<domain>/<id>.json`. The file name must match the `id`.
2. Use fictional companies only. Never name a real company, and mark invented numbers with `"fictional_data": true`.
3. Run `python scripts/validate.py` until it prints `OK`.
4. Open a pull request. Leave `reviewed_by_human` as `false`.

## Propose rubric changes

Open an issue first, describing the criterion, the problem, and the change you suggest. Rubric changes affect every scenario and the grader, so they are discussed before any pull request.
