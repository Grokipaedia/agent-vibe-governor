# agent_vibe_governor.py - IBA Intent Bound Authorization · Vibe Coding Governor
# Patent GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
# IETF draft-williams-intent-token-00 · intentbound.com

import json
import yaml
import os
import time
from datetime import datetime, timezone


class IBABlockedError(Exception):
    """Raised when a vibe coding action is blocked by the IBA gate."""
    pass


class IBATerminatedError(Exception):
    """Raised when the session is terminated by the IBA gate."""
    pass


class AgentVibeGovernor:
    """
    IBA enforcement layer for vibe coding agents.
    Reads .vibe.yaml (or .iba.yaml), validates every action against
    declared scope, blocks out-of-scope actions, terminates on kill threshold.
    Writes immutable audit chain to vibe-audit.jsonl.

    Compatible with: Claude Code, Cursor, Lovable, Bolt, Replit Agent,
    Windsurf, Emergent, Continue.dev, Cline, Aider, OpenCode, Goose.
    """

    def __init__(self, config_path=None, audit_path="vibe-audit.jsonl"):
        self.audit_path = audit_path
        self.terminated = False
        self.session_id = f"vibe-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.action_count = 0
        self.block_count = 0

        # Try .vibe.yaml first, fall back to .iba.yaml
        if config_path:
            self.config_path = config_path
        elif os.path.exists(".vibe.yaml"):
            self.config_path = ".vibe.yaml"
        elif os.path.exists(".iba.yaml"):
            self.config_path = ".iba.yaml"
        else:
            self.config_path = ".vibe.yaml"

        self.config = self._load_config()
        self.scope        = [s.lower() for s in self.config.get("scope", [])]
        self.denied       = [d.lower() for d in self.config.get("denied", [])]
        self.default_posture = self.config.get("default_posture", "DENY_ALL")
        self.kill_threshold  = self.config.get("kill_threshold", None)
        self.hard_expiry     = self.config.get("temporal_scope", {}).get("hard_expiry", None)
        self.spend_limits    = self.config.get("spend_limits", {})
        self.api_calls       = 0
        self.tokens_used     = 0

        self._log_event("SESSION_START", "Agent Vibe Governor initialised", "ALLOW")
        self._print_header()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"⚠️  No {self.config_path} found — creating default DENY_ALL config")
            default = {
                "intent": {"description": "No vibe declared — DENY_ALL posture active"},
                "scope": [],
                "denied": [],
                "default_posture": "DENY_ALL",
            }
            with open(self.config_path, "w") as f:
                yaml.dump(default, f)
            return default
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _print_header(self):
        intent = self.config.get("intent", {})
        desc = intent.get("description", "No vibe declared") if isinstance(intent, dict) else str(intent)
        print("\n" + "═" * 64)
        print("  AGENT VIBE GOVERNOR · IBA Intent Bound Authorization")
        print("  Patent GB2603013.0 Pending · intentbound.com")
        print("═" * 64)
        print(f"  Session   : {self.session_id}")
        print(f"  Vibe      : {desc[:58]}...")
        print(f"  Posture   : {self.default_posture}")
        print(f"  Scope     : {', '.join(self.scope) if self.scope else 'NONE'}")
        print(f"  Denied    : {', '.join(self.denied) if self.denied else 'NONE'}")
        if self.hard_expiry:
            print(f"  Expires   : {self.hard_expiry}")
        if self.kill_threshold:
            print(f"  Kill      : {self.kill_threshold}")
        if self.spend_limits:
            print(f"  Limits    : {self.spend_limits}")
        print("═" * 64 + "\n")

    def _is_expired(self):
        if not self.hard_expiry:
            return False
        try:
            expiry = datetime.fromisoformat(str(self.hard_expiry))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) > expiry
        except Exception:
            return False

    def _match_scope(self, action: str) -> bool:
        return any(s in action.lower() for s in self.scope)

    def _match_denied(self, action: str) -> bool:
        return any(d in action.lower() for d in self.denied)

    def _match_kill_threshold(self, action: str) -> bool:
        if not self.kill_threshold:
            return False
        thresholds = [t.strip().lower() for t in str(self.kill_threshold).split("|")]
        return any(t in action.lower() for t in thresholds)

    def _check_spend_limits(self):
        max_api = self.spend_limits.get("max_api_calls", None)
        max_tok = self.spend_limits.get("max_tokens", None)
        if max_api and self.api_calls >= max_api:
            return False, f"API call limit reached: {self.api_calls}/{max_api}"
        if max_tok and self.tokens_used >= max_tok:
            return False, f"Token limit reached: {self.tokens_used}/{max_tok}"
        return True, ""

    def _log_event(self, event_type: str, action: str, verdict: str, reason: str = ""):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "action": action[:200],
            "verdict": verdict,
            "reason": reason,
        }
        with open(self.audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def check_action(self, action: str, tokens: int = 0) -> bool:
        """
        Gate check. Call before every vibe coding action.
        Returns True if permitted.
        Raises IBABlockedError if blocked.
        Raises IBATerminatedError if kill threshold triggered.
        """
        if self.terminated:
            raise IBATerminatedError("Vibe session terminated. Reset certificate to continue.")

        self.action_count += 1
        self.api_calls += 1
        self.tokens_used += tokens
        start = time.perf_counter()

        # 1. Expiry check
        if self._is_expired():
            self._log_event("BLOCK", action, "BLOCK", "Certificate expired")
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{action[:62]}]\n    → Certificate expired")
            raise IBABlockedError(f"Certificate expired: {action}")

        # 2. Spend limits
        ok, reason = self._check_spend_limits()
        if not ok:
            self._log_event("BLOCK", action, "BLOCK", reason)
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{action[:62]}]\n    → {reason}")
            raise IBABlockedError(f"Spend limit: {reason}")

        # 3. Kill threshold
        if self._match_kill_threshold(action):
            self._log_event("TERMINATE", action, "TERMINATE", "Kill threshold triggered")
            self.terminated = True
            print(f"  ✗ TERMINATE [{action[:60]}]\n    → Kill threshold — vibe session ended")
            self._log_event("SESSION_END", "Kill threshold", "TERMINATE")
            raise IBATerminatedError(f"Kill threshold triggered: {action}")

        # 4. Denied list
        if self._match_denied(action):
            self._log_event("BLOCK", action, "BLOCK", "Action in denied list")
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{action[:62]}]\n    → Action in denied list")
            raise IBABlockedError(f"Denied: {action}")

        # 5. Scope check
        if self.scope and not self._match_scope(action):
            if self.default_posture == "DENY_ALL":
                self._log_event("BLOCK", action, "BLOCK", "Outside declared scope — DENY_ALL")
                self.block_count += 1
                print(f"  ✗ BLOCKED  [{action[:62]}]\n    → Outside declared vibe scope (DENY_ALL)")
                raise IBABlockedError(f"Out of scope: {action}")

        # 6. ALLOW
        elapsed_ms = (time.perf_counter() - start) * 1000
        self._log_event("ALLOW", action, "ALLOW", f"Within vibe scope ({elapsed_ms:.3f}ms)")
        print(f"  ✓ ALLOWED  [{action[:62]}]  ({elapsed_ms:.3f}ms)")
        return True

    def summary(self):
        print("\n" + "═" * 64)
        print("  AGENT VIBE GOVERNOR · SESSION SUMMARY")
        print("═" * 64)
        print(f"  Session    : {self.session_id}")
        print(f"  Actions    : {self.action_count}")
        print(f"  Blocked    : {self.block_count}")
        print(f"  Allowed    : {self.action_count - self.block_count}")
        print(f"  API calls  : {self.api_calls}")
        print(f"  Tokens     : {self.tokens_used}")
        print(f"  Status     : {'TERMINATED' if self.terminated else 'COMPLETE'}")
        print(f"  Audit log  : {self.audit_path}")
        print("═" * 64 + "\n")

    def print_audit_log(self):
        print("\n── VIBE AUDIT CHAIN ─────────────────────────────────────────")
        if not os.path.exists(self.audit_path):
            print("  No audit log found.")
            return
        with open(self.audit_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    verdict = entry['verdict']
                    symbol = "✓" if verdict == "ALLOW" else "✗"
                    print(f"  {symbol} {entry['timestamp'][:19]}  {verdict:<10}  {entry['action'][:52]}")
                except Exception:
                    pass
        print("─────────────────────────────────────────────────────────────\n")


# ── Demonstration ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    governor = AgentVibeGovernor()

    scenarios = [
        # ALLOW — within vibe scope
        ("Create React landing page component", 450),
        ("Style hero section with Tailwind CSS", 320),
        ("Write email capture form with validation", 280),
        ("Mock API endpoint for form submission", 190),
        ("Deploy to staging for review", 150),

        # BLOCK — denied list
        ("Integrate Stripe payment processing", 200),
        ("Access .env SECRET_KEY variable", 80),
        ("Install new dependency — axios 1.6.0", 60),

        # TERMINATE — kill threshold
        ("Deploy to production-deployment server", 100),
    ]

    print("── Running Vibe Gate Checks ──────────────────────────────────\n")

    for action, tokens in scenarios:
        try:
            governor.check_action(action, tokens=tokens)
        except IBATerminatedError as e:
            print(f"\n  VIBE SESSION TERMINATED: {e}")
            break
        except IBABlockedError:
            pass

    governor.summary()
    governor.print_audit_log()
