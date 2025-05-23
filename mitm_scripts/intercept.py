from mitmproxy import http
import json
import os

LOG_PATH = "logs/traffic.json"

def request(flow: http.HTTPFlow) -> None:
    request_data = {
        "method": flow.request.method,
        "url": flow.request.pretty_url,
        "headers": dict(flow.request.headers),
        "body": flow.request.get_text()
    }

    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a") as logfile:
        logfile.write(json.dumps(request_data) + "\n")
