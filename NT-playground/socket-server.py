# Author: Natalie Truong
# Homework 1

import socket

# Create server socket
host = '127.0.0.1'
port = 1234
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5)

while True:
	# Connect
    connection, address = serversocket.accept()
    # Receiving data
    buf = connection.recv(64)
    if len(buf) > 0 and len(buf)<12:
        print (buf.decode())
        break