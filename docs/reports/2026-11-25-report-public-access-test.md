# Report: public access test, The Grill (PM Edition)

## 1. Summary

- A **signed-out** visitor does not get the app. claude.ai shows "Sign in to view this page" in its place (Test A).
- A **second account invited as Viewer** gets the interviewer and grader (`sample`) and can complete a drill, with no Claude voice and no mic. Before the fix, **its history did not survive a reload**, although the page said "saves: account" (Test B, run in ordinary Chrome).
- Likely cause: Viewers may not write to the database; the app did not notice, and showed empty history on the next load.
- **Fixed and retested:** artifact Version 42 keeps such sessions in the browser and says "saves: this browser". On 2026-11-26 a drill by the same account was still listed after a reload. The history stays in that browser only.
- **From the docs, not tested here:** The platform docs say every signed-in visitor from outside the organization, by public link or by email invitation, can read the database but never write to it. The one exception is an outside Editor. So by the docs, outside visitors cannot save history to their account at all. Inside the organization, a Contributor or above can.
- **Still open:** whether the artifact can be shared by public link, and what a public-link visitor sees in practice.
- The artifact was listed as **private** when its sharing setting was read (after Test A), so nothing here covers a public link. Test B's account was invited by email.

## 2. Results table

| Visitor | `sample` | `tts` | `dictation` | `db` | `user` | Browser voice |
|---|---|---|---|---|---|---|
| Signed out | not tested (1) | not tested (1) | not tested (1) | not tested (1) | not tested (1) | not tested (1) |
| Outside, signed in (invited Viewer) | yes | no | no | read only; history kept in the browser since the fix (2) | yes | yes |

1. The app did not load, so it never reported its features. In practice a signed-out visitor gets none of them.
2. Before the fix the page said "saves: account", but the drill was gone after a reload. Since the fix the page says "saves: this browser" and the drill stays. These cells are worked out from the status text and the app's code; the caps JSON was not read.

| Visitor | Start a session? | Hear a voice? | Talk? | See their history? |
|---|---|---|---|---|
| Signed out | no, sign-in page | no | no | no |
| Outside, signed in (invited Viewer) | yes | browser voice only (not heard: the drill ran in Text only) | no mic | before the fix, no: the drill disappeared after a reload. Since the fix, yes, in the same browser only |

## 3. Test A details

- **Setup:** Python Playwright 1.65.2, Chromium 159.0.8154.6, headed, fresh empty context.
- **URL opened:** `https://claude.ai/artifact/B9iFzSdxxHZqoypJW85VV3` (HTTP 200)
- **Final URL (saved run):** the same; it did not redirect.
- **What rendered:** not the artifact. Page title `Sign in – Claude`, text `Sign in to view this page` and a `Sign in` button. No frame contained `#status`.
- **Status text:** none. **Caps JSON:** none. **Start button:** not present. **`#noAI` notice:** not present.
- **Why:** claude.ai answered `401` for the artifact's content (`/api/frame/5232c360-29ed-4764-9896-7acae003093a`). That answer did not carry Cloudflare's bot-check marker. Later requests in the same load did get bot-check answers (403).

The test ran three times; the saved files are from run 3.

| Run | Result |
|---|---|
| 1 (20:12) | Went to `https://claude.ai/login`, then a Cloudflare bot check ("Performing security verification"). |
| 2 (20:13) | Same as run 1. Rerun to record which answers came from the bot layer. |
| 3 (20:15) | Stayed on the artifact URL, "Sign in to view this page", no bot check page. Rerun after fixing a URL-shortening bug in the script. |

The sharing setting was read after Test A, the same evening: the artifact service listed the artifact as **private**, with email invites to people outside the organization available. It was not read before Test A, but a private artifact would explain the sign-in page. So Test A most likely shows what a signed-out visitor gets for a private artifact. It does **not** show what a public link gives. The service also notes that a public link can be unavailable for some features a page uses; the Share menu gives the reason.

The bot check was never clicked or worked around by the script. While the runs were going, the developer noticed the check in the Playwright window and asked about it.

Files: `docs/testing/2026-11-25-public-access/results-a.json`, `docs/testing/2026-11-25-public-access/screens/a-signed-out.png`

## 4. Test B details

