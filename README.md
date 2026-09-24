# Ramus android-use

Android-use for coding agents, powered by [Ramus](https://ramus.dev). Give Claude Code, Codex, Cursor, Gemini CLI or any agent with a shell a disposable cloud Android emulator it can see, tap, type on, screenshot and read logs from, then watch or take over in your browser.

This plugin connects to the Ramus hosted service. It needs a Ramus account (free during alpha) or a 60-minute CLI trial.

## Install

Claude Code, as a plugin (the android-use skill plus the Ramus MCP server; you are asked for an optional API key):

```
/plugin marketplace add ramus-dev/android-use
/plugin install ramus@ramus
```

Cursor, Codex, GitHub Copilot, Kiro and other [Agent Plugins](https://agent-plugins.org) clients: install this repository as a plugin (`plugin.json` at the root).

Any agent that supports skills, via the [skills CLI](https://skills.sh):

```sh
npx skills add ramus-dev/android-use
```

Claude Code, by hand: copy [`skills/android-use/SKILL.md`](skills/android-use/SKILL.md) to `.claude/skills/android-use/SKILL.md`.

Gemini CLI, as an extension (bundles the skill and the Ramus MCP server):

```sh
gemini extensions install https://github.com/ramus-dev/android-use
```

Any MCP client (Cline, Claude Desktop, Cursor, Windsurf, VS Code), as a remote server. Streamable HTTP, no local process:

```json
{
  "mcpServers": {
    "ramus": {
      "url": "https://api.ramus.dev/api/mcp",
      "headers": { "Authorization": "Bearer <RAMUS_API_KEY>" }
    }
  }
}
```

Create the key at https://ramus.dev/settings. The server exposes `android_*` tools (start a session from a demo app or pull request, snapshot the UI tree, tap, type, press, wait, screenshot, logs, share); list them with `tools/list`. Local APK upload and the dev loop need the CLI below.

The trial needs no account:

```sh
npx ramus-cli trial
npx ramus-cli session start --apk app-debug.apk --wait
```

## How it works

The device is a real Android emulator running stock Google images on the [Ramus](https://ramus.dev) fleet, streamed over WebRTC. The skill teaches the agent the observe, act, verify loop: read a snapshot of the UI tree, act on a referenced element, then check the result before moving on.

## Links

- Docs: https://ramus.dev/docs/agents
- Agent reference: https://ramus.dev/agents.md
- MCP endpoint (Streamable HTTP, API key): https://api.ramus.dev/api/mcp
- CLI on npm: https://www.npmjs.com/package/ramus-cli

- Privacy policy: https://ramus.dev/privacy
- Terms: https://ramus.dev/terms
- Acceptable use: https://ramus.dev/acceptable-use
- Support: hello@ramus.dev · Security: security@ramus.dev

Android only. Free during alpha. For testing apps you build or are authorized to test.

`SKILL.md` is generated from the Ramus product contracts; the canonical copy is served at https://ramus.dev/skill.md.
