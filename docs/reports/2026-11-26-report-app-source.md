# Report: web app source in the-grill-pm

## 1. Summary

- The template and build script are in `artifact/`, and both committed copies match the brief's sha256 values.
- Built on Windows, the page **does not match** the live page's sha256. The only difference is line endings: `build.py` writes in text mode, so Windows Python turns every LF into CRLF. With CRLF changed to LF, the built page is byte-identical to the live `index.html`.
- Both READMEs are updated, and `master` is pushed to `tomerseladev/the-grill-pm`. The remote hash matches the local one.

## 2. Files added

| Repo path | sha256 of the committed copy | Matches the table |
|---|---|---|
| `artifact/template.html` | `f3278aee3460d2983c4830ebbb86d681454dc8a8164707c30fc15f814f1fe3e4` | yes |
| `artifact/build.py` | `098bcbed7411f60fc4bdcba6f2c1bdc39a47524056cfa60fd8fe03999da6048b` | yes |

Both files were read from the artifact (version `1795680829-da05`) and copied without changes. They have LF line endings, so no amend was needed. The working copies have the same hashes as the committed ones.

## 3. Build check

- Command, from the repo root, with the output in a temp folder outside the repo:
  `python artifact/build.py . artifact/template.html <temp>/index.html`
- Python 3.14.4 on Windows 11. Output: `wrote …/index.html: 176 KB, 8 scenarios`.
- Built page: sha256 `64c5317a0fa3e9f37d774197681fb5509f980acc4d9469fcfdd78caab8fd57fd`, 181,498 bytes. **No match** with the live page, `aab73b36b2a70279b4b87c7f3e9410ad713b100312d31d327f9a532b337d433b` (180,400 bytes).
- The difference: the built page has 1,098 CR and 1,098 LF; the live page has 0 CR and 1,098 LF. All 1,098 lines differ by their trailing CR only. The first lines that differ (`diff built live | cat -A`):

  ```
  1,1098c1,1098$
  < <!DOCTYPE html>^M$
  < <html lang="en">^M$
  < <head>^M$
  < <meta charset="utf-8">^M$
  ```

- `diff --strip-trailing-cr` finds no differences. The built page with CRLF changed to LF has sha256 `aab73b36b2a70279b4b87c7f3e9410ad713b100312d31d327f9a532b337d433b`, which is the live page exactly.
- Cause: `build.py` writes with `open(out, "w", encoding="utf-8")`, so on Windows Python writes CRLF. Adding `newline="\n"` to that call would give the live page's bytes on any OS. That change was **not** made: the brief says to copy `build.py` exactly as it is.
- The built `index.html` was not committed.

## 4. README changes

**`artifact/README.md`:** the whole file is replaced with the text from the brief. It has a link to the app, what each file is, the build command, a table of what visitors get, a link to the public access findings, and how to change the app. The findings link points to `docs/testing/2026-11-25-public-access/`, which exists.

**`README.md`:** four changes, nothing else:

1. Try it: `- **Web app:** coming soon.` now links to the app and says it needs a Claude account and runs on your own Claude usage.
2. Stage table: the Think budget is now `3 min (5 or 8 in practice)`.
3. A new Modes paragraph after the Personas line: Practice, Assisted, Exam and Drill.
4. Folder table: `artifact/` is now `Web app source: HTML template and build script`.

## 5. Problems

- **Build hash does not match on Windows.** See section 3: the cause is line endings only, and the content is identical.
- **Tool name.** The brief names a `read_file` tool from "claude-artifacts", which this session did not have. The files were read with the Artifact tool's `read` action instead (`url` `https://claude.ai/artifact/B9iFzSdxxHZqoypJW85VV3`, `paths` `["src/template.html", "src/build.py.txt", "index.html"]`). It saved each file whole and reported the same sha256 values as the brief. The artifact was only read, never published.
- On `git add`, Git warned (no action needed): `warning: in the working copy of 'artifact/template.html', LF will be replaced by CRLF the next time Git touches it`. The same warning appeared for `artifact/build.py`, `artifact/README.md` and `README.md`. The committed copies keep LF.
- Nothing else went wrong. `git remote set-url` and `git fetch` worked against `tomerseladev/the-grill-pm`.

## 6. Commits

| Hash | Message |
|---|---|
| `07d2697` | `artifact: add web app source (template and build script)` |
| `9483757` | `docs: artifact README` |
| `d908bcc` | `docs: README points to the live app` |

This report is committed after these as `docs: app source report`.

After the push in Step 5, remote `master` and local `master` were both `d908bccc5af706ab690832d4af1b4376e5b9dcbd`.