**First run, before the fix (2026-11-25, 20:29 to 20:33, developer's ordinary Chrome, second account, Viewer):**

- **Method:** Claude in Chrome extension in a new tab. The developer had signed in and the account had been invited by email. Not Playwright, because the profile could not be signed in (below).
- **URL / rendered:** the artifact loaded at its URL. The app bar said "Viewer" and "You can't edit this artifact."
- **Status text:** `Ready · voice: browser · mic: off · saves: account`
- **Caps (derived):** `sample` true, `tts` false, `dictation` false, `db` true, `user` true, `browserVoice` true. The caps JSON was not read.
- **Start button:** enabled. **`#noAI` notice:** not shown.
- **Consent prompt:** none seen at load, at start, at reply or at grading.
- **Opening question:** `How would you know this worked? Give me one main metric, and one thing you would watch so it does not backfire.`
- **Interviewer's reply:** `Let me make sure I follow. In this scenario, who are the reporters, and how does weekly active reporters tell us that more employee accounts are protected by MFA and that companies are keeping it on?`
- **Score:** `1.5 / 5`. **Report line:** `Customers who never switch on MFA · Friendly · drill: Success metrics · median of 3 grading passes`
- **Score note:** the brief's answer was written for another scenario, and the grader said so.
- **History after reload:** no. Listed under "Your progress" after New session; gone after reloading, and after a second reload (checked at 16, 26 and 20 seconds).
- **Likely cause:** The platform docs say that Viewers can never write to the artifact's database, their own private data included. In the app's code, when a save is refused it keeps the session in the browser only, but on the next load the database answers normally with nothing in it, so the app shows an empty history and never looks at the browser copy. The status label says "saves: account" because it only checks that the database and the user id exist. The refused save itself was not captured (network recording started after the drill); the read on reload was captured and returned 200.

**The fix (artifact Version 42, published 2026-11-25):** when a save to the account is refused, or gets no answer within 10 s, the app keeps the session in this browser under a key for the signed-in account, and on load it reads both the account and the browser copy. The status says "saves: account" only when the platform says the visitor may write, or a save to the account has worked; otherwise "saves: this browser". Before publishing, it was checked against a stand-in for the platform: outside viewer, organization viewer, owner, outside editor, no database, and a save that never answers all kept the drill after a reload, and a second account in the same browser saw none of the first account's sessions. The app's source is not in this repo; the fix lives in the artifact.

**Retest after the fix (2026-11-26, 09:37 to 09:39, same account, same Chrome):**

- **Status text at load:** `Ready · voice: browser · mic: off · saves: this browser`. No history listed at the start.
- **Scenario:** `Getting employees to report phishing` (Cybersecurity, human risk, easy). The brief's answer fits it this time.
- **Opening question:** `How would you know this worked? Give me one main metric, and one thing you would watch so it does not backfire.` It appeared after the answer had been sent (the answer went in right after the briefing).
- **Interviewer's reply (pushback):** `Weekly active reporters counts people, not threats. If that number doubles but the share of real malicious emails that get reported barely moves, would you call it a success? What would you measure instead, or alongside it?`
- **Score:** `2.5 / 5`. **Report line:** `Getting employees to report phishing · Friendly · drill: Success metrics · median of 3 grading passes`
- **Status after the report:** still `saves: this browser`.
- **History after reload:** **yes.** Listed under "Your progress" after New session, and still listed with the same score about 8 seconds after reloading.
- **Not checked:** the refused save itself (network not recorded), the browser copy itself (the app's frame cannot be read), and another browser or device, where this history will not appear. The 1.5 drill lost before the fix did not come back.
- **Side note:** the timer read 04:30 before the opening question and 04:51 after it, so it may restart when the question appears (not checked).

Files: `results-b-fixed.json` and the `b-fixed-*.png` screenshots in `screens/` (account avatar masked).

**Why the Playwright profile was not used:**

- **First attempt:** `~/.grill-test` was missing from the Windows home folder, and `~/.grill-test/outside-profile` from the Ubuntu WSL home folder. No browser was launched.
- **Second attempt:** the folder was created and a Playwright Chromium window was opened on `claude.ai/login` so a person could sign in by hand. The second account had been invited to the artifact by email. Cloudflare's "Verify you are human" check kept coming back (reported by the person) and the sign-in page was not reached. The check was not worked around.

Files: `docs/testing/2026-11-25-public-access/results-b.json`, `results-b-drill.json`, and the `b-*.png` screenshots in `screens/` (account avatar masked).

## 5. Errors

**Test B:** no error was shown on the page. Console recording started after the drill; a reload recorded no console errors, but the extension may not cover the app's frame. The database read on that reload returned 200. The drill's own save request was not captured.

**Test A:** the artifact's own frame never loaded, so there are no errors from it. These are from the claude.ai page around it. Page (uncaught) errors: none in any run.

**Run 3 (saved), all console errors:**

```
Failed to load resource: the server responded with a status of 403 ()   [https://claude.ai/api/account]
Failed to load resource: the server responded with a status of 401 ()   [https://claude.ai/api/frame/5232c360-29ed-4764-9896-7acae003093a]
Failed to load resource: the server responded with a status of 403 ()   [https://claude.ai/api/frame/telemetry]
Failed to load resource: the server responded with a status of 403 ()   [https://claude.ai/api/frame/5232c360-29ed-4764-9896-7acae003093a]
Failed to load resource: the server responded with a status of 403 ()   [https://claude.ai/api/frame/telemetry]
```

**Run 1 (not saved), all 29 console errors, repeats grouped:**

```
1x  Failed to load resource: the server responded with a status of 403 ()   [https://claude.ai/api/account]
1x  Unrecognized Content-Security-Policy directive 'webrtc'.   [https://5232c360-29ed-4764-9896-7acae003093a.frame.claudeusercontent.com/_warmup]
1x  Failed to load resource: the server responded with a status of 401 ()   [https://claude.ai/api/frame/5232c360-29ed-4764-9896-7acae003093a]
1x  Failed to load resource: the server responded with a status of 403 ()   [https://claude.ai/api/frame/telemetry]
3x  Failed to load resource: the server responded with a status of 403 ()   [https://claude.ai/login]
```

The other 22, all from the bot check's own page (`challenges.cloudflare.com`):

```
7x  Connecting to 'data:,' violates the following Content Security Policy directive: "connect-src 'self' https://hagen.challenges.cloudflare.com https://brunhild.challenges.cloudflare.com https://*.alg13.dnstest.challenges.cloudflare.com https://*.mldsa44.dnstest.challenges.cloudflare.com https://dnstest.dev https://ca2.cloudflarecaptcha.com https://ca1.cloudflarecaptcha.com". The action has been blocked.
3x  Fetch API cannot load data:,. Refused to connect because it violates the document's Content Security Policy.
6x  %c%d font-size:0;color:transparent NaN
6x  %c%o font-size:0;color:transparent {}
```

Run 2 showed the same kinds of messages (without the `webrtc` one); its full list was overwritten by run 3.

## 6. Skipped steps

| Step | Why |
|---|---|
| Step 3 and 4 in the Playwright profile | First the profile folder did not exist; then a bot check blocked the sign-in. Done in ordinary Chrome instead. |
| `b-consent.png` | No consent prompt was seen. |
| Reading the caps JSON and console errors from the app frame | The extension cannot read the cross-origin frame; caps were worked out from the status text. |

Other differences from the brief:

- Test A ran three times instead of once (see section 3).
- The local `origin` is `tomersela79/the-grill-pm`. GitHub reports it as the same repo as `tomerseladev/the-grill-pm` (same id, moved), so no second clone was made and `origin` was left as is.
- The brief asked for this report at the repo root. It was first written there, then moved to `docs/reports`, where the repo keeps its reports (commit `b72de25`).

**To finish the test:** share the artifact with anyone who has the link and repeat Test B as a public visitor. The history fix is done and retested (section 4).

## 7. Commits

| Hash | Message |
|---|---|
| `3dc39f3` | test: public access test setup |
| `a1782a8` | test: signed-out visitor results |
| `c6250c2` | test: outside visitor load results |
| `ff19bb0` | docs: public access findings |
| `1f9b6df` | docs: public access test report |
| `cfa347d` | docs: record blocked sign-in and private sharing |
| `958cb2b` | test: outside viewer load and drill results in Chrome |
| `7252d9a` | docs: outside viewer findings and report |
| `a5563f6` | docs: correct who can save history to the account |
| `58587cb` | test: live drill after the history fix |
| (this update) | docs: move public access report to docs/reports |
