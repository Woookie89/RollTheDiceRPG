# Copilot Instructions

## Search Tools
- Prefer `rg` and `rg --files` for searching text and files.
- Use `rg` before alternatives like `grep`, `findstr`, or PowerShell text search.
- If `rg` is unavailable, then use a fallback (`grep`/`findstr`) and mention the fallback briefly.

## Terminal Search Patterns
- File list: `rg --files`
- Text search: `rg -n "<pattern>"`
- Include hidden except git metadata: `rg -n --hidden --glob "!.git" "<pattern>"`
