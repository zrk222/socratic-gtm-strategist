# Plan: audit-hardening
Spec: specs/audit-hardening.md
Architect verdict: PASS

## Logical decomposition (phases)
1. Reproduce baseline defects; repair adapters and outputs; verify a clean distribution.

## Tasks (atomic — each independently shippable)
<!-- Rules enforced by `specline tasks`: one slice each, <=4 files,
     explicit verify command, no forward references. -->
- [ ] T1 | slice=pyproject.toml | files=pyproject.toml | verify=`python -m pip wheel . --no-deps --no-build-isolation` | Include root CLI adapters and UI and skill resources in wheel.
- [ ] T2 | slice=socratic_gtm | files=socratic_gtm/__init__.py,socratic_gtm/assessment.py,tests/test_hardening.py | verify=`python -m unittest discover tests -q` | Centralize review-required assessment and repair installed prompt loading.
- [ ] T3 | slice=cli.py | files=cli.py,tests/test_socratic_gtm.py | verify=`python -m unittest discover tests -q` | Retain interview answers in a draft playbook with safe filenames.
- [ ] T4 | slice=server.py | files=server.py,tests/test_hardening.py | verify=`python -m unittest discover tests -q` | Restrict routes, origins, hosts and request types.
- [ ] T5 | slice=ui | files=ui/index.html,tests/test_browser.cjs | verify=`python -m unittest discover tests -q` | Retain context and show API failures without synthetic success.
- [ ] T6 | slice=scripts | files=scripts/generate_dashboard.py,scripts/incumbent_recon.py,scripts/generate_pitch_deck.py,scripts/stress_test_simulator.py | verify=`python -m unittest discover tests -q` | Escape markup and replace unsupported claims with evidence requests.
- [ ] T7 | slice=mcp_server.py | files=mcp_server.py,tests/test_hardening.py | verify=`python -m unittest discover tests -q` | Validate MCP envelopes and arguments; silence notifications.
- [ ] T8 | slice=SKILL.md | files=SKILL.md | verify=`python -m unittest discover tests -q` | Replace hidden-reasoning instructions and qualify strategy hypotheses.
- [ ] T9 | slice=skills | files=skills/socratic-gtm-strategist/SKILL.md | verify=`python -m unittest discover tests -q` | Synchronize the installable skill.
- [ ] T10 | slice=README.md | files=README.md | verify=`python -m unittest discover tests -q` | Document tested capabilities and limitations.
- [ ] T11 | slice=.github | files=.github/workflows/ci.yml | verify=`python -m unittest discover tests -q` | Add an isolated installed-wheel check to CI.
- [ ] T12 | slice=docker-compose.yml | files=docker-compose.yml | verify=`python -m unittest discover tests -q` | Publish the container only on loopback.
- [ ] T13 | slice=Dockerfile | files=Dockerfile | verify=`python -m unittest discover tests -q` | Run explicit container binding without browser launch.
- [ ] T14 | slice=ui | files=ui/session.js,ui/index.html,tests/session.test.cjs,tests/browser_smoke.cjs | verify=`node --test tests/session.test.cjs` | Add validated session export/import, answer revision, evidence and experiments, and accessible mobile controls.
- [ ] T15 | slice=openapi.json | files=openapi.json | verify=`python -m unittest discover tests -q` | Document null confidence and local intake fields.
- [ ] T16 | slice=ui | files=ui/openapi.json | verify=`python -m unittest discover tests -q` | Ship the synchronized schema resource.
- [ ] T17 | slice=CLOUD_INTEGRATIONS.md | files=CLOUD_INTEGRATIONS.md | verify=`python -m unittest discover tests -q` | Remove unsupported public-hosting instructions.
- [ ] T18 | slice=templates | files=templates/GTM_PLAYBOOK.md,templates/GTM_PITCH_DECK.md,templates/gtm_simulator.html | verify=`python -m unittest discover tests -q` | Keep checked-in examples consistent with evidence-required outputs.
- [ ] T19 | slice=CODEX.md | files=CODEX.md | verify=`python -m unittest discover tests -q` | Align Codex adapter guidance.
- [ ] T20 | slice=CLAUDE.md | files=CLAUDE.md | verify=`python -m unittest discover tests -q` | Align Claude adapter guidance.
- [ ] T21 | slice=.cursorrules | files=.cursorrules | verify=`python -m unittest discover tests -q` | Align Cursor adapter guidance.
- [ ] T22 | slice=tests | files=tests/package_smoke.py | verify=`python tests/package_smoke.py .factory/wheels/socratic_gtm_strategist-3.0.0-py3-none-any.whl` | Verify console, SDK and MCP resources from an isolated wheel environment.
- [ ] T23 | slice=.gitignore | files=.gitignore | verify=`git diff --check` | Keep local founder outputs and build products out of version control.

## Review authority
The user authorized audit, review and enhancement. Codex reviews this local plan; no separate human signoff or release approval is claimed.
