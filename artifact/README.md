# Web app

The Grill (PM Edition) runs as a single web page, published as a Claude artifact:
**[Open the app](https://claude.ai/artifact/B9iFzSdxxHZqoypJW85VV3)**. It needs a Claude account. The AI interviewer, the grader and the voice run on each visitor's own Claude account, so the project has no servers and no API keys.

## Files

| File | What it is |
|---|---|
| `template.html` | The whole app: layout, styles and code, with a `/*__DATA__*/` placeholder |
| `build.py` | Embeds `rubric/`, `prompts/` and `scenarios/` into the template and writes the page |

## Build

From the repo root:

```
python artifact/build.py . artifact/template.html index.html
```

The output is the page that gets published. It is not kept in the repo.

## What visitors get

| Visitor | AI interviewer and grader | Voice | Mic | Saved history |
|---|---|---|---|---|
| The owner's organization | yes | Claude voice | yes, in Chromium browsers | in their Claude account |
| Anyone else with access | yes | the browser's own voice | no | in their own browser only |

Findings: [`docs/testing/2026-11-25-public-access/`](../docs/testing/2026-11-25-public-access/).

## Changing the app

Edit `template.html`, build, and open the output in a browser to check it. Publishing to the live artifact is done by the maintainer.
