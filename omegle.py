#!/usr/local/bin/python3.8

import requests
import json

S = requests.Session()

resp = S.get("http://chatserv.omegle.com/status")
j = resp.json()
print(json.dumps(j, indent=4))
