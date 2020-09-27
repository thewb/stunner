#!/usr/local/bin/python3.8
from scapy.all import *
import geolite2
from IPy import IP

t = geolite2.MaxMindDb("GeoLite2-City.mmdb")
reader = t.reader()

def is_stun(pkt):
	try:
		#if packet is a Binding Success Response
		if pkt[0]['UDP'].load[0:3] == b"\x01\x01\x00":
			return True
		else:
			return False
	except:
		pass

def get_ip(pkt):
	ip = pkt['IP'].dst
	return ip

def is_private(address):
	ip = IP(address)
	type = ip.iptype()
	if type == "PRIVATE":
		return True
	else:
		return False

def country_lookup(ip):
	r = reader.get(ip)
	country = r['country']['names']['en']
	try:
		city = r['city']['names']['en']
	except:
		city = "unknown"
	location = city + ", " + country
	return location

def intercept(packet):
	if is_stun(packet):
		ip = get_ip(packet)
		if not is_private(ip):
			location = country_lookup(ip)
			print("Location for IP {} is {}".format(ip, location))
		else:
			pass

sniff(filter='udp', prn=intercept)

