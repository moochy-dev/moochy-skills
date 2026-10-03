---
name: moochy-donate-button
description: Add, fix, or check the Moochy "Donate tokens" button or the live showcase chart (tokens donated and used) in a repository README, in a GitHub organisation's or GitLab group's profile README, or in a maintainer's personal profile README, so people can donate LLM tokens to the project, the organisation, or the person. Use when the user asks for a Moochy button, badge, or chart, to accept token donations through moochy.dev, or to repair an existing Moochy button.
---

# Add the Moochy "Donate tokens" button

The button is a plain image link in the README. It needs no account, no key, and no token, and it changes nothing but the README. Full recipe: https://moochy.dev/docs/donate-button.md

## Rules

- Never put an API key, a token, or a password in the README, a URL, or a commit, and never ask the user for one: the button does not need any.
- Do not add tracking or `utm_*` parameters, redirects, scripts, or iframes. Unknown parameters break the image.
- Do not register (claim) the project or the organisation, or run any `moochy` command that signs something. Those need the maintainer's own owner key; tell them the command instead.
- Change only the README.

## Steps

### 1. Find the provider and path

If the Moochy app is installed, `moochy button` reads the git remote (offline) and prints the snippet; skip to step 3 with its output, after checking step 2. Otherwise:

```sh
url=$(git remote get-url origin)
host=$(printf '%s\n' "$url" | sed -E 's#^[a-z+]+://##; s#^[^@/]*@##; s#[:/].*$##')
path=$(printf '%s\n' "$url" | sed -E 's#^[a-z+]+://##; s#^[^@/]*@##; s#^[^:/]+(:[0-9]+)?[:/]##; s#/+$##; s#\.git$##')
case "$host" in github.com) provider=github ;; gitlab.com) provider=gitlab ;; *) provider= ;; esac
echo "$provider $path"
```

- `github` paths are `owner/name`; `gitlab` paths keep every group and subgroup (`group/subgroup/project`).
- Stop and ask the user when `provider` is empty (only public github.com and gitlab.com repositories can receive donations), or when there is no `origin` remote.
- Never print or store the remote URL itself: it can contain a token.

### 2. Check that the project is on Moochy

```sh
curl -fsS "https://moochy.dev/api/v1/projects/$provider/$path"
```

The answer is `{"claimed": …, "donate_url": …, "button_url": …, "docs": …}`, public, with no donor or amount.

- `"claimed": true`: use `button_url` and `donate_url` **exactly as returned**.
- `"claimed": false`: do not add the button (it would show "project not found"). Tell the user what is in "Not on Moochy yet" below.
- `404`: the provider or path is wrong; go back to step 1.

Address rules, for checking what you got:

| Project | Image | Link |
|---|---|---|
| GitHub | `https://moochy.dev/p/github/OWNER/NAME/button.svg` | `https://moochy.dev/p/github/OWNER/NAME/donate` |
| GitHub, short form (also valid, forever) | `https://moochy.dev/p/OWNER/NAME/button.svg` | `https://moochy.dev/p/OWNER/NAME/donate` |
| GitLab, with groups and subgroups | `https://moochy.dev/p/gitlab/GROUP/SUBGROUP/NAME/-/button.svg` | `https://moochy.dev/p/gitlab/GROUP/SUBGROUP/NAME/-/donate` |

On GitLab the action always comes after `/-/`, so a nested group path is never mistaken for an action.

### 3. Pick the snippet

Default button (mascot and text, light, medium), Markdown:

```markdown
[![Donate tokens](BUTTON_URL)](DONATE_URL)
```

Light and dark, following the reader's GitHub theme (HTML in `README.md`):

```html
<a href="DONATE_URL">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="BUTTON_URL?theme=dark">
    <img alt="Donate tokens" height="36" src="BUTTON_URL">
  </picture>
</a>
```

reStructuredText (`README.rst`):

```rst
.. image:: BUTTON_URL
   :target: DONATE_URL
   :alt: Donate tokens
```

