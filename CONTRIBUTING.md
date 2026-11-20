# Contributing

Python for SysAdmin is a community guide. Every chapter you add or fix shows up on the website at **[purutuladhar.com/python-for-sys-admin](https://purutuladhar.com/python-for-sys-admin/)** as soon as it is merged. No build step, no website code to touch.

All kinds of help are welcome:

- Fix a typo, a broken example or an outdated explanation.
- Write a chapter from the **wanted** list in [`chapters/chapters.json`](chapters/chapters.json) (shown as "Help wanted" on the website).
- Propose a new chapter by [opening an issue](https://github.com/tuladhar/Python-for-SysAdmin/issues/new?template=chapter.yml).
- Record a short GIF that shows an example running.

## How the repo is organised

```text
chapters/
  chapters.json        # order of chapters + the "wanted" list
  01-set-up-your-lab.md
  02-standard-io.md
  ...
examples/              # every runnable script from the chapters
assets/                # images and GIFs used by chapters
scripts/               # tests: test_examples.sh and check_snippets.py
```

The website reads `chapters/chapters.json`, then loads each chapter's Markdown file straight from the `main` branch.

## Fixing an existing chapter

1. Open the chapter on the website and click **Edit this page on GitHub**, or edit the file in `chapters/` directly.
2. If you change a script, update the matching file in `examples/` too.
3. Open a pull request.

## Writing a new chapter

1. Comment on (or open) an issue for the topic so nobody else starts the same chapter.
2. Create `chapters/NN-short-name.md`, using the next free number.
3. Add an entry to the right section in `chapters/chapters.json`:

   ```json
   { "slug": "regex", "file": "15-regex.md", "title": "Regular Expressions", "summary": "Parse log lines, extract IPs and validate input." }
   ```

   If the topic was on the `wanted` list, remove it from there.
4. Put every complete script in `examples/` as well.
5. Open a pull request.

### Chapter style

Look at [`09-subprocess.md`](chapters/09-subprocess.md) for a good template.

- Start with a `# Title` and one or two sentences on **why a sysadmin needs this**.
- Short sections with `##` headings. Explain one idea, then show it.
- Use **Python 3.11+** and the standard library unless the chapter is about a third-party package.
- Use `pathlib`, f-strings, `subprocess.run()`, `with` blocks and `encoding="utf-8"`.
- Every complete script starts with `#!/usr/bin/env python3` and a `# filename.py` comment, and must run as shown.
- Show the command and its output in a separate `bash` block.
- End with **Exercises** and a link to the official documentation.
- Link to other chapters by file name, e.g. `[argparse](10-argparse.md)`. The website turns these into chapter links.
- Use simple, plain English. Many readers are not native speakers.

Preview your Markdown in the GitHub pull request "Preview" tab or any Markdown viewer.

### Test before you open a pull request

Two scripts check that everything in the guide actually runs. GitHub Actions runs them on every pull request, on Python 3.11 and the latest Python:

```bash
scripts/test_examples.sh          # runs every script in examples/ and checks its exit code
python3 scripts/check_snippets.py # runs every inline snippet in chapters/
```

If you add a script to `examples/`, add a line for it to `scripts/test_examples.sh`. The quickest place to run them is the free [iximiuz Labs Python Playground](https://labs.iximiuz.com/playgrounds/python).

## Adding a GIF

Short GIFs of a script running in a terminal help a lot, especially in the [iximiuz Labs Python Playground](https://labs.iximiuz.com/playgrounds/python).

- Keep it under 20 seconds and under 3 MB. Tools like [VHS](https://github.com/charmbracelet/vhs) or [asciinema](https://asciinema.org/) + [agg](https://github.com/asciinema/agg) work well.
- Put it in `assets/` and reference it from the chapter: `![What the GIF shows](../assets/my-demo.gif)`.

## Code of conduct

Be kind and patient. Everyone here is learning.
