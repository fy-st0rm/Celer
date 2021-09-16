import socket


# Colors for terminal
class colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class CmdLine:
	def __init__(self, server):
		self.server = server

	def __print_clients(self, mode):
		print("username" + " " * 10 + "password" + " " * 13 + "ip")

		# Managing the mode
		if mode == "--all":
			ite = self.server.clients
		elif mode == "--active":
			ite = self.server.active_clients
		else:
			ite = []

		cnt = 0

		for i in ite:
			username = i
			password = self.server.clients[i]["password"]
			ip = self.server.clients[i]["ip"]

			space = len("username" + " " * 10) - len(username)
			print(username + " " * space + password + " " * 10 + ip)
			cnt += 1

		print("Total:", cnt)

	def start(self):
		while self.server.running:
			cmd = input(f"{colors.RED}root{colors.BLUE}@Server${colors.DEFAULT} ")
			tokens = cmd.split(" ")

			if tokens[0] == "shutdown":
				self.server.running = False
				self.server.server.shutdown(socket.SHUT_RDWR)
				self.server.server.close()

				print(f"{colors.GREEN}Shutting down...{colors.DEFAULT}")
			elif tokens[0] == "lc":
				if len(tokens) > 1:
					if tokens[1] == "--active":
						self.__print_clients("--active")
				else:
					self.__print_clients("--all")
