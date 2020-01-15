import socket
import json

class User():
    def __init__(self, username, auth_key):
        self.username = username
        self.auth_key = auth_key

# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}



def login_user(tcp):
    print("##### LOGIN DE USUÁRIO #####")
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha do usuário: ")

    sended_json = json.dumps({'command': 'login_user', 'username': username, 'password': password})
    tcp.send(sended_json.encode())

    recieved_json =  json.loads(tcp.recv(1024).decode())

    if recieved_json['username'] is 'None':
        return None
    else:
        return User(recieved_json['username'], recieved_json['auth_key'])
    # recv_json = tcp.recv(1024).decode()

def sign_up(tcp):
    print("##### CCADASTRO DE USUÁRIO #####")
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha do usuário: ")
    name = input("Digite o nome: ")
    cpf = input("Digite o cpf: ")
    email = input("Digite o seu email: ")
    phone = input("Digite o seu telefone: ")    

    sended_json = json.dumps({'command': 'sign_up', 'username': username, 'password': password,
                                'name': name, 'cpf': cpf, 'email': email, 'phone': phone})
    tcp.send(sended_json.encode())
    return tcp.recv(1024).decode()

def authenticate_user(tcp, auth_user):

    sended_json = json.dumps({'command': 'authenticate_user', 'username': auth_user.username, 'auth_key': auth_user.auth_key})
    tcp.send(sended_json.encode())

    result = tcp.recv(100).decode()

    if result == 'true':
        return auth_user
    else:
        return None                


def list_bills(tcp, auth_user):

    sended_json = json.dumps({'command': 'list_bills', 'username': auth_user.username, 'auth_key': auth_user.auth_key})
    tcp.send(sended_json.encode())

    list_of_bills = tcp.recv(1024).decode()

    

######################################################################################################

host = '83.136.219.66'  #ip do servidor
port = 30000        #porta que o servidor vai usar pra trocar informações

tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #AF_INET é usar a internet, SOCK_STREAM é TCP
server = (host,port) #tupla
tcp.connect(server) #conecta o servidor

print("Conectado ao servidor ", host)
print("Para sair digite 'sair'")
msg = 'none'
print(msg)
auth_user = None

while msg != 'sair':
    if auth_user is None:
        choice = int(input("Escolha as opções a seguir: \n1 - login; \n2 - cadastrar.\n")) 
        if choice == 1:
            auth_user = login_user(tcp)
            if auth_user is not None:
                print(auth_user.username)
            else:
                print('Erro!')
        if choice == 2:
            print(sign_up(tcp))
    else:
        print("Usuário logado")
        
tcp.close() #encerra o cliente
