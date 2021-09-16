import threading
import socket
import json
import os
import time

from cmd_line import *


class Server:
	def __init__(self):
		# Server details
		self.IP = "127.0.0.1"#socket.gethostbyname(socket.gethostname())
		print(self.IP)
		self.PORT = 5050
		self.BUFFER = 1024
		self.FORMAT = "utf-8"
		self.ADDR = (self.IP, self.PORT)
		
		# Clients 
		self.clients = {}
		self.active_clients = {}

		# Tokens
		self.ACCEPTED = "[ACCEPTED]"
		self.REJECTED = "[REJECTED]"
		self.LOGIN = "[LOGIN]"
		self.SIGNUP = "[SIGNUP]"
		self.DISCONNECT = "[DISCONNECT]"
		self.MSG = "[MSG]"
		self.SERVER = "[SERVER]"
		self.NEW_SV = "[NEW_SV]"
		self.JOIN = "[JOIN]"
		self.LEAVE = "[LEAVE]"
		self.SELECT = "[SELECT]"
	
		self.running = True

	# Serialization of clients data
	def __load_data(self):
		with open(os.path.join("clients.json"), "r") as r:
			self.clients = json.load(r)
		r.close()

	def __save_data(self):
		with open(os.path.join("clients.json"), "w") as w:
			json.dump(self.clients, w)
		w.close()

	# Client handlers
	def __handle_login(self, conn, addr):
		username = ""

		while True:
			recv_info = conn.recv(self.BUFFER).decode(self.FORMAT)
			tokens = recv_info.split(" ")

			# If the info is from login page
			if tokens[0] == self.LOGIN:
				username = tokens[1].split(":")[1]
				password = tokens[2].split(":")[1]
				
				# Checking for username and password
				time.sleep(0.1)
				if username in self.clients:
					if password == self.clients[username]["password"]:
						time.sleep(0.1)
						conn.send(self.ACCEPTED.encode(self.FORMAT))
						return [True, username]
				
				time.sleep(0.1)
				conn.send(self.REJECTED.encode(self.FORMAT))

			# If the info is from signup page
			elif tokens[0] == self.SIGNUP:
				username = tokens[1].split(":")[1]
				password = tokens[2].split(":")[1]

				# Checking if username already doesnt exists
				time.sleep(0.1)
				if username not in self.clients:
					# Saving the clients info
					self.clients.update({username: 
											{
												"password": password,
												"ip": addr[0],
												"sv": [],
												"current_sv": ""
											}
										})
					self.__save_data()
					time.sleep(0.1)
					conn.send(self.ACCEPTED.encode(self.FORMAT))
					return [True, username]
				else:
					time.sleep(0.1)
					conn.send(self.REJECTED.encode(self.FORMAT))

			# If the app closed
			elif tokens[0] == self.DISCONNECT:
				return [False, username]
	
	# Function to create new server
	def __create_new_sv(self, conn, key, name):
		servers = os.listdir(os.path.join("Servers"))
		if key in servers:
			time.sleep(0.1)
			conn.send(self.REJECTED.encode(self.FORMAT))
		else:
			time.sleep(0.1)
			conn.send(self.ACCEPTED.encode(self.FORMAT))

			os.mkdir(os.path.join(f"Servers/{key}"))
			sv_info = {
					"name": name,
					"mem": []
				}

			# Saving the info
			with open(os.path.join(f"Servers/{key}/sv_info.json"), "w") as w:
				json.dump(sv_info, w)
			w.close()

			# Creating new chat file
			f = open(os.path.join(f"Servers/{key}/chat.txt"), "w")
			f.close()

	# Function to send the joined servers' data
	def __send_server_data(self, conn, username):
		servers = self.clients[username]["sv"]
		total_servers = os.listdir(os.path.join("Servers"))

		data_to_send = self.SERVER

		for i in servers:
			for j in total_servers:
				if i == j:
					# Getting server infos
					with open(os.path.join(f"Servers/{j}/sv_info.json"), "r") as r:
						sv_info = json.load(r)
					r.close()
				
					name = sv_info["name"]
					key = j

					data_to_send += f" {key}:{name}"

		time.sleep(0.1)
		conn.send(data_to_send.encode(self.FORMAT))

	# Message stuff
	def __send_msg_history(self, conn, key):
		sv_list = os.listdir(os.path.join(f"Servers"))
		
		if key in sv_list:
			with open(os.path.join(f"Servers/{key}/chat.txt"), "r") as r:
				chat_history = r.read()

			data = self.MSG + " " + chat_history
			time.sleep(0.1)
			conn.send(data.encode(self.FORMAT))

	def __send_msg(self, key, msg):
		sv_list = os.listdir(os.path.join(f"Servers"))

		if key in sv_list:
			with open(os.path.join(f"Servers/{key}/sv_info.json"), "r") as r:
				sv_info = json.load(r)
			r.close()

			members = sv_info["mem"]
			
			# Sending the online members the msg
			for i in members:
				if self.clients[i]["current_sv"] == key:
					if i in self.active_clients:
						self.active_clients[i].send(msg.encode(self.FORMAT))

			# Saving the msg
			tokens = msg.split(" ")
			tokens.pop(0)
			msg = " ".join(tokens)

			with open(os.path.join(f"Servers/{key}/chat.txt"), "a") as a:
				a.write(msg)
			a.close()

	# Function to join in a server
	def __join_to_server(self, key, name):
		sv_list = os.listdir(os.path.join("Servers/"))
		if key in sv_list:
			if key not in self.clients[name]["sv"]:
				self.clients[name]["sv"].append(key)
				self.__save_data()

				with open(os.path.join(f"Servers/{key}/sv_info.json"), "r") as r:
					sv_info = json.load(r)
				r.close()

				sv_info["mem"].append(name)
				
				with open(os.path.join(f"Servers/{key}/sv_info.json"), "w") as w:
					json.dump(sv_info, w)
				w.close()

	# Function to leave server
	def __leave_server(self, key, name):
		if key in self.clients[name]["sv"]:
			self.clients[name]["sv"].remove(key)
			self.clients[name]["current_sv"] = ""
			self.__save_data()

			with open(os.path.join(f"Servers/{key}/sv_info.json"), "r") as r:
				sv_info = json.load(r)
			r.close()

			sv_info["mem"].remove(name)

			with open(os.path.join(f"Servers/{key}/sv_info.json"), "w") as w:
				json.dump(sv_info, w)
			w.close()

	def __handle_clients(self, conn, addr):	
		current_sv = None

		# Handle login and signup
		client_online = self.__handle_login(conn, addr)

		# Give the user the required data when they are in home page
		if client_online[0]:
			self.active_clients.update({client_online[1]: conn})	
			self.__send_server_data(conn, client_online[1])

		# Handle the main client and server data trading
		while client_online[0]:
			recv_info = conn.recv(self.BUFFER).decode(self.FORMAT)
			tokens = recv_info.split(" ")

			if tokens[0] == self.DISCONNECT:
				client_online[0] = False
				time.sleep(0.1)
				conn.send(self.DISCONNECT.encode(self.FORMAT))		

				self.active_clients.pop(client_online[1])

			# When new server is created
			if tokens[0] == self.NEW_SV:
				key = tokens[1].split(":")[1]
				name = tokens[2].split(":")[1]

				self.__create_new_sv(conn, key, name)
			
			# When member joins a server
			elif tokens[0] == self.JOIN:
				name = tokens[1].split(":")[1]
				key = tokens[2].split(":")[1]

				self.__join_to_server(key, name)

				time.sleep(0.1)
				self.__send_server_data(conn, name)
			
			# When member leaves a server
			elif tokens[0] == self.LEAVE:
				name = tokens[1].split(":")[1]
				key = tokens[2].split(":")[1]

				self.__leave_server(key, name)
				self.__send_server_data(conn, client_online[1])

			# When user selects a server
			elif tokens[0] == self.SELECT:
				key = tokens[1]
				self.__send_msg_history(conn, key)
				current_sv = key

				self.clients[client_online[1]]["current_sv"] = current_sv
				self.__save_data()

			# When user sends a msg
			elif tokens[0] == self.MSG:
				self.__send_msg(current_sv, recv_info)	
	
		conn.close()

	# Server stuff
	def __create_server(self):
		#try:
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(self.ADDR)
		#except Exception as e:
		#	print(f"{colors.RED}{e}{colors.DEFAULT}")

	def start(self):
		print(f"{colors.GREEN}Server is starting....{colors.DEFAULT}")

		self.__create_server()
		self.__load_data()
		
		# Cmd line
		self.cmd_line = CmdLine(self)
		cmd_line_thread = threading.Thread(target = self.cmd_line.start)
		cmd_line_thread.start()

		self.server.listen()

		while self.running:
			#try:
			conn, addr = self.server.accept()
			
			# Creating a new thread
			client_thread = threading.Thread(target = self.__handle_clients, args = (conn, addr, ))
			client_thread.start()
			#except Exception as e:
			#	print(f"{colors.RED}{e}{colors.DEFAULT}")


if __name__ == "__main__":
	server = Server()
	server.start()
