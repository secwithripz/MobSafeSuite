import json
import re
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "traffic.json")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "reports", "summary.txt")

def analyze():
    if not os.path.exists(LOG_PATH):
        print("[!] Log file not found.")
        return

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

    with open(REPORT_PATH, "w") as report_file, open(LOG_PATH, "r") as log_file:
        for line in log_file:
            entry = json.loads(line)
            url = entry.get("url", "")
            headers = entry.get("headers", {})
            body = entry.get("body", "")

            def log_alert(message):
                print(message)
                report_file.write(message + "\n")

            # Insecure HTTP
            if url.startswith("http://"):
                log_alert(f"[!] Insecure protocol used in: {url}")

            # Authorization Header
            auth = headers.get("Authorization")
            if auth:
                log_alert(f"[!] Token found in Authorization header: {auth}")

            # Password Leak
            if re.search(r"(password|pass|pwd)", body, re.IGNORECASE):
                log_alert(f"[!] Potential password leak in body: {body[:100]}...")

            # Bearer Token
            if re.search(r"Bearer\s+\w+", body, re.IGNORECASE):
                log_alert(f"[!] Bearer token found in body: {body[:100]}...")

            # API Key
            if re.search(r"api[_-]?key\s*[:=]\s*['\"]?\w{10,}", body, re.IGNORECASE):
                log_alert(f"[!] Possible API key in body: {body[:100]}...")

            # Email Address
            if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", body):
                log_alert(f"[!] Email address found in body: {body[:100]}...")

            # Credit Card Number (basic pattern)
            if re.search(r"\b(?:\d[ -]*?){13,16}\b", body):
                log_alert(f"[!] Possible credit card number in body: {body[:100]}...")

if __name__ == "__main__":
    analyze()
