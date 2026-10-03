#!/usr/bin/env python3
"""Checks every <skill>/SKILL.md: frontmatter with name (= folder) and description, under 500 lines."""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
problems = []
skills = sorted(root.glob("*/SKILL.md"))
for p in skills:
    text = p.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, flags=re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), flags=re.M)) if m else {}
    if meta.get("name") != p.parent.name:
        problems.append(f"{p.parent.name}: frontmatter name must be {p.parent.name!r}")
    if not meta.get("description"):
        problems.append(f"{p.parent.name}: frontmatter description is required")
    if text.count("\n") >= 500:
        problems.append(f"{p.parent.name}: SKILL.md must stay under 500 lines")
if not skills:
    problems.append("no */SKILL.md found")
print("\n".join(problems) or f"{len(skills)} skills ok")
sys.exit(1 if problems else 0)
