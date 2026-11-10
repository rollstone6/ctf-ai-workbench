#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tool_root="${CTF_TOOLCHAIN_DIR:-/workspace/ctf-toolchain}"
check_dir=$(mktemp -d /tmp/ctf-reverse-check-XXXXXX)
trap 'rm -rf "$check_dir"' EXIT
cat > "$check_dir/fixture.c" <<'C'
#include <stdio.h>
int main(void) { puts("benign reverse fixture"); return 0; }
C
gcc -g -O0 -o "$check_dir/fixture" "$check_dir/fixture.c"
mkdir -p "$check_dir/projects" "$tool_root/home"
"$repo_root/bin/ghidra-headless" "$check_dir/projects" SelfTest \
 -import "$check_dir/fixture" -scriptPath "$repo_root/tools/environment/ghidra" \
 -postScript VerifyProject.java -analysisTimeoutPerFile 60 -max-cpu 2 -deleteProject \
 > "$check_dir/ghidra.log" 2>&1 || { tail -35 "$check_dir/ghidra.log"; exit 1; }
grep -q 'CTF_REVERSE_SELFTEST_OK' "$check_dir/ghidra.log" || { tail -35 "$check_dir/ghidra.log"; exit 1; }
echo 'Reverse 工具自检通过：编译良性 ELF、Ghidra 导入/分析、定位 main。'
