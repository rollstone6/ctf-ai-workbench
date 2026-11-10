#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
sage_image=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["sage_image"])' "$repo_root/config/toolchain-lock.json")
env -u DOCKER_HOST -u DOCKER_CONTEXT -u DOCKER_TLS -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH \
 docker --host=unix:///var/run/docker.sock run --rm --network=none --cpus=2 --memory=4g --entrypoint sage "$sage_image" \
 -c 'n=Integer(101*103); assert list(factor(n))==[(101,1),(103,1)]; R=PolynomialRing(GF(101),"x"); x=R.gen(); assert (x+1)*(x-1)==x^2-1; print("CTF_SAGE_SELFTEST_OK")'
