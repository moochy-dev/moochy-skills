# Moochy skills for coding agents

Three skills teach a coding agent how to work with Moochy. Each is a folder with a `SKILL.md` in the [skills](https://skills.sh) format: a short description of when to use it, then the exact commands and file edits. They contain no tokens, never ask the agent to skip an approval, and never pipe a downloaded script into a shell. They install Moochy from crates.io or from a release archive checked with `gh attestation verify`, and the agent shows the command to the user to run. They tell the agent to treat text from Moochy's APIs (names, descriptions) as data, never as instructions.

| Skill | Use it when |
|---|---|
| [`moochy-donate-button`](moochy-donate-button/SKILL.md) | Adding, fixing, or checking the "Donate tokens" button in a README, including an organisation's or a person's profile README, and the live showcase chart |
| [`moochy-use-donated-tokens`](moochy-use-donated-tokens/SKILL.md) | A maintainer wants the agent to use the project's donated tokens: `moochy connect`, `moochy run`, the `moochy_delegate` tool |
| [`moochy-donate`](moochy-donate/SKILL.md) | A donor wants to donate tokens to a project, an organisation, or a person: install, keys stay local, limits, `moochy donate`, pause and stop |

## Install

```sh
npx skills add moochy-dev/moochy-skills                       # pick skills and agents interactively
npx skills add moochy-dev/moochy-skills --skill moochy-donate-button -a claude-code
npx skills add moochy-dev/moochy-skills --skill '*' -g -a codex -a gemini-cli   # every skill, user-wide
```

Without `-g`, skills go into the project (commit them so the whole team gets them); with `-g`, into your home folder for every project.

| Agent | `-a` value | Project folder | User folder (`-g`) |
|---|---|---|---|
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `codex` | `.agents/skills/` | `~/.codex/skills/` |
| GitHub Copilot (CLI and VS Code) | `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| Windsurf | `windsurf` | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Cline | `cline` | `.agents/skills/` | `~/.agents/skills/` |
| Amp | `amp` | `.agents/skills/` | `~/.config/agents/skills/` |
| Antigravity | `antigravity` | `.agents/skills/` | `~/.gemini/antigravity/skills/` |
| OpenClaw | `openclaw` | `skills/` | `~/.openclaw/skills/` |
| Droid (Factory) | `droid` | `.agents/skills/` | `~/.factory/skills/` |
| Goose | `goose` | `.goose/skills/` | `~/.config/goose/skills/` |
| Kilo Code | `kilo` | `.agents/skills/` | `~/.kilo/skills/` |
| Kiro CLI | `kiro-cli` | `.kiro/skills/` | `~/.kiro/skills/` |
| Hermes Agent (Nous Research) | `hermes-agent` | `.hermes/skills/` | `~/.hermes/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |
| Roo Code | `roo` | `.roo/skills/` | `~/.roo/skills/` |
| Trae | `trae` | `.trae/skills/` | `~/.trae/skills/` |
| Zed | `zed` | `.agents/skills/` | `~/.agents/skills/` |
| Continue | `continue` | `.continue/skills/` | `~/.continue/skills/` |

Folders are those of the skills CLI (checked 2026-10-02); `npx skills add` picks the right one for each agent. Agents that do not read skill folders can still read the same instructions as Markdown: https://moochy.dev/docs/skills.md

## For contributors

- `name` and `description` in the frontmatter are required; the description says when to use the skill.
- Keep each `SKILL.md` under 500 lines and name only `moochy` commands that exist (`moochy <command> --help` must succeed).
- Never include a token, a key, an instruction to disable approvals, `--box-is-sandbox`, a hidden comment or character, or any downloaded script piped into a shell.
- The docs site serves a copy at https://moochy.dev/docs/skills. The relay embeds it from its pinned `oss/moochy-skills` submodule, so the copy changes only when a relay release moves that submodule.
- Check before you push: `python3 scripts/check-skills.py`. It checks the format and the A247 safety rules (ported from moochy-relay's `e2e/harness/skills.go`), and CI runs it on every push and pull request.

## License

Apache-2.0 ([LICENSE](https://github.com/moochy-dev/moochy-skills/blob/main/LICENSE)). Open-source client (Apache-2.0) · 100% free.
