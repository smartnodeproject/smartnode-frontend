from Crypto.Cipher import AES
import base64
import sys
import re

def decrypt_hexstr(d):
	fuck = 'fdsl;mewrjope456fds4fbvfnjwaugfo'
	aes = AES.new(fuck)
	return aes.decrypt(d.decode('hex'))

def decrypt_hex(d):
	fuck = 'fdsl;mewrjope456fds4fbvfnjwaugfo'
	aes = AES.new(fuck)
	return aes.decrypt(d)

if __name__ == '__main__':
	d = sys.argv[1]
	decrypt_hexstr(d)

