---
name: ramus
description: Drive Ramus Android emulator sessions to verify APKs, PR previews, and app flows, or inspect changes during a Ramus development session.
allowed-tools: Bash(ramus:*), Bash(npx ramus-cli:*)
---

# Verify Android apps with Ramus

Use `ramus` (or `npx ramus-cli`, Node.js 22+) for live device verification.
Read [the agent reference](https://ramus.dev/agents.md) for additional
commands and current interface boundaries. Run unit-testable logic with the
project's test suite; build APKs with its own tooling.

## Select access and build

Run `ramus status` to inspect credentials, repository installation, and live
sessions. Without credentials, `ramus trial` creates a locally stored
60-minute sandbox key. Trials support APK/demo verification, but not PRs or
adb/dev tunnels. For signed-in access, have the user create a key at
https://ramus.dev/settings and set `RAMUS_API_KEY` in your environment;
never ask for credentials in chat or put them in URLs.

Start with one source:

- `ramus session start --apk app-debug.apk --wait` for a local build.
- `ramus session start --demo --wait` to try the demo (`--demo waypoint` names one of the demo apps; `ramus session start --help` lists them).
- `ramus session start --pr owner/repo#123 --wait` for a ready PR build.

PRs require signed-in GitHub access and the repository's Ramus GitHub App
installation. If missing, `ramus install` provides a URL for the human to
complete setup; `ramus install --wait` polls for completion. APK/demo use
does not require GitHub setup.

Share the returned `watchUrl` immediately and repeat the current link in
your final report. Anyone with it can watch and control the app without an account;
while valid it can offer a fresh launch after the old session ends, subject
to relaunch limits, capacity, and the app or build remaining available.
Fresh launches do not restore previous device state. If the link is absent,
use `ramus session share` while live. Minting a link replaces and revokes the
previous one, including the original watch URL; share the replacement.
Do not post control links publicly. `session share --revoke` revokes the
session's link; ending the session does not.

Commands default to the last session; use `--session <id>` when needed.

## Observe → act → verify

1. Read `ramus snapshot`, preferably `--find "label"` for a known target.
   Use the returned `ref` and `gen` together; choose clickable elements.
   Labels may be in `contentDesc`, not just `text`.
2. Act with `ramus tap <ref> --gen <gen>`, substituting actual values from
   that observation. Add `--expect "result"` or `--expect-gone "old text"`
   to verify the tap's outcome.
3. Re-observe before deciding the next action. Accepted actions and later
   snapshots invalidate refs. On `stale_ref`, resolve the target again;
   never guess a generation or script a chain of invented refs.

For text entry, `ramus type "hello" --ref <ref> --gen <gen>` focuses the
field, replaces its contents, and attempts read-back verification. Check
`verified`; read-back can be unavailable. `--submit` presses Enter and
`--no-verify` skips read-back. Plain `type` requires focus first.

After navigation, use `ramus wait --stable`, `--text "Welcome"`, or
`--gone "Loading"`. Stability is two matching snapshots, not proof of app
completion. `wait --text` supplies matching refs and a generation you can
use until another observation/action supersedes them.

- Close the keyboard with `ramus press IME_HIDE`; repeated BACK can exit
  the app. `ramus app launch` restores the app after HOME, backing out,
  a crash, or reinstall. Re-snapshot afterward.
- Scroll with `ramus swipe 0.5,0.8 0.5,0.2`, then re-snapshot.
- For an empty or incomplete tree, inspect `ramus screenshot --out screen.jpg`
  and use normalized coordinate taps. `--include-offscreen` cannot expose
  recycled list rows. Only override non-clickable ref rejection with
  `--force` after visually checking the target.
- On a crash or hang, collect `ramus logcat --limit 200` and a screenshot
  before relaunching. Report what you observed, including where the flow
  diverged, rather than treating an accepted input as success.

Finish with evidence and the watch URL. Use `ramus session end` when done,
but leave the session running during an active human handoff.

## Iterate locally

For code changes, `ramus dev` detects Expo/React Native/Flutter/Gradle and
runs local tooling against a tunneled session. It requires a signed-in key,
local adb, and the framework SDKs. Override with `--shape` or `--app-dir`;
`--apk` supplies a build where supported. First builds can take minutes:
inspect `ramus dev status` and its log tail.

Expo/RN use Fast Refresh. `ramus dev reload` triggers Flutter hot reload
(`--full` restarts) or Gradle reinstall. Observe the app after each change.
`ramus dev stop` stops the process and tunnel, keeping the session.
`ramus adb` alone returns a serial for `adb -s <serial>` commands.
Avoid `adb root`, `adb unroot`, and `adb reboot`, which can break the
session, and `adb reverse --remove-all`, which removes dev port mappings.

MCP supports device driving and demo/PR/known-URI session starts, but local
APK upload, adb, and dev require the CLI. MCP handoff fields are `watch_url`
and `share_url`; discover its current tools at the endpoint in the reference.

<!-- BEGIN GENERATED RAMUS CONTRACT -->

## Current contract values

- Session idle timeout: 30 minutes (60 minutes while an adb tunnel is open).
- Share links: 72 hours by default, up to 7 days (trial keys up to 72 hours).
- Trial limits: 1 active session, 30-minute idle, 150 MB APK.
- Signed-in APK cap: 300 MB.
- TTL accepts seconds, minutes, hours, and days from 60 seconds through 7 days; the default is 72 hours.
- Session start timeout: the CLI waits 180s and ends a still-starting placement by default; `--keep-on-timeout` leaves it for polling. MCP waits 120s and keeps the placement for `android_session_status`.

MCP parity is additive. The shared tool contract currently exposes:
- android_tap: ref, gen, x, y, force, expect, expect_gone
- android_type: text, ref, gen, submit, no_verify
- android_press: key
- android_snapshot: find, include_offscreen
- android_wait_for: text, text_gone, stable, timeout_ms

<!-- END GENERATED RAMUS CONTRACT -->
