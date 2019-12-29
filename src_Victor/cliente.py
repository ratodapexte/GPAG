import socket
# import models

class Connection:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dest = (self.HOST, self.PORT)

    def connect(self):
        self.tcp.connect(self.dest)

    def send(self, msg):
        self.tcp.send(msg)

    def close(self):
        self.tcp.close()



def connect_to_server():
    connection1 = Connection('127.0.0.1', 30000) 
 
    connection1.connect()

    msg = input('Digite sua mensagem: ').encode()

    while msg.decode('utf-8') != 'exit':
        connection1.send(msg)
        msg = input('Digite sua mensagem: ').encode()

def close_socket(connection):
    connection.close()
        