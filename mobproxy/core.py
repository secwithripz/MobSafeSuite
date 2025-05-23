import json
import re
import time
import os

def live_analyze(log_path="logs/traffic.json"):
    print("[📡] Live monitoring started...\n")

    seen = set()
    while True:
        if not os.path.exists(log_path):
            time.sleep(1)
            continue

        with open(log_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            if line in seen:
                continue
            seen.add(line)

            try:
                entry = json.loads(line)
                url = entry.get("url", "")
                body = entry.get("body", "")

                if url.startswith("http://"):
                    print(f"[!] Insecure protocol used: {url}")
                if re.search(r"(password|pass|pwd)", body, re.IGNORECASE):
                    print(f"[!] Password in body: {body[:80]}...")
                if re.search(r"api[_-]?key\s*[:=]\s*['\"]?\w{10,}", body, re.IGNORECASE):
                    print(f"[!] API key in body: {body[:80]}...")
                if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", body):
                    print(f"[!] Email in body: {body[:80]}...")
                if re.search(r"\b(?:\d[ -]*?){13,16}\b", body):
                    print(f"[!] Credit card in body: {body[:80]}...")

            except json.JSONDecodeError:
                continue

        time.sleep(1)
