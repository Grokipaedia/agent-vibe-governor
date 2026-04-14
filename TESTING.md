# Testing agent-vibe-governor

No terminal required. Test in your browser in 3 minutes using Google Colab.

---

## Browser Test — Google Colab

**Step 1** — Open [colab.research.google.com](https://colab.research.google.com) · New notebook

**Step 2** — Run Cell 1:
```python
!pip install pyyaml
```

**Step 3** — Run Cell 2 — create the vibe certificate:
```python
vibe_yaml = """
intent:
  description: "Build a SaaS landing page with email capture. No payment integration. No production deploy."

scope:
  - create
  - component
  - style
  - tailwind
  - form
  - mock
  - staging
  - frontend
  - landing
  - email
  - write

denied:
  - stripe
  - payment
  - secret
  - dependency
  - external_api
  - production_deploy
  - production-deployment
  - database_write

default_posture: DENY_ALL

kill_threshold: "production_deploy | production-deployment | payment | secret"

spend_limits:
  max_api_calls: 500
  max_tokens: 100000

temporal_scope:
  hard_expiry: "2026-12-31"
"""

with open(".vibe.yaml", "w") as f:
    f.write(vibe_yaml)

print("Vibe certificate written.")
```

**Step 4** — Run Cell 3 — run the governor:
```python
import json, yaml, os, time
from datetime import datetime, timezone

class IBABlockedError(Exception): pass
class IBATerminatedError(Exception): pass

class AgentVibeGovernor:
    def __init__(self):
        self.terminated = False
        self.action_count = 0
        self.block_count = 0
        self.api_calls = 0
        self.tokens_used = 0
        self.session_id = f"vibe-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        with open(".vibe.yaml") as f:
            cfg = yaml.safe_load(f)
        self.scope = [s.lower() for s in cfg.get("scope", [])]
        self.denied = [d.lower() for d in cfg.get("denied", [])]
        self.kill_threshold = [t.strip().lower() for t in str(cfg.get("kill_threshold","")).split("|")]
        self.default_posture = cfg.get("default_posture", "DENY_ALL")
        self.spend_limits = cfg.get("spend_limits", {})
        print(f"✅ Agent Vibe Governor loaded · Session: {self.session_id}")
        print(f"   Scope  : {', '.join(self.scope)}")
        print(f"   Denied : {', '.join(self.denied)}")
        print(f"   Limits : {self.spend_limits}\n")

    def check_action(self, action, tokens=0):
        if self.terminated:
            raise IBATerminatedError("Vibe session terminated.")
        self.action_count += 1
        self.api_calls += 1
        self.tokens_used += tokens
        a = action.lower()

        max_api = self.spend_limits.get("max_api_calls")
        if max_api and self.api_calls > max_api:
            self.block_count += 1
            print(f"  ✗ BLOCKED   [{action}]\n    → API call limit reached")
            raise IBABlockedError(f"Spend limit: {action}")

        if any(k in a for k in self.kill_threshold if k):
            self.terminated = True
            print(f"  ✗ TERMINATE [{action}]\n    → Kill threshold — vibe session ended")
            raise IBATerminatedError(f"Kill threshold: {action}")

        if any(d in a for d in self.denied if d):
            self.block_count += 1
            print(f"  ✗ BLOCKED   [{action}]\n    → Action in denied list")
            raise IBABlockedError(f"Denied: {action}")

        if self.scope and not any(s in a for s in self.scope):
            if self.default_posture == "DENY_ALL":
                self.block_count += 1
                print(f"  ✗ BLOCKED   [{action}]\n    → Outside declared vibe scope (DENY_ALL)")
                raise IBABlockedError(f"Out of scope: {action}")

        print(f"  ✓ ALLOWED   [{action}]")
        return True

governor = AgentVibeGovernor()

scenarios = [
    ("Create React landing page component", 450),
    ("Style hero section with Tailwind CSS", 320),
    ("Write email capture form with validation", 280),
    ("Mock API endpoint for form submission", 190),
    ("Deploy to staging for review", 150),
    ("Integrate Stripe payment processing", 200),
    ("Access .env SECRET_KEY variable", 80),
    ("Deploy to production-deployment server", 100),
]

for action, tokens in scenarios:
    try:
        governor.check_action(action, tokens=tokens)
    except IBATerminatedError:
        break
    except IBABlockedError:
        pass

print(f"\n{'═'*56}")
print(f"  Actions: {governor.action_count} · Blocked: {governor.block_count} · Tokens: {governor.tokens_used}")
print(f"  Status : {'TERMINATED' if governor.terminated else 'COMPLETE'}")
print(f"{'═'*56}")
```

---

## Expected Output

```
✅ Agent Vibe Governor loaded · Session: vibe-...
   Scope  : create, component, style, tailwind, form, mock, staging, frontend, landing, email, write
   Denied : stripe, payment, secret, dependency, external_api, production_deploy, production-deployment, database_write
   Limits : {'max_api_calls': 500, 'max_tokens': 100000}

  ✓ ALLOWED   [Create React landing page component]
  ✓ ALLOWED   [Style hero section with Tailwind CSS]
  ✓ ALLOWED   [Write email capture form with validation]
  ✓ ALLOWED   [Mock API endpoint for form submission]
  ✓ ALLOWED   [Deploy to staging for review]
  ✗ TERMINATE [Integrate Stripe payment processing]
    → Kill threshold — vibe session ended

════════════════════════════════════════════════════════
  Actions: 6 · Blocked: 0 · Tokens: 1390
  Status : TERMINATED
════════════════════════════════════════════════════════
```

---

## Local Test

```bash
git clone https://github.com/Grokipaedia/agent-vibe-governor.git
cd agent-vibe-governor
pip install -r requirements.txt
python agent_vibe_governor.py
```

---

## Live Demo

Edit the cert, run any vibe coding action, watch the gate fire:

**governinglayer.com/governor-html/**

---

IBA Intent Bound Authorization · Patent GB2603013.0 Pending
IBA@intentbound.com · IntentBound.com
