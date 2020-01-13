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

    if recieved_json is None:
        return None
    else:
        return User(recieved_json['username'], recieved_json['auth_key'])
    # recv_json = tcp.recv(1024).decode()

def sign_up(tcp):
    print("##### CCADASTRO DE USUÁRIO #####")
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha do usuário: ")


def authenticate_user(tcp, auth_user):

    sended_json = json.dumps({'command': 'authenticate_user', 'username': auth_user.username, 'auth_key': auth_user.auth_key})
    tcp.send(sended_json.encode())

    result = tcp.recv(10).decode()

    if result is 'true'
        return auth_user
    else:
        return None

     

# convert into JSON:
y = json.dumps(x)

host = '127.0.0.1'  #ip do servidor
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
        choice = ("Escolha as opções a seguir: \n1 - login; \n2 - cadastrar.") 
        if choice == 1:
            auth_user = login_user(tcp)
            print(auth_user.username)
        if choice == 2:
    else:
        auth_user = authenticate_user(tcp, auth_user)
        
tcp.close() #encerra o cliente
