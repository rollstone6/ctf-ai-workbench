"""Stage 1: exercise the managed Docker daemon and shared challenge storage."""
from pathlib import Path
import base64
import json
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
shared = Path(os.environ.get('CTF_CHALLENGES_DIR', '/workspace/ctf-challenges')).resolve()
for name in ('inbox', 'work', 'evidence'):
    (shared / name).mkdir(parents=True, exist_ok=True)
assert shutil.which('codex'), 'Codex CLI missing'
subprocess.run(['codex', '--version'], check=True)
subprocess.run(['python3', '--version'], check=True)
env = os.environ.copy()
for name in ('DOCKER_HOST','DOCKER_CONTEXT','DOCKER_TLS','DOCKER_TLS_VERIFY','DOCKER_CERT_PATH'):
    env.pop(name, None)
docker = ['docker', '--host=unix:///var/run/docker.sock']
subprocess.run(docker + ['info', '--format', '{{.ServerVersion}}'], env=env, check=True)
image = json.loads((ROOT/'config/toolchain-lock.json').read_text())['python_image']
# No real challenge or credentials are passed into this self-test.
with tempfile.TemporaryDirectory(prefix='minimal-', dir=shared/'work') as temporary:
    directory = Path(temporary)
    (directory/'input.json').write_text(json.dumps({'encoded':base64.b64encode(b'flag{shared_dir_ok}').decode()}))
    code = "import pathlib,json,base64; p=pathlib.Path('/challenges'); x=json.loads((p/'input.json').read_text()); result=base64.b64decode(x['encoded']).decode(); assert result=='flag{shared_dir_ok}'; (p/'result.json').write_text(json.dumps({'verified':True,'result':result}))"
    subprocess.run(docker + ['run','--rm','--user',f'{os.getuid()}:{os.getgid()}','--network=none','--cpus=1','--memory=512m','--cap-drop=ALL','--security-opt=no-new-privileges','--mount',f'type=bind,src={directory},dst=/challenges',image,'python','-c',code], env=env, check=True)
    result = json.loads((directory/'result.json').read_text())
    assert result == {'verified':True,'result':'flag{shared_dir_ok}'}
    (shared/'evidence/minimal-selftest.json').write_text(json.dumps(result, indent=2)+'\n')
print('第一阶段通过：Codex CLI、Python、Docker、共享题目目录及容器证据回读。未验证独立 Codex CLI 的真实模型调用。')
