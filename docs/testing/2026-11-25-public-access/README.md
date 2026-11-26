# Public access test, 2026-11-25

What does someone get when they open The Grill (PM Edition) from its public link?

Artifact: <https://claude.ai/artifact/B9iFzSdxxHZqoypJW85VV3>

## Short answer

- **Signed-out visitor:** does not get the app. claude.ai shows "Sign in to view this page" instead.
- **Visitor signed in to a second Claude account, invited as Viewer:** gets the interviewer and grader (`sample`) and can run a full drill. No Claude voice and no mic. Before the fix, **their history did not survive a reload**, although the page said "saves: account". **Since the fix (artifact Version 42) it does, in the same browser:** the page says "saves: this browser", and a drill run on 2026-11-26 was still listed after a reload.
- **The artifact was private** when its sharing setting was read (after Test A), so no test here covers a public link.
- **From the docs, not tested here:** The platform docs say every signed-in visitor from outside the organization, by public link or by email invitation, can read the database but never write to it. The one exception is an outside Editor. So by the docs, outside visitors cannot save history to their account at all. Inside the organization, a Contributor or above can.
- **Still open:** whether the artifact can be shared by public link at all, and what a public-link visitor sees in practice.

## Features by visitor

| Visitor | `sample` | `tts` | `dictation` | `db` | `user` | Browser voice |
|---|---|---|---|---|---|---|
| Signed out | not tested (1) | not tested (1) | not tested (1) | not tested (1) | not tested (1) | not tested (1) |
| Outside, signed in (invited Viewer) | yes | no | no | read only; history kept in the browser since the fix (2) | yes | yes |

1. The app did not load, so it never reported its features. In practice a signed-out visitor gets none of them.
2. Before the fix the page said "saves: account", but the drill was gone after a reload. Since the fix the page says "saves: this browser" and the drill stays. See Test B. The `sample`, `tts`, `dictation`, `db`, `user` and browser voice cells are worked out from the status text and the app's code; the caps JSON itself was not read.

## What each visitor can do

| Visitor | Start a session? | Hear a voice? | Talk? | See their history? |
|---|---|---|---|---|
| Signed out | no, sign-in page | no | no | no |
| Outside, signed in (invited Viewer) | yes | browser voice only (not heard in this test: the drill ran in Text only) | no mic | before the fix, no: the drill disappeared after a reload. Since the fix, yes, in the same browser only |

## Test A: signed-out visitor

The test ran three times in a fresh, empty browser context (Playwright Chromium, headed). The app did not load in any of them.

| Run | What happened |
|---|---|
| 1 (20:12) | The artifact page opened, then the browser went to `claude.ai/login`, where a Cloudflare bot check appeared. |
| 2 (20:13) | Same as run 1. |
| 3 (20:15) | The browser stayed on the artifact URL and showed "Sign in to view this page". No bot check page. **This is the saved result.** |

In all three runs, claude.ai's own answer for the artifact's content was `401` before any bot check page appeared, and that answer did not carry Cloudflare's bot-check marker (the marker was recorded in runs 2 and 3 only). The bot checks were not clicked or worked around. Runs 1 and 2 were overwritten by run 3; the script was also changed between runs to record more detail.

The sharing setting was read after Test A, the same evening: the artifact service listed the artifact as **private**, with email invites to people outside the organization available. It was not read before Test A, but a private artifact would explain the sign-in page. So Test A most likely shows what a signed-out visitor gets for a private artifact. It does **not** show what a public link gives. The service also notes that a public link can be unavailable for some features a page uses; the Share menu gives the reason.

- Screenshot: [screens/a-signed-out.png](screens/a-signed-out.png)
- Data: [results-a.json](results-a.json)

## Test B: outside visitor (invited Viewer)

Run in the developer's ordinary Chrome, where the developer had signed in to a second account that was invited to the artifact as **Viewer**. This is an invited viewer, not a public-link visitor, and it is not the Playwright profile the brief describes.

**First run, 2026-11-25, before the fix:**

- Status text: `Ready · voice: browser · mic: off · saves: account`
- No permission prompt was seen at any step.
- A Success metrics drill ran: the interviewer asked, replied to the answer, and the grader scored it **1.5 / 5**. (The brief's answer was written for a different scenario, which the grader pointed out.)
- Report line: `Customers who never switch on MFA · Friendly · drill: Success metrics · median of 3 grading passes`
- After **New session** the drill was listed under "Your progress". After reloading the page it was **gone**, and stayed gone after a second reload.

**Likely cause:** The platform docs say that Viewers can never write to the artifact's database, their own private data included. In the app's code, when a save is refused it keeps the session in the browser only, but on the next load the database answers normally with nothing in it, so the app shows an empty history and never looks at the browser copy. The status label says "saves: account" because it only checks that the database and the user id exist. The refused save itself was not captured (network recording started after the drill); the read on reload was captured and returned 200.

So, before the fix, the app told a Viewer their sessions were saved when they were not. The platform docs say every signed-in visitor from outside the organization, by public link or by email invitation, can read the database but never write to it. The one exception is an outside Editor. So by the docs, outside visitors cannot save history to their account at all. Inside the organization, a Contributor or above can. (An earlier version of this page suggested a Contributor might keep history; for an outside account that is wrong.)

- Screenshots: [b-loaded](screens/b-loaded.png), [b-reply](screens/b-reply.png), [b-report](screens/b-report.png), [history before reload](screens/b-history-before-reload.png), [history after reload](screens/b-history-after-reload.png)
- Data: [results-b.json](results-b.json), [results-b-drill.json](results-b-drill.json)

**The fix (artifact Version 42, published 2026-11-25).** When a save to the account is refused, or gets no answer within 10 s, the app keeps the session in this browser under a key for the signed-in account, and on load it reads both the account and the browser copy. The status says "saves: account" only when the platform says the visitor may write, or a save to the account has worked; otherwise it says "saves: this browser". The app's source is not in this repo; the fix lives in the artifact.

**Retest after the fix, 2026-11-26 (same account, same Chrome):**

- Status text at load: `Ready · voice: browser · mic: off · saves: this browser`. No history was listed at the start.
- A Success metrics drill on "Getting employees to report phishing" (Friendly, Text only) scored **2.5 / 5**. The brief's answer fits this scenario; the grader's main point was that weekly active reporters counts people, not threats caught.
- After **New session** the drill was listed under "Your progress". After reloading the page it was **still listed**, with the same score.
- The 1.5 drill lost before the fix did not come back.
- Not checked: the refused save itself (network not recorded), the browser copy itself (the app's frame cannot be read), and another browser or device, where this history will not appear.
- Side note: the answer went in before the opening question appeared, and the question was posted after it. The timer read 04:30 before the question and 04:51 after it, so it may restart when the question appears (not checked).
- Screenshots: [report](screens/b-fixed-report.png), [history before reload](screens/b-fixed-history-before-reload.png), [history after reload](screens/b-fixed-history-after-reload.png)
- Data: [results-b-fixed.json](results-b-fixed.json)

**Earlier attempts.** Playwright could not be used: no outside account signed in in the profile. The first time, the folder `~/.grill-test/outside-profile` did not exist. Later it was created and a Playwright Chromium window was opened so a person could sign in by hand with a second account, but Cloudflare's "Verify you are human" check kept coming back (reported by the person) and the sign-in page was not reached. The check was not worked around. 

Next step: check what a public link gives. The history fix is live and retested above.
