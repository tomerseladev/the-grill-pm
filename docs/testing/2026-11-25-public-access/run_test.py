"""Load the public artifact as a given kind of visitor and report what it got.

Signed-out visitor (fresh, empty context):
    python run_test.py --label a --shot screens/a-signed-out.png --out results-a.json

Signed-in visitor (existing Playwright profile folder):
    python run_test.py --label b --profile ~/.grill-test/outside-profile \
        --shot screens/b-loaded.png --out results-b.json

The script only loads the page and reads it. It never signs in, and it never
tries to get past a bot check: if one shows up, the result is "inconclusive".
"""

import argparse
import datetime
import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import Error, sync_playwright

ARTIFACT_URL = "https://claude.ai/artifact/B9iFzSdxxHZqoypJW85VV3"
HERE = Path(__file__).resolve().parent
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

BOT_CHECK = re.compile(
    r"just a moment|verify(ing)? (that )?you are (a )?human|security verification"
    r"|checking your browser|enable javascript and cookies to continue",
    re.I,
)
SIGN_IN_URL = re.compile(r"/(login|sign-?in|auth|oauth)\b", re.I)
SIGN_IN_TEXT = re.compile(
    r"continue with (google|email|apple|sso)|log in to|sign in to|enter your email", re.I
)

READ_STATE = """() => {
  const shown = el => {
    if (!el) return null;
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    return !el.hidden && s.display !== 'none' && s.visibility !== 'hidden'
           && r.width > 0 && r.height > 0;
  };
  const start = document.querySelector('#startBtn');
  const noAI = document.querySelector('#noAI');
  return {
    status_text: document.querySelector('#status')?.innerText.trim() ?? null,
    caps_raw: document.body.dataset.caps ?? null,
    start_button_present: !!start,
    start_button_enabled: start ? !start.disabled : null,
    start_button_text: start ? start.innerText.trim() : null,
    no_ai_notice_present: !!noAI,
    no_ai_notice_visible: shown(noAI),
    no_ai_notice_text: noAI ? noAI.innerText.trim() : null,
  };
}"""


def clean_url(url):
    """Drop query strings, and the long one-off tokens in bot-check URLs."""
    url = url.split("?")[0].split("#")[0]
    return re.sub(r"(challenge-platform/h/\w+/\w+/).*", r"\1...", url)


def redact(text):
    return EMAIL.sub("[email removed]", text) if text else text


def all_frames(page):
    return [f for f in page.frames if not f.is_detached()]


def find_artifact_frame(page, timeout_s):
    """Return the first frame (nested ones included) that contains #status."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        for frame in all_frames(page):
            try:
                if frame.query_selector("#status"):
                    return frame
            except Error:
                continue
        page.wait_for_timeout(500)
    return None


def body_text(page):
    try:
        return page.evaluate("() => document.body ? document.body.innerText : ''")
    except Error:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--profile", help="existing Playwright profile folder")
    ap.add_argument("--shot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--url", default=ARTIFACT_URL)
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--frame-wait", type=int, default=45)
    args = ap.parse_args()

    shot = HERE / args.shot
    shot.parent.mkdir(parents=True, exist_ok=True)
    viewport = {"width": 1280, "height": 900}

    result = {
        "label": args.label,
        "requested_url": args.url,
        "tested_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "browser": "Playwright Chromium, " + ("headless" if args.headless else "headed"),
        "profile": "persistent" if args.profile else "fresh empty context",
    }
    console_errors, page_errors, failed, navigations = [], [], [], []

    with sync_playwright() as p:
        if args.profile:
            folder = Path(args.profile).expanduser()
            if not folder.is_dir():
                sys.exit(f"profile folder not found: {folder}")
            browser = None
            ctx = p.chromium.launch_persistent_context(
                str(folder), headless=args.headless, viewport=viewport
            )
        else:
            browser = p.chromium.launch(headless=args.headless)
            ctx = browser.new_context(viewport=viewport)
        result["browser_version"] = (browser or ctx.browser).version if (
            browser or ctx.browser
        ) else None

        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on(
            "console",
            lambda m: console_errors.append(
                {"text": redact(m.text), "source": clean_url((m.location or {}).get("url", ""))}
            )
            if m.type == "error"
            else None,
        )
        page.on("pageerror", lambda e: page_errors.append(redact(str(e))))

        def on_response(r):
            if r.status < 400:
                return
            entry = {
                "status": r.status,
                "url": clean_url(r.url),
                # Cloudflare sets this header on its own challenge responses.
                "cf_mitigated": r.headers.get("cf-mitigated"),
                "content_type": r.headers.get("content-type"),
            }
            failed.append((entry, r))

        page.on("response", on_response)
        page.on(
            "framenavigated",
            lambda f: navigations.append(clean_url(f.url)) if f == page.main_frame else None,
        )

        try:
            resp = page.goto(args.url, wait_until="domcontentloaded", timeout=60000)
            result["http_status"] = resp.status if resp else None
            result["http_cf_mitigated"] = resp.headers.get("cf-mitigated") if resp else None
        except Error as e:
            result["navigation_error"] = redact(str(e))

        frame = find_artifact_frame(page, args.frame_wait)
        if frame:
            try:
                frame.wait_for_selector("body[data-caps]", timeout=15000)
            except Error:
                result["caps_note"] = "body[data-caps] did not appear within 15 s"
            state = frame.evaluate(READ_STATE)
            raw = state.pop("caps_raw")
            try:
                state["caps"] = json.loads(raw) if raw else None
            except ValueError:
                state["caps"] = raw
            result.update(state)
            result["artifact_frame_url"] = frame.url.split("?")[0]

        text = body_text(page)
        result["rendered"] = bool(frame)
        result["final_url"] = page.url.split("?")[0].split("#")[0]
        result["page_title"] = redact(page.title())
        result["bot_check_seen"] = not frame and (
            bool(result.get("http_cf_mitigated"))
            or bool(BOT_CHECK.search(page.title() or ""))
            or bool(BOT_CHECK.search(text))
        )
        result["sent_to_sign_in_url"] = not frame and bool(
            SIGN_IN_URL.search(result["final_url"])
        )
        result["sign_in_page_seen"] = not frame and bool(SIGN_IN_TEXT.search(text))
        if not frame:
            result["visible_text"] = redact(text[:1500])
            result["frame_hosts"] = sorted(
                {f.url.split("/")[2] for f in all_frames(page) if f.url.startswith("http")}
            )
        result["outcome"] = (
            "rendered"
            if frame
            else "sent to sign-in; a bot check hid the sign-in page"
            if result["bot_check_seen"] and result["sent_to_sign_in_url"]
            else "inconclusive: bot check"
            if result["bot_check_seen"]
            else "sign-in page"
            if result["sent_to_sign_in_url"] or result["sign_in_page_seen"]
            else "did not render"
        )
        page.screenshot(path=str(shot))
        result["screenshot"] = args.shot
        result["console_errors"] = console_errors
        result["page_errors"] = page_errors
        result["main_frame_navigations"] = navigations
        for entry, r in failed:
            if "json" in (entry["content_type"] or "") and "//claude.ai/" in entry["url"]:
                try:
                    entry["body"] = redact(r.text()[:400])
                except Error:
                    pass
        result["http_errors"] = [entry for entry, _ in failed]
        ctx.close()
        if browser:
            browser.close()

    out = json.dumps(result, indent=2, ensure_ascii=False)
    (HERE / args.out).write_text(out + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
