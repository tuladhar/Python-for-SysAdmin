#!/usr/bin/env python3
# github_stars.py
import json
import urllib.request

url = "https://api.github.com/repos/tuladhar/Python-for-SysAdmin"
with urllib.request.urlopen(url, timeout=10) as response:
    repo = json.load(response)

print(f"{repo['full_name']} has {repo['stargazers_count']} stars")
