---
name: moochy-donate
description: Help a user donate LLM tokens to an open-source project, a whole GitHub organisation or GitLab group, or a maintainer (sponsor a person) with Moochy - install the app, add their provider key locally, set limits, donate, pause or stop, and see what their key was used for. Use when the user wants to donate tokens, support a project with their Anthropic, OpenAI, OpenRouter, DeepSeek, xAI key or local GPU, or manage their Moochy donations.
---

# Donate tokens with Moochy

The donor's machine runs the Moochy app. It receives encrypted requests from a project's members, checks them, and calls the donor's provider with the donor's key. Your API keys stay on your machine. Moochy never stores your API keys online. They stay in your machine's keychain, used only by the Moochy app on that machine, and are never sent to Moochy's servers, not even encrypted. Nothing is paid in advance, and the donor sets the limits. Guide: https://moochy.dev/docs/donor.md

## Rules

- **The key stays with the user.** Never ask for the provider API key, never read it, print it, or put it in a file, a command line, or your reply. The user types it into `moochy keys add` themselves (it reads from standard input).
- **Donating is the user's decision.** Run `moochy donate` only when the user asked for that project (or organisation, or person) and that monthly amount, and show them the command first. Never raise a limit on your own.
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

To an organisation (a GitHub organisation or a GitLab group, with every project its owner chose):

```sh
moochy donate --org github/acme --cap '$20'              # or --org gitlab/group/subgroup
```

- Always write the code host in `--org` (`github/…`, `gitlab/…`). `--repo acme/api` is the single project, never the organisation; do not guess one from the other: ask the user.
- Check first that the organisation is on Moochy and which projects it funds: `curl -fsS https://moochy.dev/api/v1/orgs/github/acme` (a `404` means it is not). Its page is `https://moochy.dev/org/github/acme`.
- The monthly limit is shared by all the organisation's projects together, not per project. The owner accepts the user once for the whole organisation. What each project used is on the donation's page on moochy.dev (Dashboard → the donation). Guide: https://moochy.dev/docs/donate-to-an-organisation.md

To sponsor a person (a GitHub or GitLab user who maintains open source; it pays for **their own** requests on the public repos they maintain):

```sh
moochy donate --person github/alice --cap '$20'          # or --person gitlab/USERNAME
```

- `--person` always names the code host. Never turn a project (`--repo`) or an organisation (`--org`) into a person, or the reverse: ask the user.
- `moochy person list --person github/alice` shows the repos it would serve; the page is `https://moochy.dev/people/github/alice`. An unclaimed profile can still be sponsored: the sponsorship waits.
- The person accepts the user once. Sponsoring yourself is refused (`self_donation`). Guide: https://moochy.dev/docs/sponsor-a-person.md

### 7. Pause, stop, and check

```sh
moochy donations                       # each donation (organisations and people included), what it used this month, and its id
moochy donations pause <id>            # or resume <id>
moochy donations stop <id>             # ends the donation
moochy pause                           # stop serving from this machine at once (moochy resume to undo)
moochy journal                         # what the key was used for: project, model, tokens, cost
```

Stopping is immediate: nothing was transferred, so nothing needs to be returned.
