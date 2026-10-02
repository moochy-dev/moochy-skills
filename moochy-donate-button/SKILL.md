---
name: moochy-donate-button
description: Add, fix, or check the Moochy "Donate tokens" button in a repository README so people can donate LLM tokens to the project. Use when the user asks for a Moochy button or badge, to accept token donations through moochy.dev, or to repair an existing Moochy button.
---

# Add the Moochy "Donate tokens" button

The button is a plain image link in the README. It needs no account, no key, and no token, and it changes nothing but the README. Full recipe: https://moochy.dev/docs/donate-button.md

## Rules

- Never put an API key, a token, or a password in the README, a URL, or a commit, and never ask the user for one: the button does not need any.
- Do not add tracking or `utm_*` parameters, redirects, scripts, or iframes. Unknown parameters break the image.
- Do not register (claim) the project or run any `moochy` command that signs something. Those need the maintainer's own owner key; tell them the command instead.
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
2. Search for `moochy.dev/p/`. If a Moochy button is already there, do not add another; replace it only if the user asked for a change.
3. If the README has a row of badges near the top, add the button at the end of that row in the same syntax. Otherwise add it on its own line right after the title, with a blank line before and after.
4. Do not reorder, reformat, or remove anything else.
5. Commit only the README: `docs: add a "Donate tokens" button (Moochy)`.

### 5. Check

`curl -s -o /dev/null -w '%{http_code}\n' "BUTTON_URL"` prints `200` when the button renders, `400` for a wrong option, `404` when the project is not registered.

## Not on Moochy yet

Give the user this message, with `PATH` from step 1:

> To accept token donations, sign in at https://moochy.dev/claim with the GitHub or GitLab account that administers `PATH`, register the repository, then confirm on your own machine: `moochy owner init` (once) and `moochy claim PATH`. Then the "Donate tokens" button can go in the README. Guide: https://moochy.dev/docs/maintainer
