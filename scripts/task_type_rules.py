import re

RULES = [
    ("feature",  r"\b(feat|feature)\b"),
    ("bugfix",   r"\b(fix|bug)\b"),
    ("refactor", r"\b(refactor)\b"),
    ("docs",     r"\b(docs|doc|readme)\b"),
    ("test",     r"\b(test|tests)\b"),
    ("chore",    r"\b(chore)\b"),
    ("build",    r"\b(build)\b"),
    ("perf",     r"\b(perf|performance)\b"),
    ("style",    r"\b(style|format|lint)\b"),
    ("ci",       r"\b(ci)\b"),
    ("revert",   r"\b(revert)\b"),
]

def infer_task_type(title: str) -> str:
    if not isinstance(title, str) or not title.strip():
        return "unknown"
    t = title.lower()
    for label, pat in RULES:
        if re.search(pat, t):
            return label
    return "other"
