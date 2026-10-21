# Plan: adversarial-prep
Spec: specs/adversarial-prep.md
Architect verdict: PASS

## Tasks
- [x] T1 | slice=ui/prep.js | files=ui/prep.js,tests/prep.test.cjs | verify=`node --test tests/prep.test.cjs` | Implement validated practice state, adaptive follow-ups, conflict candidates, debrief, retest and safe exports.
- [x] T2 | slice=ui | files=ui/session.js,tests/session.test.cjs | verify=`node --test tests/session.test.cjs` | Extend portable sessions with optional validated practice state and legacy compatibility.
- [x] T3 | slice=ui | files=ui/prep-ui.js,ui/prep.css,ui/index.html,tests/prep_browser.cjs | verify=`node tests/prep_browser.cjs` | Add the isolated practice dialog, ledger, scenario controls, timer, history and downloads.
- [x] T4 | slice=server.py | files=server.py,tests/test_hardening.py,tests/package_smoke.py | verify=`python -m unittest discover tests -q` | Serve allowlisted practice resources and verify installed resources.
- [x] T5 | slice=README.md | files=README.md | verify=`node --test tests/session.test.cjs tests/prep.test.cjs` | Document fair host-agent practice and add core regression tests to CI.
- [x] T6 | slice=adversarial-prep.ssat.yaml | files=adversarial-prep.ssat.yaml,tests/prep_smoke.cjs | verify=`forge arch-gate adversarial-prep adversarial-prep.ssat.yaml --root .` | Prove architecture boundaries and non-hollow smoke with reproducible evidence.


- [x] T7 | slice=SKILL.md | files=SKILL.md | verify=`python -m unittest discover tests -q` | Add fair adaptive host-agent practice instructions.
- [x] T8 | slice=skills | files=skills/socratic-gtm-strategist/SKILL.md | verify=`python -m unittest discover tests -q` | Synchronize the installable agent skill.
- [x] T9 | slice=.github | files=.github/workflows/ci.yml | verify=`node --test tests/session.test.cjs tests/prep.test.cjs` | Execute the practice regressions in CI.
- [x] T10 | slice=pyproject.toml | files=pyproject.toml | verify=`python -m pip wheel . --no-deps --no-build-isolation` | Include practice styles in the package.

- [x] T11 | slice=smoke | files=smoke/adversarial-prep.json | verify=`forge smoke adversarial-prep --root .` | Declare a behavioral smoke that fails when practice implementation is replaced by stubs.

## Review authority
The user explicitly requested implementation as a goal. Codex local review
records implementation gates; it does not claim independent human approval,
merge, publication or deployment authority.
