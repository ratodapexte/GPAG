import socket
from views import *

HOST = ''
PORT = 30000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
lista_de_clientes = []
while True:
    con, cliente = tcp.accept()
    print ('Conectado por: ', cliente)
    while True:
        msg = con.recv(1024).decode('utf-8')
        if not msg:break
        if msg == 'criar conta':
            lista_de_clientes.append(cadastrar_cliente())
            print('Foram cadastrados ', len(lista_de_clientes), ' clientes')  
        print(cliente, msg)
    print ('Finalizando conexao do cliente ', cliente)
    con.close()
