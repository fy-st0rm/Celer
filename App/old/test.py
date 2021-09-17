import socket

IP = "127.0.1.1"
PORT = 5050
ADDR = (IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
