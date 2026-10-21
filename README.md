# Socratic GTM Strategist

[![CI](https://github.com/zrk222/socratic-gtm-strategist/actions/workflows/ci.yml/badge.svg)](https://github.com/zrk222/socratic-gtm-strategist/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

An eight-phase founder interview skill and a standard-library Python toolkit
for collecting GTM assumptions, preparing experiments and generating draft artifacts.

The skill can guide a host model's qualitative Socratic review. The bundled
CLI, dashboard and MCP evaluator collect founder-reported inputs; they do not
call an LLM, validate a business strategy or produce calibrated confidence.
Long answers do not earn a passing score.

## Install and run

Requires Python 3.9 or later. From a checkout:

```bash
python -m pip install .
socratic-gtm --help
socratic-gtm start
socratic-gtm ui --no-browser
```

Open http://127.0.0.1:8000/ui/index.html. The CLI can also run directly with
python cli.py. No provider key is required.

The interview writes a draft GTM playbook containing all eight answers, a
simulator with unknown assessments, a generic backlog, a pitch template and
a security practice brief. All require evidence review before external use.

## Session workspace

The dashboard adds a portable workspace for the interview:

- Revise any of the eight answers and resume that phase.
- Record evidence, counterexamples, next experiments, owners and decision dates.
- Download a draft playbook made from your answers, plus an experiment CSV.
  CSV exports neutralize spreadsheet formula prefixes.
- Save a versioned JSON session file and load it later. Invalid or oversized
  imports leave the active session intact.
- Opt into saving on this device to survive reloads, including an unsent draft.
  Unchecking the option removes the saved copy.

Device storage and session files are unencrypted. Imported notes and URLs are
data and are not automatically trusted or fetched. Default saving is off; speech
playback is also off until enabled. Review controls are available on mobile.

## Tools

```bash
# Eight self-reported scenario inputs; these are not probabilities.
socratic-gtm simulate --project "MyAI" --scores "85,60,90,75,80,70,85,0"
socratic-gtm recon --incumbent "Example" --domain "Workflow tools"
socratic-gtm stress-test --mode ciso --startup "MyAI"
socratic-gtm export --csv sprint_issues.csv --json sprint_issues.json
socratic-gtm pitch-deck --startup "MyAI"
socratic-gtm mcp
```

- Simulator: eight scenario values and an inference-cost calculator. It excludes
  support, infrastructure and other costs; it is not a measured gross margin.
  Chart.js uses a CDN; the table and calculator still work if the chart cannot load.
- Recon: sends the public competitor/domain query to DuckDuckGo. Results include
  source links and a UTC retrieval timestamp, labeled UNVERIFIED. Network failures
  and unparsed results are UNAVAILABLE, not evidence that a competitor has no releases.
- Stress tests and pitch decks: prompts and evidence-required fields; no company
  security controls, traction, margins or certifications are inferred.
- Backlog: generic example CSV/JSON, to be adapted before importing into a tracker.

## Agent integration

Use [SKILL.md](SKILL.md) in a host that supports skills or explicit prompt loading.
Platform instruction files point to the same evidence and authority boundaries.
These configurations are examples; end-to-end testing in each external host is
separate from the local CLI/MCP checks.

For an MCP host, use the installed console command:

```json
{
  "mcpServers": {
    "socratic-gtm": {"command": "socratic-gtm", "args": ["mcp"]}
  }
}
```

The executable must be on the host's PATH; otherwise supply its absolute path.
The adapter implements newline-delimited JSON-RPC with the 2024-11-05 protocol
version, tools/list, tools/call and ping. It is not a full MCP SDK implementation
or a claim of compatibility with every host or newer protocol revision.

Python SDK:

```python
from socratic_gtm import get_system_prompt, generate_pitch_deck
prompt = get_system_prompt()
generate_pitch_deck("MyAI", "draft_pitch.md")
```

Optional LangChain wrappers require a separately installed compatible LangChain;
they are not included in the dependency-free test coverage.

## Local server boundary

The server binds 127.0.0.1 by default. It serves only the UI, OpenAPI schema,
status endpoint and named generated artifacts. It rejects non-local Host headers,
foreign Origin headers, cross-site browser writes, unsupported content types,
bodies over 65536 bytes and invalid payloads. CORS access is not enabled.

Outputs from web tools are stored in gtm_outputs and linked under /artifacts/.
Do not use this as a public multi-user service: there is no authentication,
tenant isolation or durable session store. Client-carried context is untrusted
interview data. Microphone and speech support depend on the browser; recognition
may use its speech provider. Do not dictate confidential material without
checking that provider's privacy behavior.

For a local container:

```bash
docker build -t socratic-gtm .
docker run --rm -p 127.0.0.1:8000:8000 socratic-gtm
```

The explicit 0.0.0.0 binding is for the container only. Public hosting needs a
separate authentication, storage and threat-model design.

## Development checks

```bash
python -m unittest discover tests -v
python -m pip wheel . --no-deps --wheel-dir dist
```

CI also installs the wheel into a clean environment and exercises the installed
entry point, MCP, SDK prompt, HTML output and packaged UI/schema resources.
Runtime tests cover HTTP rejection/recovery, MCP errors/notifications, hostile
HTML inputs, zero-score preservation, and evidence labeling. Recon tests use
controlled fixtures; they do not prove current search-provider availability.

The local audit evidence distinguishes test coverage from production readiness.
See [specs/audit-hardening.md](specs/audit-hardening.md) for the scoped requirements.
