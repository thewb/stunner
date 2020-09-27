#!/usr/local/bin/python3.8

import requests
import json
import sys

S = requests.Session()

server = sys.argv[1] if not sys.argv[1] else "chatserv"

resp = S.get("http://chatserv.omegle.com/status")
j = resp.json()
print(json.dumps(j, indent=4))
