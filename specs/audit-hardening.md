# Spec: audit-hardening
Status: draft

## MUST — Functional core
### Description
Repair reproduced installation, HTTP exposure, output injection and evidence-integrity defects in the local GTM toolkit.

### User roles
- Founder using the CLI, local dashboard or MCP client.

### Requirements (EARS)
<!-- Every requirement uses an EARS keyword: shall / When / While / If / Where -->
- When a wheel is installed outside the checkout, the system shall load CLI help, MCP initialization, dashboard generation and SDK prompt resources without importing checkout files (acceptance: `wheel_smoke`).
- When an HTTP client requests a repository file outside explicit UI, schema and generated-artifact routes, the system shall return HTTP 404 (acceptance: `private_routes`).
- If a POST has a foreign Origin or non-local Host, the system shall return HTTP 403 before executing a tool (acceptance: `origin_host`).
- If an HTTP body is malformed JSON, not an object, over 65536 bytes or has invalid field types, the system shall return a 4xx JSON response and continue serving subsequent requests (acceptance: `request_recovery`).
- When any founder answer is assessed, the system shall return REVIEW_REQUIRED status and null confidence rather than converting word count to strategic validation (acceptance: `answer_integrity`).
- When an interview completes, the system shall store all 8 answers in a draft playbook and display only artifacts actually written (acceptance: `interview_artifacts`).
- When project names or notes contain HTML or script delimiters, the system shall render text without executing injected markup and shall preserve exactly zero as a score value (acceptance: `html_injection`).
- When recon fails or returns no sourced findings, the system shall return unavailable or unverified evidence with a retrieval timestamp and shall not label snippets verified (acceptance: `recon_provenance`).
- When pitch and stress-test templates are generated, the system shall display exactly zero unsupported traction, margin or certification assertions (acceptance: `claim_integrity`).
- If an MCP request has invalid structure or arguments, the system shall return a structured error without terminating the MCP adapter; a notification shall receive zero responses (acceptance: `mcp_recovery`).
- When a founder saves or imports a session, the system shall validate the version, phase range 0 through 9, eight answer keys, bounded text and a 262144-byte input ceiling before replacing active state (acceptance: `session_roundtrip`).
- When a founder reviews an answer, the system shall allow revising the answer and recording evidence, next experiment, owner and decision date; local exports shall preserve entered values and label missing evidence (acceptance: `review_exports`).
- When a founder opens the dashboard at a 390px viewport, the system shall display named keyboard-focusable session controls and review actions without horizontal overflow (acceptance: `mobile_session_controls`).
- When optional voice settings are used, the system shall route the upstream provider choices, reject foreign requests, cap STT input at 5242880 bytes, and return a fallback response on provider failure; credentials shall remain outside session exports and device storage (acceptance: `voice_integration`).
- When the preview opens, the system shall display the founder mission, an idea-to-evidence journey and a next action without asserting business outcomes; the interface shall respect reduced-motion preferences (acceptance: `story_preview`).

### Acceptance criteria (Gherkin)
```gherkin
Scenario: Local server rejects repository disclosure
  Given the local server has started
  When a client requests /.git/config
  Then the response status is 404

Scenario: Oversized request
  Given the body limit is 65536 bytes
  When the client declares a larger body
  Then the response is a 4xx JSON error

Scenario: Verbose filler is not strategy evidence
  Given a phase 1 answer with 40 repetitions
  When the answer is assessed
  Then the confidence is null and the status is REVIEW_REQUIRED

Scenario: Acceptance observations remain bound to declared behaviors
  Given the candidate source bytes
  When the validation profile executes
  Then `wheel_smoke` proves installed entry points and resources
  And `private_routes` rejects private files
  And `origin_host` rejects foreign requests
  And `request_recovery` rejects malformed bodies and preserves service
  And `answer_integrity` never validates verbose filler
  And `interview_artifacts` retains founder answers
  And `html_injection` renders hostile strings as text
  And `recon_provenance` marks unavailable evidence
  And `claim_integrity` leaves unknown outcomes unknown
  And `mcp_recovery` responds only to requests
  And `session_roundtrip` rejects invalid imports without replacing state
  And `review_exports` preserves evidence notes and prevents spreadsheet formula execution
  And `mobile_session_controls` keeps the session actions accessible
  And `voice_integration` proves proxy rejection, mocked forwarding, fallback and credential exclusion
  And `story_preview` presents honest onboarding and preserves usable desktop and mobile layouts
```

## SHOULD — Technical/structural
- Standard library only. Existing adapters and field names remain available.
- Scope: root adapters, socratic_gtm, scripts, ui, skill mirrors, packaging, CI, documentation and regression tests.
- Verification: unittest HTTP integration, subprocess MCP recovery, isolated wheel smoke and browser DOM behavior.
- Non-goals: hosted authentication, live LLM evaluation, calibrated confidence, commercial validation, repository merge, deployment and publication.
- Evidence boundary: local hardening checks do not certify security or universal platform compatibility.

## SHOULD NOT — Implementation details
<!-- Leave the "how" to the plan/tasks unless it is a systemic invariant -->

## Decision logic (factory candidates)
<!-- Ordered business rules over extracted facts. specline handoff compiles
     these via HSF instead of letting agents improvise them. -->
No new ordered business rules: remove the unsupported score-based business decision. Request validation and presentation remain adapter behavior.

## Authorized parameters

The HTTP body ceiling is 65536 bytes. The tool schema declares eight scores
between zero and 100, and interview phases one through eight.

- MAX_BODY = 65536
- MAX_AUDIO = 5242880
- MAX_PROVIDER_RESPONSE = 10485760
- timeout = 20
- timeout = 5
- timeout = 1
- timeout = 3
- timeout = 10
- max_length = 10000
- TOOLS_SCHEMA = 0
- TOOLS_SCHEMA = 100
- TOOLS_SCHEMA = 8
- TOOLS_SCHEMA = 1

## CI startup observation

The subprocess HTTP smoke test uses an OS-assigned port and waits at most
20 seconds for the server's startup URL before making requests. A fixed sleep
or fixed port is not readiness evidence. The test retains startup diagnostics
when readiness fails and terminates its own process on every exit path.

Rejected POST requests discard an unambiguous body of at most 65536 bytes
with a one-second deadline before returning their error. They never execute
a tool or forward a provider request. Oversized or ambiguously framed bodies
are rejected without consumption.
