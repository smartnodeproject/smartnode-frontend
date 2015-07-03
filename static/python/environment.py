# -*- coding:utf-8 -*-
import socket
import struct
from aes import decrypt_hex
import re
envicode = 'fd918a5e209499ed755e9457d6196a6a63ccebdd7d96da8f951125569a9a96fa5f68616d423a99d203c5d08bd6054706e9eb414b2181476e83b6328eeb9149bb'
server = '10.1.1.143'
port = 27431
usagecode = 'fd918a5e209499ed755e9457d6196a6a63ccebdd7d96da8f951125569a9a96fa3785dd1cd4f6f4e4fef7f97e0802721c4257825e7b1c6726a4117d97d6bf38f3'
def environment_response():
	package = envicode.decode('hex')
	addr = (server, port)
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client.sendto(package, addr)
	data, ADDR = client.recvfrom(1024)
	usage_data = decrypt_hex(data)
	data_foo = re.split('#|%' ,usage_data)
	data = {'temp':float(data_foo[7]),'hum':float(data_foo[9]),'lum':float(data_foo[11])}
	return data
