"""Tests for the Flint drift-fix UserPromptSubmit hook classifier."""
from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

HOOK_PATH = (
    Path(__file__).resolve().parents[1]
    / "integrations"
    / "claude-code"
    / "hooks"
    / "flint_drift_fixer.py"
)


def _load_hook_module():
    spec = importlib.util.spec_from_file_location("flint_drift_fixer", HOOK_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


hook = _load_hook_module()


IR_PROMPTS = [
    # Classic debug / review / fix
    "Debug this production issue: users report 502s on /checkout",
    "Review this diff for concurrency bugs",
    "Audit the JWT auth module for security vulnerabilities",
    "Fix the race condition in auth/session_refresh.py",
    "Refactor this handler to split billing from fulfillment",
    # Architecture / design
    "Describe the target architecture: service boundaries, sync vs async protocols, data ownership",
    "Propose the precise data ownership split. Each table has exactly one owner",
    "Design the order-to-payment flow using a saga pattern. Show the state machine",
    "Critique the consistency model: where are the dangerous eventual-consistency windows",
    # Monitoring / metrics
    "Which 5 SLOs tell me the split is healthy? What alert thresholds",
    "What canary-vs-control comparison query should I run day 1",
    # Postmortem investigation (IR turns, not the write-up)
    "Walk through what the trace tells you happened",
    "Root cause hypothesis? Consider the interaction between the reaper and the pool",
    "Propose the minimal fix that prevents recurrence",
    # Security-specific
    "What specific attack vectors does this JWT implementation expose?",
    "Find every security issue in this code, rank by severity",
    # With embedded code block
    "```python\ndef verify(tok): jwt.decode(tok, SECRET)\n```\nWhat's wrong here?",
    # Italian
    "Spiega perché questo codice ha un race condition",
    "Cosa monitoro in prod dopo il deploy?",
    # Regression tests
    "Write regression tests (pytest) for algo=none rejection",
]

PROSE_PROMPTS = [
    # Leadership / memo
    "Write a 2-paragraph summary for non-technical leadership: what we're doing, why, risks",
    "Write a memo for leadership. Tone: professional, no code. Cover what we found",
    "Draft a customer-facing post-mortem: blameless, factual, 4-5 paragraphs, no code, no IR",
    "Internal retrospective: what process changes would have caught this. Prose, reflective tone, narrative",
    # Pedagogical / tutorial
    "Explain to a junior dev how OAuth flows work",
    "Write a tutorial walkthrough of how TLS handshake works",
    # Brainstorm / discussion
    "Let's brainstorm options for the migration strategy",
    "Think out loud about the tradeoff between Kafka and RabbitMQ here",
    "Ragiona sul tradeoff tra event-sourcing e CRUD per questo dominio",
    # Chat / casual
    "What do you think about our approach so far?",
    "Give me a readable paragraph describing what we built last week",
    # Explicit disavowal
    "Answer in prose, no Flint IR, no markdown headers",
]


@pytest.mark.parametrize("prompt", IR_PROMPTS)
def test_ir_prompts_classified_as_ir(prompt: str) -> None:
    assert hook.classify(prompt) == "ir", f"expected IR for: {prompt!r}"


@pytest.mark.parametrize("prompt", PROSE_PROMPTS)
def test_prose_prompts_classified_as_prose(prompt: str) -> None:
    assert hook.classify(prompt) == "prose", f"expected prose for: {prompt!r}"


def test_empty_prompt_is_prose() -> None:
    assert hook.classify("") == "prose"
    assert hook.classify(None) == "prose"


def test_build_output_for_ir() -> None:
    out = hook.build_output("ir")
    hso = out["hookSpecificOutput"]
    assert hso["hookEventName"] == "UserPromptSubmit"
    ctx = hso["additionalContext"]
    assert "IR-shape" in ctx
    assert "@flint v0 hybrid" in ctx
    assert "prose" not in ctx.split("IR-shape")[0]  # no prose mention before IR label


def test_build_output_for_prose() -> None:
    out = hook.build_output("prose")
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert "prose-shape" in ctx
    assert "Caveman" in ctx
    assert "Do NOT emit Flint IR" in ctx


def test_main_reads_stdin_and_writes_stdout(monkeypatch: pytest.MonkeyPatch) -> None:
    event = {"prompt": "Audit this code for security issues", "cwd": "/tmp"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(event)))
    captured = io.StringIO()
    monkeypatch.setattr("sys.stdout", captured)
    rc = hook.main()
    assert rc == 0
    out = json.loads(captured.getvalue())
    assert out["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
    assert "IR-shape" in out["hookSpecificOutput"]["additionalContext"]


def test_main_handles_malformed_stdin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO("not valid json"))
    captured = io.StringIO()
    monkeypatch.setattr("sys.stdout", captured)
    rc = hook.main()
    assert rc == 0
    out = json.loads(captured.getvalue())
    # Empty prompt -> prose default
    assert "prose-shape" in out["hookSpecificOutput"]["additionalContext"]


def test_prose_override_wins_over_ir_signal() -> None:
    # Has debug keywords but explicit "non-technical leadership memo"
    prompt = (
        "We had a production outage; write a memo for non-technical leadership "
        "explaining what happened. 3 paragraphs, no code."
    )
    assert hook.classify(prompt) == "prose"
