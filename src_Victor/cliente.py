import socket
import json

class User():
    def __init__(self, username, auth_key):
        self.username = username
        self.auth_key = auth_key

def login_user(tcp):
    print("##### LOGIN DE USUÁRIO #####")
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha do usuário: ")

    sended_json = json.dumps({'command': 'login_user', 'username': username, 'password': password})
    tcp.send(sended_json.encode())

    recieved_json =  json.loads(tcp.recv(1024).decode())

    if recieved_json['username'] == 'None':
        return None
    else:
        return User(recieved_json['username'], recieved_json['auth_key'])
    # recv_json = tcp.recv(1024).decode()

def sign_up(tcp):
    print("##### CADASTRO DE USUÁRIO #####")
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

def add_bills(tcp, auth_user):
    sended_json = json.dumps({'command': 'add_bills', 'username': auth_user.username, 'auth_key': auth_user.auth_key})
    tcp.send(sended_json.encode())
    add_bills = tcp.recv(1024).decode()
    if add_bills == 'ERRO 401':
        return None
    else:
        print("##### CADASTRO DE CONTA #####")
        payment = input("Digite o valor da conta: ")
        due_date = input("Digite a data de vencimento: ")
        cpf = input("Digite o CPF do cliente: ")
        sended_json = json.dumps({'command': 'add_bills', 'payment': payment, 'due_date': due_date, 'employee_username': auth_user.username, 'cpf': cpf})
        tcp.send(sended_json.encode())
        return tcp.recv(1024).decode()


def list_bills(tcp, auth_user):
    sended_json = json.dumps({'command': 'list_bills', 'username': auth_user.username, 'auth_key': auth_user.auth_key})
    tcp.send(sended_json.encode())

    list_of_bills = tcp.recv(1024).decode()

    if list_of_bills == 'ERRO 401':
        return None
    else:
        list_of_bills = json.loads(list_of_bills)

        for i in range(len(list_of_bills['id'])):
            print("Id: ", list_of_bills['id'][i])
            print("Pagamento: ", list_of_bills['pagamento'][i])
            print("Data de cadastro: ", list_of_bills['cadastro'][i])
            print("Data de vencimento: ", list_of_bills['id'][i])
        return auth_user
    
def list_unchecked_payments(tcp, auth_user):
    sended_json = json.dumps({'command': 'list_unchecked_payments', 'username': auth_user.username, 'auth_key': auth_user.auth_key})
    tcp.send(sended_json.encode())

    list_of_bills = tcp.recv(1024).decode()

    if list_of_bills == 'ERRO 401':
        return None
    else:
        list_of_bills = json.loads(list_of_bills)

        for i in range(len(list_of_bills['id'])):
            print("Id: ", list_of_bills['id'][i])
            print("Pagamento: ", list_of_bills['pagamento'][i])
            print("Data de cadastro: ", list_of_bills['cadastro'][i])
            print("Data de vencimento: ", list_of_bills['id'][i])
        return auth_user
    
def del_bills(tcp, auth_user):
    sended_json = json.dumps({'command': 'del_bills', 'username': auth_user.username, 'auth_key': auth_user.auth_key})
    tcp.send(sended_json.encode())
    del_bills = tcp.recv(1024).decode()
    if del_bills == 'ERRO 401':
        return None
    else:
        list_bills(tcp, auth_user)
        print("##### EXCLUSAO DE CONTA #####")
        conta_id = input("Digite o ID da conta: ")
        sended_json = json.dumps({'command': 'del_bills', 'conta_id': conta_id})
        tcp.send(sended_json.encode())
        return tcp.recv(1024).decode()

def auth_bills(tcp, auth_user):
    sended_json = json.dumps({'command': 'auth_bills', 'username': auth_user.username, 'auth_key': auth_user.auth_key})
    tcp.send(sended_json.encode())
    auth_bills = tcp.recv(1024).decode()
    if auth_bills == 'ERRO 401':
        return None
    else:
        print("##### CONFIRMACAO DE PAGAMENTO #####")
        conta_token = input("Digite o Token da conta: ")
        sended_json = json.dumps({'command': 'del_bills', 'conta_token': conta_token})
        tcp.send(sended_json.encode())
        return tcp.recv(1024).decode()

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
        switch(choice):
            case 1:
                auth_user = login_user(tcp)
                if auth_user is not None:
                    print(auth_user.username)
                else:
                    print('Erro!')
                    break
            case 2:
                print(sign_up(tcp))
                break
            
            
    else:
        print("Usuário logado")
        print("Nome: ", auth_user.username)
        choice = int(input("""Escolha as opções a seguir:\n1 - adicionar contas;\n2 - remover contas;\n3 - Listar contas;\n4 - Listar contas abertas;\n"""))
        if choice == 1:
            auth_user = add_bills(tcp, auth_user)
        elif choice == 2:
            auth_user = del_bills(tcp, auth_user)
        elif choice == 3:
            auth_user = list_bills(tcp, auth_user)
        elif choice == 4:
            auth_user = list_unchecked_payments(tcp, auth_user)
        elif choice == 5:
            auth_user = auth_bills(tcp, auth_user) 


        
tcp.close() #encerra o cliente
