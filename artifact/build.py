"""Build the single-page app from the repo's content files.

Usage: python3 build.py <repo_dir> <template> <out_html>
Embeds rubric/rubric.json, prompts/interviewer.md, prompts/grader.md and every
scenarios/*/*.json into the template's /*__DATA__*/ placeholder.
"""
import json, sys, glob, os

repo, tpl, out = sys.argv[1:4]
scen = []
for p in sorted(glob.glob(os.path.join(repo, "scenarios", "*", "*.json"))):
    with open(p, encoding="utf-8") as f:
        scen.append(json.load(f))
data = {
    "rubric": json.load(open(os.path.join(repo, "rubric", "rubric.json"), encoding="utf-8")),
    "interviewer": open(os.path.join(repo, "prompts", "interviewer.md"), encoding="utf-8").read(),
    "grader": open(os.path.join(repo, "prompts", "grader.md"), encoding="utf-8").read(),
    "scenarios": scen,
}
blob = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
html = open(tpl, encoding="utf-8").read().replace("/*__DATA__*/", blob)
open(out, "w", encoding="utf-8").write(html)
print(f"wrote {out}: {len(html)//1024} KB, {len(scen)} scenarios")
