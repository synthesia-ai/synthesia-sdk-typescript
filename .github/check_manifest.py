"""Check the SDK's manifest against main.

  python3 .github/check_manifest.py

Runs on every pull request (.github/workflows/manifest.yml). A generator bump, a generator config change or a hand edit
can add a dependency, an install script, an entry point or a build-system change in a few lines of a large generated
pull request. This compares the manifest the pull request would merge with main's, ignoring the version, and fails on
any difference until a person other than the pull request's author adds the `dependencies-approved` label. A push
removes the label, so an approval covers only what the approver saw. The differences go to the run's summary, with new
dependencies called out: a new dependency shipped to customers needs a maintainer's review before the label goes on.

Ours, not Fern's: kept through .fernignore. Stdlib only.
"""

import difflib
import json
import os
import re
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

LABEL = "dependencies-approved"
# Manifests compared field by field, without the version, which changes on every regeneration.
PARSED = {
    "pyproject.toml": (tomllib.loads, [("project", "version"), ("tool", "poetry", "version")]),
    "package.json": (json.loads, [("version",)]),
}
# Compared as text (no YAML parser in the stdlib). It can allow dependencies' install scripts.
TEXT = ["pnpm-workspace.yaml"]


def main():
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    changes, shipped, dev = compare()
    if not changes:
        print("The manifest is unchanged from main.")
        return
    report = ["## Manifest changes against main", ""]
    if shipped:
        report += [f"**New dependencies shipped to customers (review before approving):** {', '.join(shipped)}", ""]
    if dev:
        report += [f"**New dev dependencies:** {', '.join(dev)}", ""]
    report += ["```diff", *changes, "```", ""]

    number = event["pull_request"]["number"]
    author = event["pull_request"]["user"]["login"]
    approval = None
    if event["action"] == "synchronize":
        remove_label(number)
    else:
        approval = approved_by(number, author)
    if approval:
        report.append(f"Approved with the `{LABEL}` label by @{approval}.")
    else:
        report.append(f"Review these changes, then add the `{LABEL}` label. It counts only when added by a person "
                      "other than the pull request's author, after the latest push.")
    print("\n".join(report))
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
        summary.write("\n".join(report) + "\n")
    if not approval:
        print(f"::error::The manifest changed; it needs the {LABEL} label")
        sys.exit(1)


def compare():
    """The changed fields as diff lines, and the new shipped and dev dependency names."""
    changes, shipped, dev = [], [], []
    for name, (parse, ignored) in PARSED.items():
        texts = on_main(name), Path(name).read_text() if Path(name).exists() else ""
        if not any(texts):  # Not this repo's manifest; a deleted one compares as all removed
            continue
        old, new = (flatten(drop(parse(text), ignored)) if text else {} for text in texts)
        for path in sorted(old.keys() | new.keys(), key=str):
            if old.get(path) != new.get(path):
                key = f"{name}: {'.'.join(path)}"
                changes += [f"- {key} = {json.dumps(old[path])}"] if path in old else []
                changes += [f"+ {key} = {json.dumps(new[path])}"] if path in new else []
        old_names = {dependency(path) for path in old} - {None}
        for added in sorted({dependency(path) for path in new} - old_names - {None}):
            (dev if added[0] else shipped).append(added[1])
    for name in TEXT:
        if Path(name).exists() or on_main(name):
            lines = difflib.unified_diff(on_main(name).splitlines(), Path(name).read_text().splitlines()
                                         if Path(name).exists() else [], f"main:{name}", name, lineterm="")
            changes += list(lines)
    return changes, shipped, dev


def on_main(name):
    """The file as main has it: the merge commit's first parent."""
    result = subprocess.run(["git", "show", f"HEAD^1:{name}"], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else ""


def drop(manifest, ignored):
    for path in ignored:
        table = manifest
        for key in path[:-1]:
            table = table.get(key, {})
        table.pop(path[-1], None)
    return manifest


def flatten(value, path=()):
    """{path tuple: leaf}. List items become keys, so an added or removed item shows on its own."""
    if isinstance(value, dict) and value:
        return {leaf: item for key, child in value.items() for leaf, item in flatten(child, path + (key,)).items()}
    if isinstance(value, list) and value:
        return {path + (json.dumps(item, sort_keys=True),): True for item in value}
    return {path: value}


def dependency(path):
    """(is dev, name) for a path inside a dependency table (Poetry, PEP 621 or npm), else None."""
    for i, key in enumerate(path[:-1]):
        if key.lower().endswith("dependencies"):
            item = path[i + 2] if key == "optional-dependencies" and len(path) > i + 2 else path[i + 1]
            name = re.split(r"[\s<>=!~;\[(]", item.strip('"'), maxsplit=1)[0] or item
            if name == "python":  # Poetry's interpreter constraint
                return None
            return ("group" in path[:i] or key == "devDependencies", name)
    return None


def approved_by(number, author):
    """Who added the label, if it's on and was added by a person other than the author."""
    if LABEL not in {label["name"] for label in api("GET", f"issues/{number}/labels")}:
        return None
    events, page = [], 1
    while batch := api("GET", f"issues/{number}/events?per_page=100&page={page}"):
        events += batch
        page += 1
    added = [e for e in events if e["event"] == "labeled" and e["label"]["name"] == LABEL]
    actor = added[-1]["actor"] if added else None
    if not actor or actor["login"] == author or actor["type"] != "User":
        return None
    return actor["login"]


def remove_label(number):
    try:
        api("DELETE", f"issues/{number}/labels/{LABEL}")
    except urllib.error.HTTPError as error:
        if error.code != 404:  # Not on the pull request
            raise


def api(method, path):
    url = f"{os.environ['GITHUB_API_URL']}/repos/{os.environ['GITHUB_REPOSITORY']}/{path}"
    headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github+json"}
    with urllib.request.urlopen(urllib.request.Request(url, method=method, headers=headers), timeout=30) as response:
        return json.load(response)


if __name__ == "__main__":
    main()
