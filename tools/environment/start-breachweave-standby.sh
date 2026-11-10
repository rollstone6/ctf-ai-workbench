#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tool_root="${CTF_TOOLCHAIN_DIR:-/workspace/ctf-toolchain}"
export PATH="$tool_root/bun-linux-x64:$PATH"
export BUN_INSTALL_CACHE_DIR="$tool_root/bun-cache"
unset DOCKER_HOST DOCKER_CONTEXT DOCKER_TLS DOCKER_TLS_VERIFY DOCKER_CERT_PATH
# The upstream app uses ~/.tch-agent. Keep its data under the writable workspace.
python3 - "$tool_root" <<'PY'
import json,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
state=root/'state/breachweave';state.mkdir(parents=True,exist_ok=True)
home=Path.home()/'.tch-agent'
if not home.exists() and not home.is_symlink():
    home.symlink_to(state,target_is_directory=True)
if home.resolve()!=state:
    raise SystemExit('Existing ~/.tch-agent belongs to another deployment; preserved')
p=state/'config/settings.json';p.parent.mkdir(parents=True,exist_ok=True)
data=json.loads(p.read_text()) if p.exists() else {}
runtime=data.setdefault('tch',{}).setdefault('runtime',{})
runtime.update(image='ctf-workbench-breachweave-standby:phase5',maxSolvers=0,networkMode='bridge')
p.write_text(json.dumps(data,indent=2)+'\n')
PY
env -u DOCKER_HOST -u DOCKER_CONTEXT -u DOCKER_TLS -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH \
 docker --host=unix:///var/run/docker.sock build --network=none \
 -t ctf-workbench-breachweave-standby:phase5 \
 -f "$repo_root/tools/environment/Dockerfile.breachweave-standby" "$repo_root/tools/environment"
cd "$tool_root/frameworks/BreachWeave"
exec bun apps/cli/src/main.ts web --listen 127.0.0.1:18765
