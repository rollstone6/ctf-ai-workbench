"""Install pinned, checksum-verified local tools without modifying system Java."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import urllib.request
import zipfile

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--with-sage', action='store_true')
parser.add_argument('--with-bun', action='store_true')
args = parser.parse_args()
tools = Path(os.environ.get('CTF_TOOLCHAIN_DIR','/workspace/ctf-toolchain')).resolve()
(tools/'downloads').mkdir(parents=True,exist_ok=True)
lock = json.loads((root/'config/toolchain-lock.json').read_text())

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def archive(spec, name, expected_dir):
    path=tools/'downloads'/name
    if not path.exists():
        temporary=path.with_suffix(path.suffix+'.partial')
        with urllib.request.urlopen(spec['url'],timeout=60) as source, temporary.open('wb') as target:
            shutil.copyfileobj(source,target)
        if digest(temporary)!=spec['sha256']:
            raise SystemExit(f'Checksum mismatch: {temporary}')
        temporary.replace(path)
    if digest(path)!=spec['sha256']:
        raise SystemExit(f'Checksum mismatch: {path}; file preserved for diagnosis')
    if not (tools/expected_dir).exists():
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as z:
                for item in z.infolist():
                    if not (tools/item.filename).resolve().is_relative_to(tools):
                        raise SystemExit('Archive path escapes tool directory')
                z.extractall(tools)
                for item in z.infolist():
                    mode=(item.external_attr>>16)&0o777
                    if mode: (tools/item.filename).chmod(mode)
        else:
            with tarfile.open(path) as t: t.extractall(tools,filter='data')
    print(f'校验通过：{name}')

uv=shutil.which('uv')
if not uv: raise SystemExit('uv is required; use the managed environment runtime')
python=tools/'venv/bin/python'
if not python.exists():
    subprocess.run([uv,'--cache-dir',str(tools/'uv-cache'),'venv',str(tools/'venv'),'--python','python3'],check=True)
subprocess.run([uv,'--cache-dir',str(tools/'uv-cache'),'pip','sync','--python',str(python),str(root/'tools/environment/requirements-toolchain.txt')],check=True)
archive(lock['ghidra'],'ghidra_12.2_PUBLIC_20261016.zip','ghidra_12.2_PUBLIC')
archive(lock['jdk'],'temurin25.tar.gz','jdk-25.0.5+8')
if args.with_bun:
    archive(lock['bun'],'bun-linux-x64.zip','bun-linux-x64')
    (tools/'bun-linux-x64/bun').chmod(0o755)
if args.with_sage:
    env=os.environ.copy()
    for key in ('DOCKER_HOST','DOCKER_CONTEXT','DOCKER_TLS','DOCKER_TLS_VERIFY','DOCKER_CERT_PATH'):env.pop(key,None)
    subprocess.run(['docker','--host=unix:///var/run/docker.sock','pull',lock['sage_image']],env=env,check=True)
print('本地工具安装完成；系统 Chromium、gcc 与 Docker daemon 仍需可用。')
