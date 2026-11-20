# Set Up Your Lab

You learn Python for system administration by **running** things: reading `/etc/passwd`, starting processes, checking ports. So before the first chapter, get a Linux box with Python on it.

You have two options. Pick one.

## Option 1: A free Linux VM in your browser (recommended)

The [iximiuz Labs Python Playground](https://labs.iximiuz.com/playgrounds/python) gives you a real Linux VM with root access, the latest Python 3, `uv`, `pyenv`, Docker and VS Code. It starts in seconds and there is no paywall. You only need to sign in.

1. Open the [Python Playground](https://labs.iximiuz.com/playgrounds/python).
2. Sign in and click **Start playground**.
3. Open the terminal tab and check your Python version:

```bash
python3 --version
```

4. Clone this guide so every example is on the machine:

```bash
git clone https://github.com/tuladhar/Python-for-SysAdmin.git
cd Python-for-SysAdmin/examples
ls
```

Because it is a throwaway VM, you can break things safely. Delete files, kill processes, fill the disk. Nothing touches your own laptop.

<!-- DEMO GIF: when assets/playground-demo.gif exists, uncomment the line below.
![Starting the iximiuz Labs Python playground and running grep.py](../assets/playground-demo.gif)
-->

## Option 2: Your own Linux or macOS machine

Most Linux distributions and macOS already ship Python 3. Check it:

```bash
python3 --version
```

You want **Python 3.10 or newer**. Every example in this guide uses only the standard library, so there is nothing to install with `pip`.

If you need a newer Python, [uv](https://docs.astral.sh/uv/) is the quickest way to get one without touching the system Python:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.13
uv run --python 3.13 python --version
```

> Never upgrade or remove the system Python on a server. Tools like `dnf`, `apt` and many agents depend on it. Use `uv` or a virtual environment instead.

## How to use this guide

- Each chapter introduces one module and ends with a small, real script.
- Type the examples yourself instead of copy-pasting. You remember what your fingers typed.
- Every script lives in the [`examples/`](https://github.com/tuladhar/Python-for-SysAdmin/tree/main/examples) folder, so you can compare your version with the reference.
- Try the **exercises** at the end of a chapter before you move on.

## Stuck? Learn it step by step with AI

If a concept doesn't click, use the free [`/step-by-step` Claude skill](https://github.com/tuladhar/my-claude-skills-as-devops-engineer). It explains any topic one short sentence at a time and waits for you to say "understood" before moving on, so you never get a wall of text:

```text
/step-by-step how subprocess.run captures stdout and the exit code
/step-by-step what os.walk yields for each directory
```
