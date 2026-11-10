#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"
python3 -B - <<'PY'
from pathlib import Path
root=Path.cwd()
links=list((root/'.agents/skills').iterdir())
assert len(links)==15, 'Expected 15 installed skills'
for link in links:
    assert link.resolve().is_relative_to(root), link
    assert (link/'SKILL.md').is_file(), link
print('15 repository-local skills validated')
PY
"$repo_root/bin/sapper" --version
python3 -B "$repo_root/tools/environment/smoke.py"
for target in test_skill_frontmatter.py test_cross_references.py test_skill_discoverability.py; do
  (cd vendor/ctf-skills && python3 -B -m unittest discover -s tests -p "$target")
done
(cd vendor/sapper-v2 && python3 -B -m unittest discover -s tests)
python3 -B -m unittest discover -s tools/environment -p test_localization.py
