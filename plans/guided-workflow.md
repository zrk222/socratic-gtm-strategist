# Plan: guided-workflow
Spec: specs/guided-workflow.md
Architect verdict: PASS

## Tasks
- [x] T1 | slice=ui | files=ui/index.html,ui/prep-ui.js,ui/prep.css,tests/guided_browser.cjs | verify=`node tests/guided_browser.cjs` | Funnel first use through idea, questions, direct practice and next steps.
- [x] T2 | slice=scripts | files=scripts/generate_dashboard.py | verify=`python -m unittest discover tests -q` | Explain the optional scenario calculator and link to the workspace.
- [x] T3 | slice=tests | files=tests/browser_smoke.cjs,tests/prep_browser.cjs | verify=`node tests/prep_browser.cjs` | Exercise optional controls through their disclosure while preserving regression scope.

## Review authority
Codex local review under the user's explicit request to simplify and funnel.
No independent human, merge or deployment approval is claimed.
