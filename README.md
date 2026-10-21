# Socratic GTM Strategist for AI Startups (v3.0 - Full-Spectrum OS)

An elite AI Startup Strategy Partner, Socratic Advisor, and GTM Operating System designed to ruthlessly but constructively de-risk a founder's Go-To-Market (GTM) strategy before building unscalable or indefensible products.

Version 3.0 integrates **Context Engineering** state management with **5 production-grade execution modules**:
1. 📊 **Interactive GTM Risk Radar & Margin Collapse Simulator** (`gtm_simulator.html`)
2. 🕵️ **Live Incumbent Reconnaissance** (Automated competitive intelligence)
3. ⚔️ **Adversarial Stress Test Modes** (`/stress-test ciso` and `/stress-test vc`)
4. 🚀 **Executable Sprint Backlog Export** (Importable CSV/JSON for Linear, Jira & GitHub)
5. 🎙️ **Investor Pitch Deck Narrative Generator** (`GTM_PITCH_DECK.md`)

---

## 🎯 Strategic Overview

AI products face unique market dynamics that render traditional B2B SaaS playbooks obsolete:
- The death of per-seat SaaS pricing.
- The threat of foundational lab model improvements.
- The trap of low-frequency reactive text-boxes.
- Incumbent distribution advantages.

**Socratic GTM Strategist** conducts a structured, 8-phase Socratic dialogue with the founder, evaluates answers against strict red/green flags, verifies operational depth against an **85% confidence gate**, and synthesizes an entire execution toolkit.

---

## 🛠️ The 5 Operational Modules

### 1. Interactive Risk Radar & Margin Collapse Simulator
* **Script:** [`scripts/generate_dashboard.py`](./scripts/generate_dashboard.py)
* **Output:** Standalone responsive dark-mode HTML file (`gtm_simulator.html`) with:
  * Dynamic **8-Vector Radar (Spider) Chart** plotting your startup's moats and vulnerabilities.
  * Real-time **AI Unit Economics Calculator**: Sliders for token counts, pricing, task frequencies, and user accounts that dynamically graphs Gross Margin % and triggers red alerts when margins drop below healthy software thresholds.

### 2. Live Incumbent Reconnaissance
* **Script:** [`scripts/incumbent_recon.py`](./scripts/incumbent_recon.py)
* **Function:** In Phase 2, queries real-time product updates and announcements for named competitors (`"[Incumbent] AI agent announcements 2026"`). 
* **Value:** Protects founders from building features that incumbents already shipped or announced last quarter.

### 3. Adversarial Role-Playing Inquisitions
* **Script:** [`scripts/stress_test_simulator.py`](./scripts/stress_test_simulator.py)
* **Subcommands:**
  * `/stress-test ciso`: Grills the founder from the perspective of an enterprise Fortune 500 CISO on data egress, tenant isolation, prompt injection blast radiuses, and SOC2 readiness.
  * `/stress-test vc`: Grills the founder as a Tier-1 Venture Partner on unit economics, churn rate physics, TAM, and defensibility against foundation lab updates.

### 4. Executable GTM Runbook Export (Linear / Jira / GitHub)
* **Script:** [`scripts/export_issues.py`](./scripts/export_issues.py)
* **Outputs:** `gtm_sprint_issues.csv` and `gtm_sprint_issues.json`
* **Value:** Instantly converts strategic advice into prioritized engineering tickets (Sprint 0 Telemetry, Sprint 1 Bi-Directional Webhooks, Sprint 2 Hybrid Metering) with acceptance criteria ready to import directly into your project tracker.

### 5. Investor Pitch Deck Narrative Generator
* **Script:** [`scripts/generate_pitch_deck.py`](./scripts/generate_pitch_deck.py)
* **Output:** `GTM_PITCH_DECK.md`
* **Value:** Translates the validated strategy into 5 battle-tested slide scripts for Seed/Series A fundraising (The Wedge, The Agentic Shift, Incumbent Bypass, AI Economics, Data Gravity).

---

## 🧭 The 8 Strategic Laws of AI GTM

