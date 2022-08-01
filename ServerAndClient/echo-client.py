# echo-client.py

import socket
import time 

start = time.time()  # 시작 시간 저장

client = socket.socket()
client.connect(('127.0.0.1', 6543))
client.send('Hello'.encode('utf-8'))

print(client.recv(1024))
print("time :", time.time() - start)  # (현재 시간)-(시작 시간)=(실행 시간)