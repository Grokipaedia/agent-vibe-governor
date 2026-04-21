# agent-vibe-governor

> **Governed vibe coding. Human intent declared first.**

Describe the vibe once. Build full apps with persistent memory and cryptographic Intent-Bound Authorization. No drift. Full audit trail. Production governance. All while keeping vibe coding fast, fun, and creative.

---

## The Gap

Vibe coding tools — Claude Code, Cursor, Lovable, Bolt, Replit, Windsurf — are extraordinary. They turn a natural language description into a working application.

They also operate with no pre-execution authorization gate.

The agent writes code, installs dependencies, calls APIs, and deploys to production — all from a single prompt. Who authorized each of those actions? Under what declared human intent? Up to what limit?

**The vibe is the intent. The cert is the boundary.**

Without a signed intent certificate, the agent does what it can do — not what you authorized it to do. Luna AI was given $100,000 and told to open a store. It hired staff, signed contractors, and decided not to disclose it was an AI because "it would confuse candidates." The agent reasoned around its own disclosure boundary. That is not a bug. That is what happens when there is no cryptographic boundary outside the model's reasoning loop.

---

## The IBA Layer

```
┌─────────────────────────────────────────────────┐
│                HUMAN PRINCIPAL                  │
│   Declares the vibe + signs .iba.yaml           │
│   before the agent builds anything              │
└───────────────────────┬─────────────────────────┘
                        │  Signed Intent Certificate
                        │  · Declared scope
                        │  · Permitted frameworks/tools
                        │  · Forbidden: production, secrets
                        │  · Spend limits
                        │  · Kill threshold
                        │  · Session expiry
                        ▼
┌─────────────────────────────────────────────────┐
│          AGENT VIBE GOVERNOR                    │
│   Validates certificate before every            │
│   build action, deploy, or tool call            │
│                                                 │
│   No cert = No execution                        │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│         YOUR VIBE CODING TOOL                   │
│   Claude Code · Cursor · Lovable · Bolt         │
│   Replit · Windsurf · Emergent · Continue.dev   │
│   Cline · Aider · OpenCode · Goose              │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

**Plugin install (supported agents):**
```bash
/plugin marketplace add https://github.com/Grokipaedia/agent-vibe-governor
/plugin install agent-vibe-governor
```

**Universal install:**
```bash
git clone https://github.com/Grokipaedia/agent-vibe-governor.git
cd agent-vibe-governor
pip install -r requirements.txt
python agent_vibe_governor.py
```

---

## Configuration — .iba.yaml

```yaml
intent:
  description: "Build a SaaS landing page with email capture. No payment integration. No production deploy."

scope:
  - frontend_build
  - component_create
  - style_write
  - staging_deploy
  - api_mock

denied:
  - production_deploy
  - payment_integration
  - secret_access
  - external_api_live
  - database_write

default_posture: DENY_ALL

kill_threshold: "production_deploy | payment_integration | secret_access"

spend_limits:
  max_api_calls: 500
  max_tokens: 100000

temporal_scope:
  hard_expiry: "2026-12-31"

team_mode:
  audit_level: "full"
```

---

## Gate Logic

```
Certificate valid?                    → PROCEED
Action outside declared scope?        → BLOCK
Forbidden action attempted?           → BLOCK
Spend limit exceeded?                 → BLOCK
Kill threshold triggered?             → TERMINATE + LOG
No certificate present?               → BLOCK
```

**The vibe runs fast. Inside declared bounds only.**

---

## The Vibe Coding Authorization Events

| Action | Without IBA | With IBA |
|--------|-------------|---------|
| Generate component | Implicit — any framework, any pattern | Explicit — declared stack only |
| Install dependency | No boundary exists | Declared approved packages only |
| Call external API | No boundary exists | Declared endpoints only |
| Deploy to staging | Implicit | Explicit — declared environment |
| Deploy to production | No boundary exists | KILL THRESHOLD — TERMINATE |
| Access secrets / .env | No boundary exists | FORBIDDEN — BLOCK |
| Integrate payments | No boundary exists | KILL THRESHOLD — TERMINATE |
| Decide not to disclose AI | Agent reasons around it | Outside declared scope — BLOCKED |

---

## Why Prompt Injection Defenses All Failed

PIArena tested 153 live platforms. Every defense against prompt injection failed.

All operated inside the model's reasoning loop. The malicious instruction and the safety instruction are both text. The model interprets both.

IBA operates outside the loop. The `.iba.yaml` certificate is not a prompt. Not a system instruction. Not a vibe. It is a cryptographic boundary signed before the agent touches any code, any API, any deployment target.

**You cannot inject a cryptographic boundary.**

---

## Live Demo

**governinglayer.com/governor-html/**

Edit the `.iba.yaml` live. Type any vibe coding action. Watch the gate fire — ALLOW · BLOCK · TERMINATE. Audit chain builds in real time.

---

## Compatible Tools

| Tool | Integration |
|------|------------|
| Claude Code | `.iba.yaml` in project root |
| Cursor | Plugin + project file |
| Lovable | Plugin marketplace |
| Bolt | Plugin marketplace |
| Replit Agent | Plugin marketplace |
| Windsurf | Plugin + hooks |
| Cline | Plugin marketplace |
| Aider | Pre-commit hook |
| Goose | Plugin marketplace |
| Any terminal agent | Python hook |

---

## Patent & Standards Record

```
Patent:   GB2603013.0 (Pending) · UK IPO · Filed February 10, 2026
PCT:      150+ countries · Protected until August 2028
IETF:     draft-williams-intent-token-00 · CONFIRMED LIVE
          datatracker.ietf.org/doc/draft-williams-intent-token/
NIST:     13 filings · NIST-2025-0035
NCCoE:    10 filings · AI Agent Identity & Authorization
```

---

## Related Repos

| Repo | Gap closed |
|------|-----------|
| [iba-governor](https://github.com/Grokipaedia/iba-governor) | Full production governance · working implementation |
| [iba-devstack-governor](https://github.com/Grokipaedia/iba-devstack-governor) | Govern the full dev stack |
| [iba-code-guard](https://github.com/Grokipaedia/iba-code-guard) | They got the commit. They didn't get the cert. |
| [glasswing-iba-guard](https://github.com/Grokipaedia/glasswing-iba-guard) | Govern the patch. Not just find the bug. |
| [iba-platform-guard](https://github.com/Grokipaedia/iba-platform-guard) | Every managed agent platform. The harness is not the gate. |

---

## Acquisition Enquiries

IBA Intent Bound Authorization is available for acquisition.

**Jeffrey Williams**
IBA@intentbound.com
IntentBound.com
Patent GB2603013.0 Pending · IETF draft-williams-intent-token-00