1. **The Interaction Frequency Rule:** Low-frequency software (annual/seasonal) cannot sustain viral word-of-mouth.
2. **The Ticking Clock on Distribution:** Startups win on speed and UX; incumbents win on distribution. Network effects must be built before incumbents replicate core features.
3. **Bottom-Up User Delight vs. The CISO Trap:** Starting with IT/CISO compliance yields unloved software. Start with end-user delight (PLG), then layer enterprise controls.
4. **Proactive Routines vs. Text-Box Friction:** Value lies in proactive, background agentic routines, not chat-box friction.
5. **Horizontal Seeding to Organic Verticalization:** Discover high-ROI power-user workflows horizontally, then package vertical solutions from real pull.
6. **Model Neutrality & Context Ownership:** Avoid single-supplier derivative risk. Serve as a neutral router while the customer retains ownership of their context.
7. **The Pricing Paradox:** AI agents destroy seat-based pricing by replacing human labor. Value must be captured via outcomes, tasks, or consumption.
8. **Data Gravity & The Integration Moat:** Standalone tools fail. Bi-directional integrations establish the switching costs needed for durable moats.

---

## 🔄 The 8-Phase Socratic Framework

| Phase | Strategic Vector | Core Objective | Gating Threshold |
| :--- | :--- | :--- | :---: |
| **Phase 1** | **Interaction Frequency & WoM Physics** | Test for the annual/cyclical trap & organic virality | $\ge 85\%$ |
| **Phase 2** | **"Ticking Clock" vs. Incumbent Distribution** | Live recon on competitor releases & architectural wedge | $\ge 85\%$ |
| **Phase 3** | **Adoption Vector (PLG vs. CISO Governance)** | Ensure end-user wedge precedes compliance bloat | $\ge 85\%$ |
| **Phase 4** | **Expansion Strategy** | De-risk vertical specialization via horizontal discovery | $\ge 85\%$ |
| **Phase 5** | **Value Architecture** | Shift reactive prompt engineering to proactive routines | $\ge 85\%$ |
| **Phase 6** | **Defensive Layer** | Ensure model neutrality & customer context ownership | $\ge 85\%$ |
| **Phase 7** | **Pricing & Value Capture** | Align pricing models with autonomous work economics | $\ge 85\%$ |
| **Phase 8** | **Integration & Data Gravity** | Establish bi-directional sync and switching barriers | $\ge 85\%$ |
| **Phase 9** | **Full 5-Piece Deliverable Synthesis** | Playbook, HTML Simulator, Sprint Issues, Pitch Deck | Multi-Artifact |

---

## 📦 Repository Structure

```text
socratic-gtm-strategist/
├── SKILL.md                          # Full v3.0 agent system skill with module hooks
├── skills/
│   └── socratic-gtm-strategist/
│       └── SKILL.md                  # Package distribution mirror
├── README.md                         # Complete documentation
├── LICENSE                           # Apache License 2.0
├── scripts/
│   ├── generate_dashboard.py         # Generates interactive HTML Radar & Margin Simulator
│   ├── incumbent_recon.py            # Automated competitor AI intelligence recon
│   ├── stress_test_simulator.py      # CISO & VC adversarial brief generator
│   ├── export_issues.py              # Exports Sprint 0-2 issues to Linear/Jira CSV & JSON
│   └── generate_pitch_deck.py        # Generates 5-slide venture pitch deck copy
└── templates/
    ├── gtm_simulator.html            # Sample interactive simulator
    ├── GTM_PLAYBOOK.md               # Sample strategic playbook
    ├── GTM_PITCH_DECK.md             # Sample investor deck copy
    └── gtm_sprint_issues.csv         # Sample Linear/Jira importable issues
```

---

## 🚀 Usage

### 1. Run in Antigravity or Gemini CLI
```bash
# Global installation:
git clone https://github.com/zrk222/socratic-gtm-strategist.git ~/.gemini/config/skills/socratic-gtm-strategist
```

### 2. Standalone Python CLI Tooling
```bash
# Generate the interactive HTML Radar & Margin Simulator:
python scripts/generate_dashboard.py --project "MyAI" --scores "85,60,90,75,80,70,85,90" --output gtm_simulator.html

# Run live incumbent recon:
python scripts/incumbent_recon.py --incumbent "Salesforce" --domain "Customer Support AI"

# Generate an Adversarial CISO or VC Brief:
python scripts/stress_test_simulator.py --mode ciso --startup "MyAI"

# Export Linear / Jira Sprint Backlog:
python scripts/export_issues.py --csv sprint_issues.csv

# Generate 5-Slide Pitch Deck Copy:
python scripts/generate_pitch_deck.py --startup "MyAI"
```

---

## 📄 License

Apache License 2.0. See [LICENSE](./LICENSE) for details.
