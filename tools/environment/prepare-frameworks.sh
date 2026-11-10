#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tool_root="${CTF_TOOLCHAIN_DIR:-/workspace/ctf-toolchain}"
mkdir -p "$tool_root/frameworks"
export DSH_HOME="${DSH_HOME:-$tool_root/state/dsh}"
if [ ! -x "$tool_root/frameworks/dsh/node_modules/.bin/dsh" ]; then
  mkdir -p "$tool_root/frameworks/dsh"
  cp "$repo_root/config/frameworks/dsh/package.json" "$repo_root/config/frameworks/dsh/package-lock.json" "$tool_root/frameworks/dsh/"
  npm ci --prefix "$tool_root/frameworks/dsh" --cache "$tool_root/npm-cache" --ignore-scripts --no-audit --no-fund
fi
raw_dsh="$tool_root/frameworks/dsh/node_modules/.bin/dsh"
"$raw_dsh" --version
if [ ! -d "$DSH_HOME/profiles/ctf-skills" ]; then
  "$raw_dsh" --profile ctf-skills --from-default-profile web --dump-default-config >/dev/null
fi
"$repo_root/bin/dsh" --dump-config >/dev/null
breach="$tool_root/frameworks/BreachWeave"
if [ ! -e "$breach" ]; then
  git clone --branch pentest --single-branch https://github.com/m-sec-org/BreachWeave.git "$breach"
  git -C "$breach" checkout --detach 6957a55f15e0d585f4b728c831021a34f7e02891
fi
if [ "$(git -C "$breach" rev-parse HEAD)" != 6957a55f15e0d585f4b728c831021a34f7e02891 ]; then
  echo 'BreachWeave checkout differs from pinned commit; preserved without reset' >&2
  exit 1
fi
export PATH="$tool_root/bun-linux-x64:$PATH"
export BUN_INSTALL_CACHE_DIR="$tool_root/bun-cache"
(cd "$breach" && TCH_AGENT_SKIP_INSTALL_SCRIPT=1 bun install --frozen-lockfile --ignore-scripts)
if [ ! -f "$breach/node_modules/cpu-features/build/Release/cpufeatures.node" ]; then
  npm_config_devdir="$tool_root/node-gyp" npm --cache "$tool_root/npm-cache" rebuild --prefix "$breach/node_modules/cpu-features"
fi
(cd "$breach" && bun apps/cli/src/main.ts --help)
echo '框架依赖与 CLI 就绪；模型、接管收益和完整 Solver 执行尚需独立验证。'
