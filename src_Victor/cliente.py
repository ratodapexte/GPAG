import socket
import json

class User():
    def __init__(self, username, auth_key, ):
        self.username = username
        self.auth_key = auth_key
    
    def set_admin(self, admin):
        self.admin = admin
    
    def set_employee(self, employee):
        self.employee = employee
    
    def get_admin(self):
        return self.admin
    
    def get_employee(self):
        return self.employee

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
        auth_user = User(recieved_json['username'], recieved_json['auth_key'])
        auth_user.set_admin(recieved_json['adm'])
        auth_user.set_employee(recieved_json['employee'])
        return auth_user
    # recv_json = tcp.recv(1024).decode()

def sign_up(tcp, auth_user):
    print("##### CADASTRO DE USUÁRIO #####")
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha do usuário: ")
    name = input("Digite o nome: ")
    cpf = input("Digite o cpf: ")
    email = input("Digite o seu email: ")
    phone = input("Digite o seu telefone: ")    

    if auth_user.get_admin() is True:
        adm_status = str(input("Usuário terá previlégios de adm?(S(sim))\n"))
        if adm_status == 'S' or adm_status == 'sim':
            adm_status = True
        else:
            adm_status = False
        employee_status = str(input("Usuário terá previlégios de empregado?(S(sim))\n"))
        if employee_status == 'S' or adm_status == 'sim':
            employee_status = True
        else:
            employee_status = False
    elif auth_user.get_employee() is True:
        adm_status = False
        employee_status = False
    sended_json = json.dumps({'command': 'sign_up', 'auth_name': auth_user.username, 'auth_key': auth_user.auth_key,
                        'adm': auth_user.get_admin(), 'employee': auth_user.get_employee(),
                        'username': username, 'password': password, 'name': name, 'cpf': cpf, 'email': email, 
                        'phone': phone, 'adm_status': adm_status, 'employee_status': employee_status})
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
    print("##### CADASTRO DE CONTA #####")
    payment = input("Digite o valor da conta: ")
    due_date = input("Digite a data de vencimento: ")
    cpf = input("Digite o CPF do cliente: ")
    sended_json = json.dumps({'command': 'add_bills', 'payment': payment, 'due_date': due_date, 'cpf': cpf,
                            'username': auth_user.username, 'auth_key': auth_user.auth_key })
    tcp.send(sended_json.encode())
    result = tcp.recv(1024).decode()

    if result == 'INSERTED':
        print("Conta inserida no cpf de numero ", cpf)
        return auth_user
    elif result == 'ERRO 401!':
        return None
    else:
        print("Usuário proibido de realizar a ação!")
        return auth_user

def list_bills(tcp, auth_user):
    sended_json = json.dumps({'command': 'list_bills', 'username': auth_user.username, 'auth_key': auth_user.auth_key})
    tcp.send(sended_json.encode())

    list_of_bills = tcp.recv(1024).decode()

    if list_of_bills == 'ERRO 401':
        return None
    elif list_of_bills ==  'ERRO 404':
        print("Nenhuma conta encontrada!")
        return auth_user
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
    elif list_of_bills == 'ERRO 404':
       print("Nenhuma conta foi encontrada!")
       return auth_user
    else:
        list_of_bills = json.loads(list_of_bills)

        for i in range(len(list_of_bills['id'])):
            print("Id: ", list_of_bills['id'][i])
            print("Pagamento: ", list_of_bills['pagamento'][i])
            print("Data de cadastro: ", list_of_bills['cadastro'][i])
            print("Data de vencimento: ", list_of_bills['vencimento'][i])
        return auth_user
    
def del_bills(tcp, auth_user):
    sended_json = json.dumps({'command': 'list_all_bills'})
    tcp.send(sended_json.encode())
    list_of_bills = json.loads(tcp.recv(1024).decode())

    print("##### Lista das contas #####")
    for i in range(len(list_of_bills['id'])):
        print("Id: ", list_of_bills['id'][i])
        print("Pagamento: ", list_of_bills['pagamento'][i])
        print("Data de vencimento: ", list_of_bills['vencimento'][i])

    print("\n\nDigite o id da conta: ")
    bill_id = int(input())

    tcp.send(json.dumps({'command': 'del_bills', 'username': auth_user.username, 
                            'auth_key': auth_user.auth_key, 'id':  bill_id}))
    result = tcp.recv(1024).decode()

    if result == 'ERRO 401':
        return None
    elif result == 'ERRO 404':
        print("Conta não encontrada!")
        return auth_user
    else
        print('Conta deletada!')
        return auth_user


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

host = 'localhost'  #ip do servidor
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
        auth_user = login_user(tcp)
    else:
        print("Usuário logado")
        print("Nome: ", auth_user.username)
        if auth_user.get_admin() is True or auth_user.get_employee() is True:
            choice = int(input("""Escolha as opções a seguir: \n1 - adicionar contas;\n2 - remover contas;\n3 - Listar contas;\n4 - Listar contas abertas;\n Escolha: """))
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
            elif choice == 6:
                print(sign_up(tcp, auth_user))
            else:
                print("Opção errada!")
        else:
            choice = int(input("""Escolha as opções a seguir: \n1 - Listar contas;\n2 - Listar contas abertas;\n3 - Entrar código de pagamento;\nEscolha: """))
            if choice == 1:
                auth_user = list_bills(tcp, auth_user)
            elif choice == 2:
                auth_user = list_unchecked_payments(tcp, auth_user)
            elif choice == 3:
                auth_user = auth_bills(tcp, auth_user) 
            else:
                print("Opção errada!")


        
tcp.close() #encerra o cliente