Options, added to `BUTTON_URL` as a query string (any other key, a repeated key, or a value not listed makes the server answer 400):

| Key | Values | Default |
|---|---|---|
| `label` | 1–32 characters: letters, digits, spaces, `. , : ; ! ? ' ’ & + - ( ) / # @` | `Donate tokens` |
| `style` | `mascot`, `text`, `compact` | `mascot` |
| `theme` | `light`, `dark`, `auto` | `light` |
| `size` | `s` (28 px), `m` (36 px), `l` (44 px) | `m` |

Match `height` in HTML to the size. Keep `alt="Donate tokens"` (or the label).

### 4. Put it in the README

1. Use `README.md`, `README.rst`, or `README` at the repository root, in that order. If none exists, ask before creating one.
2. Search for `moochy.dev/p/`, `moochy.dev/org/` and `moochy.dev/people/`. If a Moochy button is already there, do not add another; replace it only if the user asked for a change.
3. If the README has a row of badges near the top, add the button at the end of that row in the same syntax. Otherwise add it on its own line right after the title, with a blank line before and after.
4. Do not reorder, reformat, or remove anything else.
5. Commit only the README: `docs: add a "Donate tokens" button (Moochy)`.

### 5. Check

`curl -s -o /dev/null -w '%{http_code}\n' "BUTTON_URL"` prints `200` when the image renders and `400` for a wrong option. A project that is not registered also gets `200`, with a "project not found" badge, so check registration with the projects API (step 1).

## Organisations (profile READMEs)

A GitHub organisation or GitLab group claimed on Moochy has its own button; a donation to it serves every project its owner chose. Use it in the organisation's profile README, or in a project README only when the user asks for the organisation's button. Personal accounts are not organisations: see People below.

| Where | Profile README file |
|---|---|
| GitHub organisation `ORG` | `profile/README.md` in the `ORG/.github` repository |
| GitLab group `GROUP` | `README.md` in the `GROUP/gitlab-profile` project |

In the `.github` or `gitlab-profile` checkout, the organisation is the remote path without its last segment (`acme/.github` → `github/acme`; `group/sub/gitlab-profile` → `gitlab/group/sub`). Check it and get the addresses:

```sh
curl -fsS "https://moochy.dev/api/v1/orgs/github/acme"            # or .../orgs/gitlab/group/sub
```

The answer is `{"org_id": …, "path": …, "claimed": true, "repos": […], "donate_url": …, "button_url": …}`, public, with no donor or amount. Use `button_url` and `donate_url` exactly as returned. A `404` means the organisation is not on Moochy: do not add the button; give the user the organisation message below.

| Organisation | Image | Link |
|---|---|---|
| GitHub | `https://moochy.dev/org/github/ORG/button.svg` | `https://moochy.dev/org/github/ORG/donate` |
| GitLab, group or subgroup | `https://moochy.dev/org/gitlab/GROUP/SUB/-/button.svg` | `https://moochy.dev/org/gitlab/GROUP/SUB/-/donate` |

Snippets, options, placement and the check are those of steps 3 to 5. Example:

```markdown
[![Donate tokens](https://moochy.dev/org/github/acme/button.svg)](https://moochy.dev/org/github/acme/donate)
```

