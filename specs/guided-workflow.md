# Spec: guided-workflow

## MUST — Behavior
### Requirements (EARS)
- When the workspace opens, the system shall display a four-step idea, questions, practice and next-steps workflow with a named primary action and optional tools closed (acceptance: `simple_entry`).
- When the founder submits an idea or an interview answer, the system shall display the current question and retain interview progress while keeping optional save/edit/settings controls inside an explicit disclosure (acceptance: `guided_questions`).
- When the founder chooses practice, the system shall start a buyer rehearsal from the latest saved answer or concept and display the objection without requiring claim creation or persona configuration; absent input shall focus a labelled idea field without fabricating a claim (acceptance: `direct_practice`).
- When the founder finishes practice, the system shall return to the next-steps screen and emit a downloadable draft containing actual interview and practice notes; detailed claim/settings controls shall remain explicitly available (acceptance: `guided_finish`).
- When a served simulator is opened, the system shall display a workspace return link and instructions identifying the calculator as an optional scenario tool (acceptance: `simulator_orientation`).
- When the workflow opens at a 390px viewport, the system shall display named keyboard actions and prevent horizontal overflow while retaining legacy save/import and manual practice functions (acceptance: `workflow_recovery`).

### Acceptance criteria (Gherkin)
```gherkin
Scenario: Founder completes a guided preparation
  Given a new workspace
  When the founder writes an idea and answers an interview question
  Then `simple_entry` displays a clear first action
  And `guided_questions` displays the next question
  When the founder chooses practice and answers an objection
  Then `direct_practice` records the response without interview changes
  When the founder finishes practice
  Then `guided_finish` displays next steps and downloads the entered notes
  And `simulator_orientation` links back to the workspace
  And `workflow_recovery` preserves optional tools and mobile keyboard access
```

## SHOULD — Scope and evidence
Scope: ui/index.html, ui/prep-ui.js, ui/prep.css, scripts/generate_dashboard.py,
tests/browser_smoke.cjs, tests/prep_browser.cjs, tests/guided_browser.cjs.
No claim scoring, model calls, credentials, interview deletion or deployment.
Keep the current validation and portable-session bounds. Reuse the existing
practice engine. Run existing regressions, a real-browser first-use funnel,
Prestige checks and candidate-bound Code Factory workflow evidence.

## Authorized parameters
- timeout = 10000

- limit = 0
