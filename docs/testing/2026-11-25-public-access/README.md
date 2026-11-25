# Public access test, 2026-11-25

What does someone get when they open The Grill (PM Edition) from its public link?

Artifact: <https://claude.ai/artifact/B9iFzSdxxHZqoypJW85VV3>

## Short answer

- **Signed-out visitor:** does not get the app. claude.ai shows "Sign in to view this page" instead.
- **Visitor signed in to an outside Claude account:** not tested. The browser profile with the outside account was not on the test machine.
- So the main question is **still open**: we do not know whether an outside, signed-in visitor gets the interviewer (`sample`) or saved history (`db`).

## Features by visitor

| Visitor | `sample` | `tts` | `dictation` | `db` | `user` | Browser voice |
|---|---|---|---|---|---|---|
| Signed out | not tested (1) | not tested (1) | not tested (1) | not tested (1) | not tested (1) | not tested (1) |
| Outside, signed in | not tested (2) | not tested (2) | not tested (2) | not tested (2) | not tested (2) | not tested (2) |

1. The app did not load, so it never reported its features. In practice a signed-out visitor gets none of them.
2. Test B did not run. The platform docs say outside visitors get no `tts` and no `dictation`; this test neither confirms nor contradicts that.

## What each visitor can do

| Visitor | Start a session? | Hear a voice? | Talk? | See their history? |
|---|---|---|---|---|
| Signed out | no, sign-in page | no | no | no |
| Outside, signed in | not tested | not tested | not tested | not tested |

## Test A: signed-out visitor

The test ran three times in a fresh, empty browser context (Playwright Chromium, headed). The app did not load in any of them.

| Run | What happened |
|---|---|
| 1 (20:12) | The artifact page opened, then the browser went to `claude.ai/login`, where a Cloudflare bot check appeared. |
| 2 (20:13) | Same as run 1. |
| 3 (20:15) | The browser stayed on the artifact URL and showed "Sign in to view this page". No bot check page. **This is the saved result.** |

In all three runs, claude.ai's own answer for the artifact's content was `401` before any bot check page appeared, and that answer did not carry Cloudflare's bot-check marker (the marker was recorded in runs 2 and 3 only). The bot checks were not clicked or worked around. Runs 1 and 2 were overwritten by run 3; the script was also changed between runs to record more detail.

What this does not settle: whether claude.ai asks every signed-out visitor to sign in, or only does so because of how this artifact is shared. The sharing setting was not checked.

- Screenshot: [screens/a-signed-out.png](screens/a-signed-out.png)
- Data: [results-a.json](results-a.json)

## Test B: outside visitor

Not run: no outside account signed in in the profile. The folder `~/.grill-test/outside-profile` does not exist on the test machine. The drill was skipped for the same reason. There are no Test B screenshots.

- Data: [results-b.json](results-b.json)

To run the load part of Test B once the profile exists (the drill and the consent prompt are not in the script yet):

```
python run_test.py --label b --profile ~/.grill-test/outside-profile --shot screens/b-loaded.png --out results-b.json
```
