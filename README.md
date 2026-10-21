# Socratic GTM Strategist for AI Startups (v2.1 - Context-Engineered)

An elite AI Startup Strategy Partner and Socratic Advisor designed to ruthlessly but constructively de-risk a founder's Go-To-Market (GTM) strategy before building unscalable or indefensible products.

Version 2.1 incorporates **Context Engineering** principles (pioneered by Dex Horthy and Carlos Kelkboom) to ensure high-fidelity execution, eliminate context degradation across multi-turn dialogues, and enforce quantitative confidence gating.

---

## 🎯 Overview

AI products face unique market dynamics that render traditional B2B SaaS playbooks obsolete:
- The death of per-seat SaaS pricing.
- The threat of foundational lab model improvements.
- The trap of low-frequency reactive text-boxes.
- Incumbent distribution advantages.

**Socratic GTM Strategist** acts as an uncompromising peer-level strategic advisor that conducts a structured, 8-phase Socratic dialogue with the founder, evaluates answers against strict red/green flags, and synthesizes a production-grade **Customized AI GTM Playbook & Risk Matrix**.

---

## 🧠 Context Engineering Enhancements (v2.1)

1. **Context State Accumulator (`<internal_monologue>`):**
   Maintains a formal, structured state object across all conversational turns. Prevents "context loosening" where long transcripts cause models to forget early nuances by Phase 8.
2. **Quantitative Confidence Gating ($\ge 85\%$ Threshold):**
   Replaces subjective advancement with an operational score gate. The advisor will not advance to the next phase without concrete mechanics (APIs, DAU mechanisms, integration depth).
3. **Open-Mode Execution Fence:**
   Strict separation between diagnostic discovery and execution. File creation and raw playbook dumps are locked behind the completion of all 8 phases to prevent premature generation.
4. **Artifact Containment:**
   The final deliverable is written cleanly to `GTM_PLAYBOOK.md` rather than dumped into the conversational window, preserving context cleanliness for subsequent iterative refinement.

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

| Phase | Strategic Vector | Core Objective | Confidence Gate |
| :--- | :--- | :--- | :---: |
| **Phase 1** | **Interaction Frequency & WoM Physics** | Test for the annual/cyclical trap & organic virality | $\ge 85\%$ |
| **Phase 2** | **"Ticking Clock" vs. Incumbent Distribution** | Pressure-test durability against incumbent feature copies | $\ge 85\%$ |
| **Phase 3** | **Adoption Vector (PLG vs. CISO Governance)** | Ensure end-user wedge precedes compliance bloat | $\ge 85\%$ |
| **Phase 4** | **Expansion Strategy** | De-risk vertical specialization via horizontal discovery | $\ge 85\%$ |
| **Phase 5** | **Value Architecture** | Shift reactive prompt engineering to proactive routines | $\ge 85\%$ |
| **Phase 6** | **Defensive Layer** | Ensure model neutrality & context ownership | $\ge 85\%$ |
| **Phase 7** | **Pricing & Value Capture** | Align pricing models with autonomous work economics | $\ge 85\%$ |
| **Phase 8** | **Integration & Data Gravity** | Establish bi-directional sync and switching barriers | $\ge 85\%$ |
| **Phase 9** | **Final Playbook Deliverable** | Auto-generate the customized Playbook, Matrix & Stress Test to file | Synthesis |

---

## 🛡️ Execution Guardrails & Mechanics

- **The Rule of Two:** At most two focused questions per turn to ensure depth.
- **Synthesize & Pivot:** Every turn validates/challenges previous responses before transitioning.
- **Internal Monologue:** Operates with internal evaluation (`<internal_monologue>`) measuring red vs. green flags.
- **Dynamic Branching:** Offers constructive pivot brainstorming when fatal flaws are uncovered rather than simple failure notices.
- **Anti-Sycophancy:** Uncompromising, intellectually rigorous peer tone.

---

## 📦 Installation & Usage

### Antigravity / Gemini CLI
Clone or copy this repository into your customizations directory:

```bash
# Global skills
git clone https://github.com/zrk222/socratic-gtm-strategist.git ~/.gemini/config/skills/socratic-gtm-strategist

# Or within a workspace:
git clone https://github.com/zrk222/socratic-gtm-strategist.git .agents/skills/socratic-gtm-strategist
```

### Direct Agent System Prompt
Copy the entire content of [`SKILL.md`](./SKILL.md) directly into your LLM's system prompt or custom instructions.

---

## 📄 License

Apache License 2.0. See [LICENSE](./LICENSE) for details.
