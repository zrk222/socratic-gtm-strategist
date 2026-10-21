# GTM Strategist: adversarial preparation

Implemented on the existing audit/local-hardening branch and draft PR #1.
This feature turns the static browser CISO/VC prompts into an isolated practice
workspace. Interview phase and answers remain intact.

## Delivered behavior

- Seven perspectives: skeptical investor, enterprise CISO, buyer, budget owner,
  procurement lead, incumbent competitor and dissatisfied customer.
- Claim ledger with verbatim bounded interview-statement extraction, assertion /
  hypothesis / unknown / evidence-linked labels, source notes, counterexample,
  next test, owner, due date and founder review status.
- Follow-ups request missing evidence, counterexamples or tests and quote the
  focused claim. Explicit uncertainty prompts a falsifiable test.
- Possible-conflict review quotes overlapping statements with changed numbers or
  negation. It asks for scope/date/unit review rather than declaring a contradiction.
- Contested premises remain recorded. Founders can request an interruption.
- Hypothetical budget loss, rising costs, free competition, integration loss and
  launch/deal premortem scenarios.
- Untimed, 30-second or two-minute rehearsal. Pause/resume and explicit interruption.
  Expiry retains the draft without submitting. Timers reset paused on reload.
- Persistent attempts and drafts in opt-in device saving and portable session JSON;
  legacy interview-only files still work. Invalid imports preserve active state.
- Debriefs show recorded gaps, transcripts and next actions without readiness scores.
  Retests reuse the original first objection and compare recorded answers/evidence.
- Real Markdown debrief, formula-neutralized action CSV and agent-coach packet
  downloads. A packet is never transmitted automatically.
- Native keyboard dialog, labelled controls, focus return, mobile layout, reduced
  motion styling, and packaged/allowlisted JavaScript and CSS.

## Verification

Exact commands, timestamps, durations and logs:
.factory/adversarial-prep/verification.json.

- 36 Python tests, including allowlisted practice-resource HTTP behavior.
- 18 Node tests covering pure engine transitions, all persona/scenario choices,
  records, invalid state, references, bounds, conflict candidates and exports.
- Existing 11-scenario Chrome regression suite.
- Eight new Chrome scenarios: ledger/conflicts, follow-ups/contested premise,
  clock expiry/interruption/reload, debrief/retest, interview isolation/downloads,
  hostile text/invalid import recovery, 390px keyboard/mobile and runtime errors.
- Fresh wheel installed into an isolated environment outside the checkout.
- SpecLine strict and 17 requirement mutations, drift and skill frontmatter checks.
- ForgeLine architecture review and runtime smoke. The same self-contained smoke
  passes on the engine and fails on the generated empty() stub with
  NotImplementedError. Verification/smoke run in one process because the installed
  verifier binds its evidence to the complete process environment.
- Prestige source audit, critique, desktop/mobile render and sabotage challenge.
  Interactive practice dialog evidence comes from the actual Chrome suite.
- Code Factory bounded Python security audit; candidate-bound workflow evidence
  completeness/hash checks. These checks do not grant release authority.
- Internal JavaScript compiler inventory: maximum measured branch complexity 7
  in the engine and 9 in the adapter. ForgeLine's public-export QA is inventory
  only for these UMD modules; its aggregate is not behavioral coverage evidence.

## Requirement evidence map

| Requirement IDs | Authoritative evidence |
| --- | --- |
| practice_isolation, claim_ledger, adaptive_followup, fair_challenge | tests/prep.test.cjs, tests/prep_browser.cjs and their recorded runtime logs |
| persona_selection, claim_candidates, conflict_review, scenario_shocks | Named Node tests, plus browser conflict quotations |
| timed_rehearsal | Browser clock expiry preserves draft/turn count; interruption and reload assertions |
| practice_debrief, retest_comparison, practice_exports | Browser actual downloads and prior/current answer assertions; Node export validation |
| practice_restore, practice_recovery | Legacy/new session Node tests; invalid and hostile browser imports |
| practice_privacy | No practice POSTs; no rendered injected images; text-only DOM and scoped architecture invariants |
| practice_accessibility | Native dialog keyboard/focus assertions, 390px overflow check and screenshots |
| practice_wheel | HTTP allowlist test and clean installed-wheel resource checks |

## Limits and review boundaries

The local engine is deterministic guided rehearsal. It does not run an LLM,
verify sources, judge answer quality, detect semantic contradictions generally,
or predict meeting/business success. Follow-up selection depends on explicit
supporting fields and a small explicit-unknown pattern. English numeric/negation
conflict heuristics can miss conflicts and flag consistent statements.

Notes supplied in later attempts or ledger edits are current notes, not proof
that a prior answer had evidence. Retest comparison retains the actual prior and
current answer fields. All claim labels and addressed/contested states are founder
assessments. Source links are text and are not fetched automatically.

Limits: 24 claims, eight attempts, 18 answers per attempt, 192 KiB practice and
256 KiB portable session. Export before removing old attempts. Device saving is
optional and unencrypted. Existing browser voice/provider behavior remains
separate; no real keys or paid provider calls were used for this feature.

Prestige reports a source-density heuristic; the practice UI uses progressive
disclosure and separate stages. No conversion uplift or full assistive-technology
certification is claimed. Chrome desktop and a 390px mobile viewport were tested.

Initial verification issues were repaired: the browser harness needed its clock
installed before time manipulation; interview isolation compares persisted
interview fields; parameter facts require the named SpecLine section; the
Windows inline smoke command required explicit encoding. Retained drift failure
is in .factory/adversarial-prep/drift-first-failure.txt. Generated stub and real
smoke diagnostics are retained in forge-bundle.txt.

ForgeLine's operator gate uses a built-in human label. Here it represents Codex
local review under the user's explicit implementation authorization, not a
separate human review. No merge, deployment, publication or independent approval
is claimed. GitHub CI status is recorded separately against the pushed commit.
