from network import *
from login import *


# Network constants
IP = "127.0.0.1"#socket.gethostbyname("0.tcp.ngrok.io")#socket.gethostname())	
PORT = 5050
BUFFER = 1024
FORMAT = "utf-8"

client = Network(IP, PORT, BUFFER, FORMAT)
client.connect()

# Opening login menu
login = Login(client)
login.run()


# Telling the server that the client is being disconnected
client.send("[DISCONNECT]")

