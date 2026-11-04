#!/usr/bin/env python3
"""Download a Java package THROUGH our Artifactory into the packages/ folder.

Usage: python3 pull_package.py
Needs ART_USER / ART_PW, either as environment variables or in a .env file
in this folder or the folder above it. Never commit the .env file.
"""
import base64
import os
import urllib.request

# --- Which Artifactory and which repo ---
ARTIFACTORY = "http://192.168.30.132:8084/artifactory"
REPO = "maven_test2"

# --- Which package to pull (change these to pull something else) ---
GROUP = "org.apache.commons"
NAME = "commons-lang3"
VERSION = "3.14.0"

# --- Load username/password from .env (this folder, or the one above) ---
here = os.path.dirname(os.path.abspath(__file__))
for folder in (here, os.path.dirname(here)):
    env_file = os.path.join(folder, ".env")
    if os.path.exists(env_file):
        for line in open(env_file):
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ.setdefault(key, value.strip("'\""))
        break
user = os.environ.get("ART_USER", "admin")
password = os.environ["ART_PW"]

# Maven stores files at: group-with-slashes/name/version/name-version.jar
file_name = f"{NAME}-{VERSION}.jar"
url = f"{ARTIFACTORY}/{REPO}/{GROUP.replace('.', '/')}/{NAME}/{VERSION}/{file_name}"
save_to = os.path.join(here, "packages", file_name)

print(f"Pulling {NAME} {VERSION} through Artifactory repo '{REPO}'...")
print(f"  {url}")

login = base64.b64encode(f"{user}:{password}".encode()).decode()
request = urllib.request.Request(url, headers={"Authorization": f"Basic {login}"})

try:
    with urllib.request.urlopen(request) as response:
        data = response.read()
    os.makedirs(os.path.dirname(save_to), exist_ok=True)
    with open(save_to, "wb") as f:
        f.write(data)
    print(f"SUCCESS: saved packages/{file_name} ({len(data) // 1024} KB)")
except urllib.error.HTTPError as e:
    print(f"FAILED: HTTP {e.code}")
