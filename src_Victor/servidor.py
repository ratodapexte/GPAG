import socket
import secrets
import json
from reused_code import *

def login_user(dict):
    print("Dados recebidos: ", dict)
    querry = querry_one("""SELECT login FROM users WHERE login = %s AND password = %s""",
            dict['username'], dict['password'])
    if querry is None:
        return "Nada encontrado!".encode()
    else:
        result = "Usuário encontrado: " + querry + secrets.token_hex() 
        return result.encode() 

HOST = ''
PORT = 30000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    print ('Conectado por: ', cliente)
    while True:
        msg = con.recv(1024).decode('utf-8')
        if not msg:break
        recv_json = json.loads(msg)
        print("Comando: ", recv_json['command'])
        con.send(globals()[recv_json['command']](recv_json))
    print ('Finalizando conexao do cliente ', cliente)
    con.close()
    