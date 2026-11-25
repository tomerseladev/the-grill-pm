# Report: five new scenarios

## 1. Summary

Five scenarios were added (three Fintech, two Cybersecurity), so the repo now has 4 Fintech and 4 Cybersecurity scenarios.
The committed files match the supplied text byte for byte, and `reviewed_by_human` is `false` in all five.
The validator passes and `master` is pushed.

## 2. Files added

| Path | Title |
|---|---|
| `scenarios/fintech/fin-002.json` | Small businesses abandon the loan application |
| `scenarios/fintech/fin-003.json` | Helping first-salary customers save |
| `scenarios/fintech/fin-004.json` | Card disputes that take weeks |
| `scenarios/cybersecurity/cyber-003.json` | Customers who never switch on MFA |
| `scenarios/cybersecurity/cyber-004.json` | A patching backlog nobody can finish |

None of the five existed before, so nothing was overwritten.

## 3. Validator output

```
OK 8 scenarios
```

It passed on the first run, so there is no `scenarios: fix copy errors` commit.

## 4. README changes

None needed. The README does not list the scenarios or give a count.

## 5. Problems

No errors. Four things to know:

- **Local clone:** an existing clone outside the home folder was used, instead of making a second one in `~/repos`.
- **Remote name:** the clone's `origin` still uses the old account name, `tomersela79`. GitHub redirected the push, which landed in the right repo:

  ```
  remote: This repository moved. Please use the new location:        
  remote:   https://github.com/tomerseladev/the-grill-pm.git        
  ```

- **Line endings:** Git on Windows (`core.autocrlf=true`) printed this warning for each of the five files. The committed files have LF line endings:

  ```
  warning: in the working copy of 'scenarios/cybersecurity/cyber-003.json', LF will be replaced by CRLF the next time Git touches it
  warning: in the working copy of 'scenarios/cybersecurity/cyber-004.json', LF will be replaced by CRLF the next time Git touches it
  warning: in the working copy of 'scenarios/fintech/fin-002.json', LF will be replaced by CRLF the next time Git touches it
  warning: in the working copy of 'scenarios/fintech/fin-003.json', LF will be replaced by CRLF the next time Git touches it
  warning: in the working copy of 'scenarios/fintech/fin-004.json', LF will be replaced by CRLF the next time Git touches it
  ```

- **Skill zip not rebuilt:** the latest release, v0.1.0, is still tagged at `371eec7`, before these files. Making a new release was not part of this task.

## 6. Commits

| Hash | Message |
|---|---|
| `474f5f31d75e5eeae8b6368115bcaa8dab017692` | `scenarios: add fin-002, fin-003, fin-004, cyber-003, cyber-004` |
| the commit that adds this file | `docs: new scenarios report` |

After the first push, `git ls-remote origin` showed `refs/heads/master` at `474f5f31d75e5eeae8b6368115bcaa8dab017692`, the same as local `master`. A commit cannot contain its own hash, so the report's hash is not listed here.
