# echo-server.py

import socket

server = socket.socket()
server.bind(('0.0.0.0', 6543))
server.listen()

conn, addr = server.accept()
data = conn.recv(1024)
conn.send(data)