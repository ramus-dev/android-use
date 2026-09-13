# Ramus skill for coding agents

Give Claude Code, Codex, Cursor or any agent with a shell a disposable Android emulator it can drive: start a session, read the UI tree, tap, type, screenshot, read logcat, and hand you a browser link to watch or take over.

## Install

Copy [`SKILL.md`](SKILL.md) to `.claude/skills/ramus/SKILL.md` for Claude Code, or into your agent's skill directory. The CLI trial needs no account:

```sh
npx ramus-cli trial
npx ramus-cli session start --apk app-debug.apk --wait
```

## Links

- Docs: https://ramus.dev/docs/agents
- Agent reference: https://ramus.dev/agents.md
- MCP endpoint (Streamable HTTP, API key): https://api.ramus.dev/api/mcp
- CLI on npm: https://www.npmjs.com/package/ramus-cli

Ramus runs stock Android images on its own fleet, streams them over WebRTC, and is free during alpha. Android only.

`SKILL.md` is generated from the Ramus product contracts; the canonical copy is served at https://ramus.dev/skill.md.
