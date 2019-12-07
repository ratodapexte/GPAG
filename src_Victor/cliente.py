import socket

HOST = '127.0.0.1'
PORT = 30000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = (HOST,  PORT)

tcp.connect(dest)

msg = input('Digite sua mensagem: ').encode()

while msg.decode('utf-8') != 'exit':
    tcp.send(msg)
    msg = input('Digite sua mensagem: ').encode()

tcp.close()