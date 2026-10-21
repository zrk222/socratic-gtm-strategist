# GTM Strategist audit and enhancement

Repository: zrk222/socratic-gtm-strategist. Original audit base:
3da14f872b9fb45058b6b388b19cc4a769405d25. The concurrent voice update
479b07eda8b1e15c8f0cadaa53a2ec50e6d6bd63 was merged and preserved.

## Assessment

The original ten tests passed while the following runtime defects remained.
The current branch repairs the reproduced paths and adds a founder evidence
workspace. It remains a local, single-user toolkit. Host-model review,
calibrated confidence and commercial validation are separate capabilities.

| Priority | Finding | Change and verification |
| --- | --- | --- |
| P1 | The HTTP server bound every network interface and served the entire repository, including .git and local configuration; wildcard CORS allowed cross-origin access. | Default loopback binding, explicit GET/HEAD routes, same-origin/Host checks and no wildcard CORS. HTTP tests reject private files, traversal and foreign writes. |
| P1 | Repeated filler received an 85% strategic PASS. Phase eight advanced to completion without validation, and the UI claimed unwritten deliverables existed. | Removed word-count scoring across CLI, MCP and HTTP. Intake returns REVIEW_REQUIRED and null confidence. Only actual generator responses or browser downloads are presented as files. |
| P1 | Simulator project names and notes entered HTML/script contexts without escaping. A zero score became 75 in the browser. | Escaped project text, script-safe JSON, DOM textContent and explicit null handling. Runtime tests use hostile strings, zero scores and a blocked chart CDN. |
| P2 | The built wheel omitted the CLI, server, MCP adapter, UI, schema and prompt; editable/source checks hid this. | Included modules and resources. A fresh virtual environment installs the wheel outside the checkout and exercises the console entry point, SDK, MCP and generation. |
| P2 | Malformed HTTP payloads could kill a request handler or bypass validation; MCP parameter arrays could terminate the server and notifications received responses. | Typed and bounded request validation, JSON errors, MCP envelope/argument checks, notification suppression and recovery tests. |
| P2 | Pitch and security briefs asserted company margins, acquisition results, certifications and controls without founder evidence. Recon labeled failed searches as verified signals. | Evidence-required narrative fields and practice questions. Recon emits source-bearing, timestamped UNVERIFIED leads or UNAVAILABLE state. |
| P2 | Browser phase/context were not retained from API responses, and API failure switched to fabricated client-side success. | Client state updated on successful responses; failed turns retain the answer and phase. Opt-in session saving, import/export and answer revision make progress recoverable. |
| P2 | Concurrent voice settings stored provider credentials in browser storage and exposed unbounded proxy behavior. | Preserved provider choices with memory-only keys, local-origin enforcement, upload/response ceilings and fixed provider targets. Mocked forwarding, fallback and credential-exclusion tests pass. |

## Added user functions

- A named project workspace with visible answer and evidence-note counts.
- Opt-in local save/resume, portable versioned JSON sessions and retained drafts.
- Import validation with a 256 KiB ceiling; failed imports preserve active state.
- Eight editable answers with evidence, counterexample, next experiment, owner
  and decision-date fields.
- A playbook generated from the entered answers and notes, plus an experiment CSV
  that neutralizes spreadsheet formula prefixes.
- Resume at a chosen interview phase; generate or download real local artifacts.
- Accessible control names, keyboard review dialog, responsive session actions,
  reduced-motion support and default-muted speech.
- Nanna storytelling: idea, assumptions, evidence and one next move. Prestige
  styling uses a calmer slate/mint palette, clearer hierarchy and readable text.

## Local verification

See .factory/evidence/verification.json for exact argv, execution timestamps,
elapsed time, exit codes and logs. Checks include:

- Python unittest: 33 tests.
- Node session data suite: 5 tests.
- Chrome browser: 11 scenarios including desktop/mobile preview, voice-key
  exclusion, save/reload, real downloads, invalid and hostile imports, injected
  API failure, device-copy removal and simulator behavior without its chart CDN.
- A built-wheel install in a clean environment outside the checkout.
- Skill frontmatter validation, SpecLine strict lint and 15 requirement-mutation
  checks, source drift audit and git whitespace validation.
- Prestige audit, seven-lens critique, desktop/mobile render and sabotage challenge.
- Code Factory bounded Python static security audit and hash-bound workflow
  evidence gate. The gate validates supplied record completeness and hashes;
  actual behavior is supported by the underlying tests and browser observations.

## Remaining limits

- This is not an authenticated public service or multi-tenant application.
- The bundled evaluator collects answers; it does not run a model or establish
  that a strategy works. Market outcomes, confidence calibration and customer
  results are unknown.
- Provider speech forwarding uses controlled fixtures in tests. No real keys,
  paid calls, microphone quality, provider account settings or retention terms
  were verified. Provider/model choices are inherited configuration, not a claim
  that a model remains available in every account.
- Search tests use controlled failures/results and do not establish live search
  availability. External primary sources must be reviewed before strategic use.
- Desktop Chrome and a 390px mobile viewport were tested locally. This is not a
  full assistive-technology audit or proof of every agent host/browser integration.
- The UI still loads external style/icon resources. Chart.js is optional for the
  simulator table/calculator, but complete offline visual fidelity is not proven.
- Prestige's source-density heuristic remains a review prompt. Detailed review
  and voice settings are behind explicit panels; no conversion uplift is claimed.
- Local test results do not establish deployment, package publication, customer
  readiness or release approval.
