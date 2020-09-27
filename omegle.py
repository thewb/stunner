#!/usr/local/bin/python3.8

import requests
import json
import socket
import geoip

from geolite2 import geolite2
S = requests.Session()
reader = geolite2.reader()

resp = S.get("http://chatserv.omegle.com/status")

for i in resp.json()['servers']:
	ip = socket.gethostbyname(i + '.omegle.com')
	r = S.get("http://" + i + ".omegle.com/status")
	j = r.json()
	r = reader.get(ip)
	print('Server: {} count: {}'.format(i, j["count"]))
