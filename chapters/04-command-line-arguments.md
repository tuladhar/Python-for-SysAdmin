# Command-line Arguments

A script becomes a tool when it accepts arguments. The simplest way to read them is `sys.argv`, a list of strings passed to your script.

> `sys.argv[0]` is always the name of the script itself. The real arguments start at `sys.argv[1]`.

```python
#!/usr/bin/env python3
# argv_01.py
import sys

print("sys.argv:", sys.argv)
print("length:", len(sys.argv))
```

```bash
$ python3 argv_01.py --help
sys.argv: ['argv_01.py', '--help']
length: 2
$ python3 argv_01.py 1 2 3
sys.argv: ['argv_01.py', '1', '2', '3']
length: 4
```

## Require an exact number of arguments

`sys.exit("message")` prints the message to `stderr` and exits with status `1`, which is exactly what you want for a usage error.

```python
#!/usr/bin/env python3
# argv_02.py
import sys

args = sys.argv[1:]  # drop the script name

if len(args) != 2:
    sys.exit(f"invalid number of arguments (expected 2, given: {len(args)})")

print("two arguments are:", args)
```

```bash
$ python3 argv_02.py 1
invalid number of arguments (expected 2, given: 1)
$ echo $?
1
$ python3 argv_02.py 1 2
two arguments are: ['1', '2']
```

## Example: a tiny `grep`

```python
#!/usr/bin/env python3
# grep.py
import sys


def main(argv):
    if len(argv) != 1:
        sys.exit(f"usage: python3 {sys.argv[0]} PATTERN")

    pattern = argv[0]
    for line in sys.stdin:
        if pattern in line:
            print(line.rstrip())


if __name__ == "__main__":
    main(sys.argv[1:])
```

```bash
$ cat /etc/services | python3 grep.py 8080
http-alt	8080/tcp	webcache	# WWW caching service
```

> `sys.argv` is fine for one or two positional arguments. As soon as you need flags like `-v` or `--port 8080`, use [`argparse`](10-argparse.md). It writes the help text and error handling for you.

## Exercises

- Extend `grep.py` to read from a file given as a second argument: `python3 grep.py 8080 /etc/services`.
- Then make the file optional: read the file if given, otherwise fall back to `stdin`, just like the real `grep`.
- Add a `-i` flag for case-insensitive matching.
