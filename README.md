# android-use

Android-use for coding agents. Give Claude Code, Codex, Cursor, Gemini CLI or any agent with a shell a disposable Android device it can see, tap, type on, screenshot and read logs from, then watch or take over in your browser.

## Install

Any agent that supports skills, via the [skills CLI](https://skills.sh):

```sh
npx skills add ramus-dev/android-use
```

Claude Code, by hand: copy [`skills/android-use/SKILL.md`](skills/android-use/SKILL.md) to `.claude/skills/android-use/SKILL.md`.

Gemini CLI, as an extension (bundles the skill and the Ramus MCP server):

```sh
gemini extensions install https://github.com/ramus-dev/android-use
```

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

Android only. Free during alpha.

`SKILL.md` is generated from the Ramus product contracts; the canonical copy is served at https://ramus.dev/skill.md.
