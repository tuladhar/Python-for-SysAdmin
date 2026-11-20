#!/usr/bin/env bash
# Run every script in examples/ the way a reader would, and check its exit code.
# Usage: scripts/test_examples.sh        (from anywhere inside the repo)
set -u
cd "$(dirname "$0")/../examples"
E=$PWD
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
pass=0
fail=0

# expect RC COMMAND...   runs COMMAND in a scratch dir and checks its exit code
expect() {
  local want=$1; shift
  local out rc
  out=$(cd "$T" && timeout 30 "$@" 2>&1 < /dev/null); rc=$?
  if [ "$rc" -eq "$want" ]; then
    pass=$((pass + 1)); echo "ok   rc=$rc  $*"
  else
    fail=$((fail + 1)); echo "FAIL rc=$rc (want $want)  $*"; echo "$out" | head -15 | sed 's/^/     | /'
  fi
}

echo "python: $(python3 --version)"
for f in *.py ../*.py; do python3 -m py_compile "$f" || fail=$((fail + 1)); done

expect 0 bash -c "printf 'alice\nline1\nline2\n' | python3 '$E/stdio.py'"
expect 0 bash -c "echo hello sysadmin | python3 '$E/upper.py'"
expect 0 python3 "$E/working_with_files_01.py"
expect 0 bash -c "cat /etc/passwd | python3 '$E/line_count.py'"
expect 0 python3 "$E/line_count.py" /etc/services /etc/passwd /etc/hosts
expect 0 python3 "$E/argv_01.py" 1 2 3
expect 1 python3 "$E/argv_02.py" 1
expect 0 python3 "$E/argv_02.py" 1 2
expect 0 bash -c "cat /etc/passwd | python3 '$E/grep.py' root"
expect 1 python3 "$E/grep.py"
expect 0 python3 "$E/filesizes.py" /etc
expect 0 python3 "$E/sys_01.py"
expect 0 python3 "$E/disk_alert.py" /
mkdir -p "$T/bk"; touch -d '10 days ago' "$T/bk/old.tar.gz"; touch "$T/bk/new.tar.gz"
expect 0 python3 "$E/prune_backups.py" bk
if [ -e "$T/bk/old.tar.gz" ] || [ ! -e "$T/bk/new.tar.gz" ]; then fail=$((fail + 1)); echo "FAIL prune_backups.py deleted the wrong files"; fi
expect 1 python3 "$E/check_call.py"
expect 0 python3 "$E/capture_output.py"
expect 0 python3 "$E/app.py" 1 2 3 4 --sum
expect 2 python3 "$E/app.py" one
expect 0 python3 "$E/tcp_port_checker.py" github.com -p 443 -t 3
expect 1 python3 "$E/tcp_port_checker.py" github.com -p 443 8080 -t 2
expect 0 python3 "$E/github_stars.py"
expect 0 python3 "$E/users_to_csv.py"
expect 0 python3 "$E/backup_log.py" /srv/data ok
expect 0 python3 "$E/backup_log.py" /srv/x fail
expect 0 python3 "$E/port_check.py"
expect 0 python3 "$E/sweep.py" 127.0.0.1/32 1
expect 1 python3 "$E/sweep.py"
expect 0 python3 "$E/nested_sequences_flattened.py"
expect 0 python3 "$E/Monitoring Disk Space and Sending Alerts.py"
expect 0 python3 "$E/Automating_System_Tasks_with_subprocess.py"
expect 0 python3 "$E/Multi-threading.py"
expect 0 python3 "$E/../Network_Monitoring_and_Utilities.py"
if command -v ping > /dev/null; then expect 0 python3 "$E/follow.py"; fi
if docker info > /dev/null 2>&1; then expect 0 python3 "$E/stopped_containers.py"; else echo "skip stopped_containers.py (no docker)"; fi

echo
echo "passed: $pass  failed: $fail"
[ "$fail" -eq 0 ]
