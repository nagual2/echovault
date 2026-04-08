# Local Memory

You have access to a persistent memory system via the `memory` CLI. Use it to save important decisions, patterns, bugs, context, and learnings — and retrieve them in future sessions.

## At Session Start

Check available memories for this project:

```bash
memory context --project
```

Then use `memory search <query>` to retrieve full details on any relevant memory.

## Saving Memories

When you make a decision, fix a bug, discover a pattern, set up infrastructure, or learn something non-obvious:

```bash
memory save \
  --title "Short descriptive title" \
  --what "What happened or was decided" \
  --why "Reasoning behind it" \
  --impact "What changed as a result" \
  --tags "tag1,tag2,tag3" \
  --category "decision" \
  --related-files "src/auth.ts,src/middleware.ts" \
  --source "codex" \
  --details "Context:

             Options considered:
             - Option A
             - Option B

             Decision:
             Tradeoffs:
             Follow-up:"
```

Categories: `decision`, `pattern`, `bug`, `context`, `learning`

## Searching Memories

```bash
memory search "your query"                 # search all projects
memory search "your query" --project       # current project only
memory search "your query" --source codex  # from specific agent
```

## Getting Full Details

When search results show "Details: available":

```bash
memory details <memory-id>
```

## Session Protocol

### Start of Session
1. **Load context**: `memory context --project`
2. **Search relevant**: `memory search "<topic>"`
3. **Get details**: `memory details <id>` if needed

### End of Session (MANDATORY)
Before finishing ANY work:
1. Review what was done
2. Determine what to save (see categories below)
3. Save with `--source claude-code`
4. Verify: `memory context --project`

### What to Save

| MUST SAVE | NEVER SAVE |
|-----------|------------|
| Architectural decisions | Trivial changes (typos) |
| Bug fixes (root cause + solution) | Info obvious from code |
| Non-obvious patterns | Duplicates (search first!) |
| Infrastructure/tooling setup | |
| User corrections/clarifications | |

### Categories
- `decision` — architectural/design choices
- `pattern` — discovered patterns or gotchas
- `bug` — fixes with root causes
- `setup` — infrastructure configuration
- `learning` — lessons learned
- `context` — important project context

## Rules

- **Always capture thorough details** — never omit reasoning or context
- **Never include API keys, secrets, or credentials** in any field
- **Wrap sensitive values** in `<redacted>` tags if referencing them
- **Search before deciding** — check if a decision was already made
- **Save after doing** — capture decisions, fixes, and learnings as you go
- **Use `--source`** — identify your agent: `claude-code`, `codex`, or `cursor`
