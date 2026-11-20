# Python for SysAdmin

[![Read the guide](https://img.shields.io/badge/Read_the_guide-purutuladhar.com-9ece6a?style=flat-square)](https://purutuladhar.com/python-for-sys-admin/)
[![Try it free](https://img.shields.io/badge/Hands--on-iximiuz_Labs_Playground-7aa2f7?style=flat-square)](https://labs.iximiuz.com/playgrounds/python)
[![GitHub stars](https://img.shields.io/github/stars/tuladhar/Python-for-SysAdmin?style=flat-square)](https://github.com/tuladhar/Python-for-SysAdmin/stargazers)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-e0af68?style=flat-square)](CONTRIBUTING.md)

A practical, community-driven guide to **Python 3 for system administrators and DevOps engineers**. Each chapter teaches one module through the tasks you actually do on servers: reading configs and logs, running commands, checking disks and ports, and building your own command-line tools.

**📖 Read it as a website: [purutuladhar.com/python-for-sys-admin](https://purutuladhar.com/python-for-sys-admin/)**

⭐ If this guide helps you, please **give it a star**. It helps other sysadmins find it.

## Practice hands-on, for free

You don't need a server. The **[iximiuz Labs Python Playground](https://labs.iximiuz.com/playgrounds/python)** gives you a real Linux VM with root access, the latest Python 3, `uv`, Docker and VS Code, right in your browser. Start it, then:

```bash
git clone https://github.com/tuladhar/Python-for-SysAdmin.git
cd Python-for-SysAdmin/examples
cat /etc/passwd | python3 grep.py bash
```

## Learn step by step with AI

Stuck on a concept? Install the free [`/step-by-step` Claude skill](https://github.com/tuladhar/my-claude-skills-as-devops-engineer). It explains any topic one short sentence at a time, and waits for you to say "understood" before it moves on:

```text
/step-by-step how subprocess.run captures stdout and the exit code
```

## Contents

### Getting Started
1. [Set Up Your Lab](chapters/01-set-up-your-lab.md)
2. [Standard Input, Output and Error](chapters/02-standard-io.md)
3. [Working with Files](chapters/03-working-with-files.md)
4. [Command-line Arguments](chapters/04-command-line-arguments.md)

### Standard Library
5. [The `os` Module](chapters/05-os-module.md)
6. [The `sys` Module](chapters/06-sys-module.md)
7. [`shutil` and `glob`](chapters/07-shutil-and-glob.md)
8. [Date and Time](chapters/08-date-and-time.md)
9. [Running Commands with `subprocess`](chapters/09-subprocess.md)
10. [Building CLIs with `argparse`](chapters/10-argparse.md)

### Data and Networking
11. [Working with JSON](chapters/11-json.md)
12. [Working with CSV](chapters/12-csv.md)
13. [SQLite: a Database in a File](chapters/13-sqlite.md)
14. [Network Checks with `socket`](chapters/14-socket.md)

### Help wanted 🙌
Regular expressions, logging, compression, XML, platform, signals, `ipaddress`, concurrency, HTTP APIs, SSH automation (`paramiko`), `psutil`, `netmiko`, `boto3`, Docker and Kubernetes clients, Jinja2 templating, and testing with `pytest`.

**[Pick one and write it →](CONTRIBUTING.md)**

All runnable scripts are in [`examples/`](examples/).

## Contributing

This guide is written by the community. Fixing a typo is as welcome as writing a new chapter. Merged chapters appear on the website automatically. Read [CONTRIBUTING.md](CONTRIBUTING.md) to get started, or [open an issue](https://github.com/tuladhar/Python-for-SysAdmin/issues/new?template=chapter.yml) to propose a topic.

## Credits

- Author: [Puru Tuladhar](https://github.com/tuladhar)
- Editor and maintainer: [Silent Mobius](https://github.com/silent-mobius)
- And [everyone who contributed](https://github.com/tuladhar/Python-for-SysAdmin/graphs/contributors) ❤️

Licensed under the terms in [LICENSE](LICENSE).
