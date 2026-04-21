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
are opt-in via the `HEWN_LOCALE` environment variable (comma-separated):

```bash
HEWN_LOCALE=en          # default — English only
HEWN_LOCALE=en,it       # English + Italian
HEWN_LOCALE=en,es,fr    # English + Spanish + French
HEWN_LOCALE=en,de       # English + German
```

Shipped locales: `en`, `it`, `es`, `fr`, `de`. `en` and `it` are
validated against real prompt corpora; `es`/`fr`/`de` are synthesized
1:1 from the Italian patterns and await community curation — PRs with
real-prompt evidence welcome at `hooks/locales/<code>.py`.

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
