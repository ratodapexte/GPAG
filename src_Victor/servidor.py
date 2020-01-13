import socket
import secrets
import json
from datetime import datetime
from reused_code import *

def login_user(dict):
    print("Dados recebidos: ", dict)
    querry = querry_one("""SELECT username FROM users WHERE username = %s AND password = %s""",
            dict['username'], dict['password'])
    if querry is None:
        return json.dumps({'username': 'None', 'auth_key': 'None'}).encode()
    else:
        auth_key = secrets.token_hex()
        auth_key_init_datetime = datetime.now()
        result = {'username': querry[0], 'auth_key': auth_key}
        commit_querry("""UPDATE users SET auth_key = %s, auth_key_init_datetime = %s 
                        WHERE username = %s AND password = %s""",
        auth_key, auth_key_init_datetime, result['username'], dict['password'])

        return json.dumps(result).encode() 


def sign_up(dict):
    print("Dados recebidos: ", dict)
    status = commit_querry("""INSERT INTO users (username, password, name, cpf, email, phone)
                    VALUES (%s,%s,%s,%s,%s,%s)""", 
                    dict['username'], dict['password'], dict['name'], dict['cpf'], dict['email'], dict['phone'])
    return status


def authenticate_user(dict):
    print("##### AUTENTICANDO USUARIO #####")
    print("Dados recebidos: ", dict)
    querry = querry_one("""SELECT auth_key_init_datetime FROM users WHERE username = %s AND auth_key = %s""",
            dict['username'], dict['auth_key'])

    time_dif = datetime.now() - querry[0]
    print(time_dif.seconds)

    if time_dif.seconds < 10:
        return 'true'.encode()
    else:
        commit_querry("""UPDATE users SET auth_key = null, auth_key_init_datetime = null 
                        WHERE username = %s""", dict['username'])
        return 'false'.encode()


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
    
##############################################################################
'''                              AUTENTICACAO
    RECEBE CHAVE E USUÁRIO
    BUSCA O TEMPO EM QUE A CHAVE DO USUÁRIO FOI AUTENTICADO PELA ULTIMA VEZ
    CASO A DIFERENÇA SEJA MAIOR QUE X O BANCO VAI APAGAR A SUA CHAVE DE AUTENTICACAO
'''
##############################################################################