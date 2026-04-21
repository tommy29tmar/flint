# Hewn — Claude Code integration

Hewn is a Claude Code CLI wrapper. It runs `claude` with:

- A thinking-mode **system prompt** appended via `--append-system-prompt`,
  which routes each turn to one of six shapes (IR, prose+code,
  prose-findings, prose-polished, prose-polished+code, prose-caveman)
  based on task structure.
- A per-turn **drift-fix hook** registered via `--settings`, which
  classifies every user prompt and re-injects the routing directive as
  `additionalContext`. This prevents the T2+ drift observed when relying
  on the system prompt alone.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/tommy29tmar/hewn/main/integrations/claude-code/install.sh | bash
```

## Usage

```bash
hewn                     # interactive session with Hewn thinking-mode
hewn -p "your prompt"    # non-interactive
```

Any flag accepted by `claude` is forwarded: `hewn --model claude-opus-4-7 -p "…"`.

The default `claude` command is untouched.

## Locales

The classifier ships with English patterns by default. Other languages
are opt-in via the `--locale` flag or the `HEWN_LOCALE` environment
variable (both accept comma-separated stacks; the flag wins when both
are set):

```bash
hewn --locale en,it       # English + Italian for this invocation
hewn --locale en,es,fr    # English + Spanish + French
export HEWN_LOCALE=en,it  # persistent across sessions
```

Shipped locales: `en`, `it`, `es`, `fr`, `de`. All five are validated
at 100% coverage on a 12-prompt realistic corpus spanning every route;
`en` and `it` additionally draw from real-prompt history, while
`es`/`fr`/`de` patterns were synthesized from the Italian baseline —
PRs expanding them with more real-prompt evidence are welcome at
`hooks/locales/<code>.py`.

## Files installed

- `~/.local/bin/hewn` — the wrapper
- `~/.claude/hewn_thinking_system_prompt.txt` — the system prompt
- `~/.claude/hooks/hewn_drift_fixer.py` — the UserPromptSubmit hook
- `~/.claude/hooks/locales/{en,it,es,fr,de}.py` — locale patterns

## Uninstall

```bash
rm -f ~/.local/bin/hewn \
      ~/.claude/hewn_thinking_system_prompt.txt \
      ~/.claude/hooks/hewn_drift_fixer.py
rm -rf ~/.claude/hooks/locales
```
