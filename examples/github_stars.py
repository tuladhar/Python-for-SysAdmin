#!/usr/bin/env python3
# github_stars.py
import json
import os
import urllib.request

url = "https://api.github.com/repos/tuladhar/Python-for-SysAdmin"
request = urllib.request.Request(url)
token = os.environ.get("GITHUB_TOKEN")
if token:  # optional: raises the rate limit from 60 to 5,000 requests per hour
    request.add_header("Authorization", f"Bearer {token}")

with urllib.request.urlopen(request, timeout=10) as response:
    repo = json.load(response)

print(f"{repo['full_name']} has {repo['stargazers_count']} stars")
