---
name: moochy-donate
description: Help a user donate LLM tokens to an open-source project with Moochy - install the app, add their provider key locally, set limits, donate, pause or stop, and see what their key was used for. Use when the user wants to donate tokens, support a project with their Anthropic, OpenAI, OpenRouter, DeepSeek, xAI key or local GPU, or manage their Moochy donations.
---

# Donate tokens with Moochy

The donor's machine runs the Moochy app. It receives encrypted requests from a project's members, checks them, and calls the donor's provider with the donor's key. The key never leaves the machine, nothing is paid in advance, and the donor sets the limits. Guide: https://moochy.dev/docs/donor.md

## Rules

- **The key stays with the user.** Never ask for the provider API key, never read it, print it, or put it in a file, a command line, or your reply. The user types it into `moochy keys add` themselves (it reads from standard input).
- **Donating is the user's decision.** Run `moochy donate` only when the user asked for that project and that monthly amount, and show them the command first. Never raise a limit on your own.
- **Do not weaken safety.** Do not use `moochy up --unsafe-no-lockdown`, and do not skip the safety step for the user (`--accept-safety` is their confirmation, not yours).
- **Do not install by piping a script into a shell.** Use a package manager or a release file the user can check.

## Steps

### 1. Install

```sh
brew install moochy-dev/tap/moochy        # macOS and Linux with Homebrew
```

Or download a release archive for the platform from the public `moochy-dev/moochy-cli` repository and check it (`gh attestation verify <file> --repo moochy-dev/moochy-cli`). Then `moochy --help`.

### 2. Sign in (the user does this)

```sh
moochy login --roles worker
```

It prints a short code and a link; the user confirms the code in their browser. Add `gateway` (`--roles gateway,worker`) only if they also want to use donated tokens from this machine.

### 3. Add the provider key (the user types it)

Recommend a **separate API key with a spending limit at the provider** (Anthropic workspace limit, OpenAI project spend limit, OpenRouter key credit limit, DeepSeek or xAI prepaid balance). Then the user runs, in their own terminal:

```sh
read -rs KEY && printf '%s' "$KEY" | moochy keys add anthropic --key-stdin && unset KEY
```

Providers: `anthropic`, `openai`, `openrouter`, `deepseek`, `xai`. For a model on their own GPU: `moochy keys add local --base-url http://127.0.0.1:11434 --model local/<id>=<server model>` (guide: https://moochy.dev/docs/local-gpu.md). `moochy keys list` shows the keys.

### 4. The safety step

Right after a key is added, the app asks for a **monthly limit for this machine** and a confirmation about the provider-side limit. If the user prefers to set it in one line:

```sh
moochy safety --monthly-limit '$25' --accept-safety
```

The machine does not donate until this is done. The most they can spend is the smallest of: each donation's monthly limit, this machine's limit, and the provider's spending limit.

### 5. Start the app

```sh
moochy up
moochy service install      # start at login (optional)
moochy status
moochy doctor               # if something looks wrong
```

### 6. Donate

```sh
moochy donate --repo owner/name --cap '$20'      # up to $20 a month; asks for confirmation
```

Quote the amount so the shell keeps the `$`. The donation starts when the project's maintainer accepts it. Models, maximum effort, schedule, and visibility are set on the project's page on moochy.dev.

### 7. Pause, stop, and check

```sh
moochy donations                       # each donation, what it used this month, and its id
moochy donations pause <id>            # or resume <id>
moochy donations stop <id>             # ends the donation
moochy pause                           # stop serving from this machine at once (moochy resume to undo)
moochy journal                         # what the key was used for: project, model, tokens, cost
```

Stopping is immediate: nothing was transferred, so nothing needs to be returned.
