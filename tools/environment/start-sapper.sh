#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"
"$repo_root/bin/sapper" setup --goal "维护 CTF AI 工作台的解题记录与任务状态"
"$repo_root/bin/sapper" validate
exec "$repo_root/bin/sapper" view --serve --host 127.0.0.1 --port "${SAPPER_VIEW_PORT:-8765}"
