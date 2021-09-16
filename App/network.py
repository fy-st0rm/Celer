import socket


class Network:
	def __init__(self, IP, PORT, BUFFER, FORMAT):
		self.IP = IP
		self.PORT = PORT
		self.ADDR = (self.IP, self.PORT)
		self.BUFFER = BUFFER
		self.FORMAT = FORMAT

	def connect(self):
		self.network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.network.connect(self.ADDR)
	
	def send(self, data):
		self.network.send(data.encode(self.FORMAT))

	def recv(self):
		return self.network.recv(self.BUFFER).decode(self.FORMAT)