`moochy button` prints project buttons only (`moochy button --chart --org …` prints the organisation's chart). Commit message: `docs: add a "Donate tokens" button for the organisation (Moochy)`.

## People (personal profile READMEs)

A maintainer who claimed their own GitHub or GitLab profile on Moochy can be sponsored: sponsors' tokens pay for that person's own requests on the public repos they maintain. Their personal profile README is `README.md` in the repository named like the user (`LOGIN/LOGIN` on GitHub; `USERNAME/USERNAME` on GitLab), so the person is `github/LOGIN` or `gitlab/USERNAME`. Check it and get the addresses:

```sh
curl -fsS "https://moochy.dev/api/v1/people/github/LOGIN"          # or .../people/gitlab/USERNAME
```

Same shape as the organisations API. Use `button_url` and `donate_url` exactly as returned (images `https://moochy.dev/people/github/LOGIN/button.svg`, GitLab `https://moochy.dev/people/gitlab/USERNAME/-/button.svg`). A `404` means the person has not claimed their profile: do not add the button; tell the user to sign in on moochy.dev, choose Claim your profile, then run `moochy claim --person` on their own machine (guide: https://moochy.dev/docs/sponsor-a-person). Snippets, options, placement and the check are those of steps 3 to 5.

## Showcase chart

A live chart of the tokens donated to and used by a project, an organisation, or a person, as an image for READMEs (`chart.svg`) or a card for websites (`card`, in an `<iframe>`; never in a README). Add it only when the user asks for a chart; put it below the button, never instead of it. Only for targets the checks above found on Moochy (otherwise the server answers `404` with a "not on moochy" image).

If the Moochy app is installed, `moochy button --chart` prints the snippet (offline; it reads the git remote like `moochy button`; `--org ORG` or `--person PERSON` for the others; `--format markdown|html|rst|iframe`). Otherwise build it:

| Target | Image | Link |
|---|---|---|
| GitHub project | `https://moochy.dev/p/github/OWNER/NAME/chart.svg` | `https://moochy.dev/p/github/OWNER/NAME` |
| GitLab project | `https://moochy.dev/p/gitlab/GROUP/SUB/NAME/-/chart.svg` | `https://moochy.dev/p/gitlab/GROUP/SUB/NAME` |
| Organisation | `https://moochy.dev/org/github/ORG/chart.svg` (GitLab: `…/org/gitlab/GROUP/-/chart.svg`) | `https://moochy.dev/org/github/ORG` |
| Person | `https://moochy.dev/people/github/LOGIN/chart.svg` (GitLab: `…/people/gitlab/USERNAME/-/chart.svg`) | `https://moochy.dev/people/github/LOGIN` |

The card is the same address with `card` instead of `chart.svg`. Options (strict, like the button; 400 otherwise):

| Key | Values | Default |
|---|---|---|
| `metric` | `tokens`, `dollars` | `tokens` |
| `series` | `both`, `donated`, `used` | `both` |
| `kind` | `area`, `bars`, `line`, `sparkline` | `area` |
| `period` | `7d`, `30d`, `90d`, `12m` | `30d` |
| `theme` | `light`, `dark`, `auto` | `light` |
| `size` | `s` (320 px wide), `m` (480), `l` (640) | `m` |
| `label` | 1–40 characters: letters, digits, spaces, `. , : ; ! ? ' ’ & + - ( ) / # @` | the target's name |
| `goal` | `1`: the monthly goal line (with `metric=dollars`) | off |
| `total` | `1`: a headline total | off |

```markdown
[![Tokens donated and used on Moochy](https://moochy.dev/p/github/tinyhttp/arrow/chart.svg)](https://moochy.dev/p/github/tinyhttp/arrow)
```

For light and dark, use the `<picture>` form of step 3 with `chart.svg?theme=dark` in the `<source>`. Every option and snippet: https://moochy.dev/docs/donate-button.md (section "Showcase charts")

## Not on Moochy yet

Give the user this message, with `PATH` from step 1:

> To accept token donations, sign in at https://moochy.dev/claim with the GitHub or GitLab account that administers `PATH`, register the repository, then confirm on your own machine: `moochy owner init` (once) and `moochy claim PATH`. Then the "Donate tokens" button can go in the README. Guide: https://moochy.dev/docs/maintainer

For an organisation, with `ORG` as `github/acme` or `gitlab/group/sub`:

> To accept token donations for the whole organisation, sign in at https://moochy.dev/claim with an account that owns `ORG` (GitHub: an organisation admin; GitLab: a group Owner) and choose Organisation, then confirm on your own machine: `moochy claim --org ORG`, and add the projects it funds with `moochy org add PROJECT --org ORG`. Guide: https://moochy.dev/docs/organisations
