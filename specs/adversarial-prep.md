# Spec: adversarial-prep

## MUST — Behavior

### Goal
Help a founder rehearse skeptical conversations, identify missing evidence and
leave with specific follow-up work. The local engine uses transparent rules;
it neither runs a language model nor verifies business or security claims.

### User roles
- Founder preparing for customer, investor and enterprise meetings.

### Requirements (EARS)
- When a founder starts practice, the system shall store an isolated practice session with zero modifications to interview answers or phase (acceptance: `practice_isolation`).
- When a founder selects a persona, the system shall display investor, CISO, buyer, finance, procurement, competitor and dissatisfied-customer perspectives (acceptance: `persona_selection`).
- When a founder records a claim, the system shall retain its exact text, assertion/hypothesis/unknown/evidence-linked label, evidence note, counterexample, next action, owner and due date without marking evidence verified (acceptance: `claim_ledger`).
- When interview statements are extracted, the system shall store the resulting verbatim statements as founder assertions requiring review (acceptance: `claim_candidates`).
- When a practice answer lacks evidence, a counterexample or a falsifiable test, the system shall emit a follow-up requesting the missing field and quote the focused claim (acceptance: `adaptive_followup`).
- When statements have overlapping terms and differing numeric or negation patterns, the system shall display both exact statements as possible conflicts for founder review rather than asserting a contradiction (acceptance: `conflict_review`).
- When a founder contests a question, the system shall record the challenge, invite correction of its premise and preserve the answer without a readiness penalty (acceptance: `fair_challenge`).
- When a founder selects a scenario, the system shall display baseline, budget loss, rising costs, free competition, integration loss and premortem conditions as hypothetical (acceptance: `scenario_shocks`).
- When a timed rehearsal is selected, the system shall display untimed, 30-second and 120-second answer controls, pause/resume and an explicit interruption action; expiration shall preserve the draft without automatic submission (acceptance: `timed_rehearsal`).
- When a practice session ends, the system shall retain the transcript and show missing evidence, counterexamples and next actions without inventing scores or probabilities (acceptance: `practice_debrief`).
- When a founder retests a recorded objection, the system shall create a linked practice attempt and show the previous and current answer with their recorded supporting fields (acceptance: `retest_comparison`).
- When a founder exports practice, the system shall emit a text-safe Markdown debrief, formula-neutralized action CSV and an agent-coach packet from actual session inputs (acceptance: `practice_exports`).
- When a session file or device copy is restored, the system shall validate practice records, references, enums, text, numeric bounds and dates before replacing active state while accepting legacy interview-only files (acceptance: `practice_restore`).
- If a practice mutation or import exceeds a bound or contains invalid data, the system shall retain the current session and show an error (acceptance: `practice_recovery`).
- When untrusted text is rendered or exported, the system shall render it as text and shall make zero network requests from practice content (acceptance: `practice_privacy`).
- When practice opens at a 390px viewport, the system shall display labelled keyboard controls, a native focus-managed dialog and no horizontal overflow (acceptance: `practice_accessibility`).
- When an installed wheel serves the dashboard, the system shall return HTTP 200 for the practice JavaScript and stylesheet resources (acceptance: `practice_wheel`).

### Acceptance criteria (Gherkin)
```gherkin
Scenario: Practice acceptance observations
  Given a founder interview and separate practice records
  When local tests and browser scenarios run
  Then `practice_isolation` retains the interview phase and answers
  And `persona_selection` selects each of the seven viewpoints
  And `claim_ledger` preserves evidence and next actions
  And `claim_candidates` preserves verbatim founder statements
  And `adaptive_followup` requests missing supporting fields
  And `conflict_review` displays possible conflicting quotations
  And `fair_challenge` records a contested premise
  And `scenario_shocks` marks each scenario hypothetical
  And `timed_rehearsal` retains the draft on expiration
  And `practice_debrief` shows recorded gaps without scores
  And `retest_comparison` links the previous answer
  And `practice_exports` preserves text without spreadsheet execution
  And `practice_restore` restores valid data and accepts legacy files
  And `practice_recovery` rejects invalid updates atomically
  And `practice_privacy` renders hostile content without network calls
  And `practice_accessibility` supports keyboard and mobile controls
  And `practice_wheel` serves installed resources
```

## SHOULD — Architecture
- Scope: ui/prep.js, ui/prep-ui.js, ui/prep.css, ui/session.js, ui/index.html,
  server.py, pyproject.toml, tests, CI, README, skill mirrors and feature evidence.
- A pure deterministic practice engine owns validated state and exports. A DOM
  adapter owns dialog, timer and rendering. Session code owns the shared portable
  envelope. Neither practice module calls a provider or executes imported text.
- Workflow: Code Factory doctor and evidence audit, SpecLine strict/mutation/
  drift gates, ForgeLine SSAT and non-hollow runtime smoke, Prestige audits.
- Non-goals: verified semantic contradiction detection, live model evaluation,
  calibrated readiness scores, paid provider calls, merge, deployment or release.

## Authorized parameters
- Whole portable session: 262144 bytes; practice: 196608 bytes.
- Practice: 24 claims, 8 runs, 18 turns per run; text limits 200, 2000 and 4000.
- Timer limits: 0, 30, 120 seconds; measured elapsed maximum 86400 seconds.
- Candidate extraction: at most 24 verbatim statements; overlap threshold 2 terms.
- Claim identity and run identity use sequential positive integers with prefixes.
- Dates: ISO calendar dates; timestamps: non-negative finite epoch milliseconds.
- Performance fixture: 50 small-history conflict scans in at most 2000 milliseconds.
- Timer updates: 250 milliseconds. No readiness or success percentage exists.
- limit = 0
- limit = 30
- limit = 120
- limit = 5

The value 5 is an invalid-input test fixture only; runtime must reject it.

## SHOULD NOT — Implementation invention
No company facts, missing claims, evidence judgments or provider results may be
invented. Possible-conflict heuristics must explain their limited scope.
