# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.websocket
import os.path
import json
from json import *
import rethinkdb as rethink
import socket
from static.python.usage import usage_response
from static.python.environment import environment_response
import re
import time

class WelcomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("welcome.html")

class OverviewHandler(tornado.web.RequestHandler):
	def get(self):	
		conn = rethink.connect(host = 'localhost',port = 28015,db = 'smartnode')
		mac_name = rethink.table('mac').run(conn)
		self.render("overview.html", name = mac_name)
	def post(self):
		mac_name = self.get_argument('mac_name')
		conn = rethink.connect(host = 'localhost',port = 28015,db = 'smartnode')
		mac_name = rethink.table('mac').filter({'mac_name':mac_name}).run(conn)
		self.render("overview.html", name = mac_name)

class AddmHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("addm.html")
	def post(self):
		mac_name = self.get_argument('namem')
		mac_position = self.get_argument('positionm')
		mac_ip = self.get_argument('ipm')
		mac_port = self.get_argument('portm')
		mac_protocol = self.get_argument('protocol')
		mac_head = {'mac_name':mac_name, 'mac_position':mac_position, 'mac_ip':mac_ip, 'mac_port':mac_port, 'mac_protocol':mac_protocol}
		upload_path = os.path.join(os.path.dirname(__file__), 'static/json')
		file_metas = self.request.files['settingm']
		for meta in file_metas:
			filename = meta['filename']
			filepath = os.path.join(upload_path, filename)
			with open(filepath, 'wb') as up:
				up.write(meta['body'])
			mac_body = json.load(file(filepath))
			#f = open(filepath, 'r')
			#mac_body = json.loads(f.read(), "UTF-8")
			mac = dict(mac_head, **mac_body)
			conn = rethink.connect(host = 'localhost',port = 28015,db = 'smartnode')
			rethink.table("mac").insert(mac).run(conn)
		self.redirect('/overview')

class RemovemHandler(tornado.web.RequestHandler):
	def get(self):
		conn = rethink.connect(host = 'localhost',port = 28015,db = 'smartnode')
		mac_name = rethink.table('mac').run(conn)
		self.render("removem.html", name = mac_name)
	def post(self):
		mac_id = self.request.arguments
		for i in mac_id.values():
			for j in i:
				conn = rethink.connect(host = 'localhost',port = 28015,db = 'smartnode')
				rethink.table("mac").get(j).delete().run(conn)
		self.redirect("/overview")

class MacViewHandler(tornado.web.RequestHandler):
	def send_package(self, command, protocol, server, port):
		if protocol == "UDP":
			addr = (server, port)
			client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			client.sendto(command.decode('hex'), addr)
			#data, ADDR = client.recvfrom(1024)
			#return data
		if protocol == "TCP":
			addr = (server, port)
			client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			client.connect(addr)
			client.send(command)    #send request head code
			client.close()
	def get(self, mac):
		conn = rethink.connect(host = 'localhost',port = 28015,db = 'smartnode')
		for mac in rethink.table("mac").filter({'id':mac}).run(conn):
			self.render("macview.html", mac=mac)
	def post(self, param):
		command = self.get_argument('command')
		protocol = self.get_argument('protocol')
		server = self.get_argument('server')
		port = int(self.get_argument('port'))
		try:
			self.send_package(command, protocol, server, port)
		except:
			pass
class UsageHandler(tornado.web.RequestHandler):
	def get(self):
		filename = os.path.join(os.path.dirname(__file__), "static/python/usage.py")
		if os.path.exists(filename):
			flag = True
		else:
			flag = False
		self.render("usage.html", flag=flag)

class UsageStatusHandler(tornado.websocket.WebSocketHandler):
	def open(self):
			data = usage_response()
			self.write_message(data)
	def on_message(self, message):
			data = usage_response()
			self.write_message(data)
class EnvironmentHandler(tornado.web.RequestHandler):
	def get(self):
		filename = os.path.join(os.path.dirname(__file__), "static/python/environment.py")
		if os.path.exists(filename):
			flag = True
		else:
			flag = False
		self.render("environment.html", flag=flag)

class EnvironmentStatusHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		data = environment_response()
		self.write_message(data)
	def on_message(self, message):
		data = environment_response()
		self.write_message(data)

class M2MHandler(tornado.web.RequestHandler):
	def get(self):
		conn = rethink.connect(host = 'localhost',port = 28015,db = 'smartnode')
		mac_name1 = rethink.table('mac').run(conn)
		mac_name2 = rethink.table('mac').run(conn)
		mac_name3 = rethink.table('mac').run(conn)
		mac_name4 = rethink.table('mac').run(conn)
		mac_name5 = rethink.table('mac').run(conn)
		self.render("M2M.html", name1 = mac_name1, name2 = mac_name2, name3 = mac_name3, name4 = mac_name4, name5 = mac_name5)
	def post(self):
		machine1 = self.get_argument('M2M1')
		machine2 = self.get_argument('M2M2')
		do1 = self.get_argument('M2M3')
		do2 = self.get_argument('M2M5')
		many = self.get_argument('M2M4')
		conn = rethink.connect(host = 'localhost',port = 28015,db = 'smartnode')
		for mac1 in rethink.table('mac').filter({'id':machine1}).run(conn):
			MacViewHandler.send_package(do1, mac1['mac_protocol'], mac1['mac_ip'], mac1['mac_port'])
		if many[-1] == "s":
			time.sleep(int(many[0:-1]))
		if many[-1] == "c":
			print "hehe" 
		for mac2 in rethink.table('mac').filter({'id':machine2}).run(conn):
			MacViewHandler.send_package(do2, mac2['mac_protocol'], mac2['mac_ip'], mac2['mac_port'])
		
application = tornado.web.Application([
    (r"/", WelcomeHandler),
    (r"/overview", OverviewHandler),
    (r"/machine/addm", AddmHandler),
    (r"/machine/removem", RemovemHandler),
    (r"/machine/(.*[-].*)", MacViewHandler),
    (r"/usage", UsageHandler),
    (r"/usage/status", UsageStatusHandler),
    (r"/environment", EnvironmentHandler),
    (r"/environment/status", EnvironmentStatusHandler),
    (r"/M2M", M2MHandler)],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    debug = True
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
