#!/usr/bin/env python3
"""Run every inline Python snippet in chapters/*.md and report the ones that raise.

Full scripts (blocks starting with "# name.py") are tested by scripts/test_examples.sh.
Usage: python3 scripts/check_snippets.py
"""
import contextlib, glob, io, json, os, re, sys, tempfile

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
os.chdir(tempfile.mkdtemp())
open("hosts.csv", "w").write("hostname,ip,role\nweb-01,10.0.0.10,web\nweb-02,10.0.0.11,web\ndb-01,10.0.0.20,\"database, primary\"\n")
json.dump({"hosts": []}, open("inventory.json", "w"))
fails = 0
for fn in sorted(glob.glob(os.path.join(root, "chapters", "*.md"))):
    ns = {"__name__": "snippet"}
    for i, block in enumerate(re.findall(r"```python\n(.*?)```", open(fn).read(), re.S)):
        if re.match(r"(?:#!.*\n)?# [\w.]+\.py\n", block):
            continue  # full script, run by test_examples.sh
        if ">>>" in block:
            code, cur = [], None
            for line in block.splitlines():
                if line.startswith(">>> "):
                    if cur is not None: code.append(cur)
                    cur = line[4:]
                elif line.startswith("..."):
                    cur += "\n" + line[4:]
            if cur is not None: code.append(cur)
            stmts = code
        else:
            stmts = [block]
        for st in stmts:
            out = io.StringIO()
            try:
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                    try:
                        exec(compile(st, "<snippet>", "single" if ">>>" in block and "\n" not in st.strip() else "exec"), ns)
                    except SystemExit as e:
                        print(f"(SystemExit: {e})")
            except Exception as e:
                fails += 1
                print(f"FAIL {os.path.basename(fn)} block {i}: {st.strip().splitlines()[0][:70]!r}\n     -> {type(e).__name__}: {e}")
print(f"\nsnippet failures: {fails}")

sys.exit(1 if fails else 0)
