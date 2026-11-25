# Report: public access test, The Grill (PM Edition)

## 1. Summary

- A **signed-out** visitor does not get the app. claude.ai shows "Sign in to view this page" in its place (Test A).
- The **outside, signed-in** visitor was **not tested**: a bot check blocked signing in to the test browser (Test B).
- So the main question is **still open**: we do not know whether an outside visitor gets `sample` (interviewer and grader) or `db` (saved history).
- The artifact was listed as **private** when its sharing setting was read (after Test A), so nothing here covers a public link.

## 2. Results table

| Visitor | `sample` | `tts` | `dictation` | `db` | `user` | Browser voice |
|---|---|---|---|---|---|---|
| Signed out | not tested (1) | not tested (1) | not tested (1) | not tested (1) | not tested (1) | not tested (1) |
| Outside, signed in | not tested (2) | not tested (2) | not tested (2) | not tested (2) | not tested (2) | not tested (2) |

1. The app did not load, so it never reported its features. In practice a signed-out visitor gets none of them.
2. Test B did not run.

| Visitor | Start a session? | Hear a voice? | Talk? | See their history? |
|---|---|---|---|---|
| Signed out | no, sign-in page | no | no | no |
| Outside, signed in | not tested | not tested | not tested | not tested |

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

Test B not run: no outside account signed in in the profile.

- **First attempt:** `~/.grill-test` was missing from the Windows home folder, and `~/.grill-test/outside-profile` from the Ubuntu WSL home folder. No browser was launched.
- **Second attempt:** the folder was created and a Playwright Chromium window was opened on `claude.ai/login` so a person could sign in by hand. The second account had been invited to the artifact by email. Cloudflare's "Verify you are human" check kept coming back (reported by the person) and the sign-in page was not reached. The check was not worked around.
- Consent prompt wording, interviewer reply, drill score, history after reload: none, not reached.

File: `docs/testing/2026-11-25-public-access/results-b.json`

## 5. Errors

The artifact's own frame never loaded, so there are no errors from it. These are from the claude.ai page around it. Page (uncaught) errors: none in any run.

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
| Step 3, opening the artifact in the outside profile | First the profile folder did not exist; then a bot check blocked the sign-in. |
| Step 4, the drill (no `results-b-drill.json`, no drill commit) | Test B did not load the artifact. |
| `b-loaded.png`, `b-consent.png`, `b-report.png` | Same reason. |

Other differences from the brief:

- Test A ran three times instead of once (see section 3).
- The local `origin` is `tomersela79/the-grill-pm`. GitHub reports it as the same repo as `tomerseladev/the-grill-pm` (same id, moved), so no second clone was made and `origin` was left as is.
- This report is at the repo root, as the brief says, although commit `b72de25` moved reports to `docs/reports`.

**To finish the test:** a person runs Test B by hand in an ordinary browser, signed in to the second account, and reports what they see. To cover a public visitor, the artifact must first be shared with anyone who has the link; an email invite only covers an invited visitor.

Also note: the app can save history in the browser as well as to the account, so a drill that is still listed after a reload does not prove it was saved to the account. Checking for it in a second browser does.

## 7. Commits

| Hash | Message |
|---|---|
| `3dc39f3` | test: public access test setup |
| `a1782a8` | test: signed-out visitor results |
| `c6250c2` | test: outside visitor load results |
| `ff19bb0` | docs: public access findings |
| `1f9b6df` | docs: public access test report |
| (this update) | docs: record blocked sign-in and private sharing |
