"""Fails if a tracked file mentions something internal to Synthesia.

Ours, not Fern's (all of .github/ is in .fernignore). CI's secrets job runs it on every tracked file; the pre-commit
hook runs it on the files being committed. It prints only the file, the line and the pattern's name, never the text
that matched: CI logs are public once the repository is.

Usage: python3 .github/check_internal_refs.py [FILE ...]   (no files: every file `git ls-files` lists)
"""

import re
import subprocess
import sys

# The patterns are written so that none of them matches its own source text, so this file is checked like any other.
PATTERNS = [
    ("internal GitHub org", re.compile(r"synthesia-technolog(?:ies)", re.I)),
    ("AppSec threat-model id", re.compile(r"\bT[M]-[0-9]+\b")),
    ("ticket id", re.compile(r"\b([A-Z][A-Z\d]{1,9})-\d+\b")),
    ("Linear URL", re.compile(r"linear\.app", re.I)),
    ("Slack URL", re.compile(r"slack\.com", re.I)),
    ("Notion URL", re.compile(r"notion\.(?:so|site|com)\b", re.I)),
    ("internal dev host", re.compile(r"\.dev\.synthesia\.io", re.I)),
    ("staging host", re.compile(r"\bstaging\.[a-z0-9]", re.I)),
    ("internal email address", re.compile(r"([a-z0-9._%+-]+)@synthesia\.io\b", re.I)),
    ("non-GitHub-hosted runner", re.compile(r"self-host(?:ed)", re.I)),
    ("ECR registry host", re.compile(r"\.dkr\.ecr\.", re.I)),
]

# Uppercase-hyphen-number words that aren't ticket ids. Add a prefix here for a reviewed false positive.
NOT_TICKETS = {"TM", "UTF", "ISO", "SHA", "RFC", "CVE", "CWE", "GHSA", "PEP", "ECMA"}
# The one public address: SECURITY.md sends vulnerability reports there.
PUBLIC_ADDRESSES = {"security-reports"}


def allowed(name, match):
    if name == "ticket id":
        return match.group(1) in NOT_TICKETS
    if name == "internal email address":
        return match.group(1).lower() in PUBLIC_ADDRESSES
    return False


def main():
    paths = sys.argv[1:] or subprocess.run(
        ["git", "ls-files", "-z"], check=True, capture_output=True, text=True
    ).stdout.split("\0")
    hits = 0
    for path in filter(None, paths):
        try:
            with open(path, "rb") as f:
                data = f.read()
        except (FileNotFoundError, IsADirectoryError):  # A deleted file or a submodule
            continue
        if b"\0" in data:  # Binary
            continue
        for number, line in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
            for name, pattern in PATTERNS:
                if any(not allowed(name, m) for m in pattern.finditer(line)):
                    print(f"{path}:{number}: {name}")
                    hits += 1
    if hits:
        print(f"{hits} internal reference(s) found. Remove them; see .github/check_internal_refs.py.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
