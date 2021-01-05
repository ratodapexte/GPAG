import socket
import secrets
import json
import threading
from reused_code import *

def login_user(dict):
    print("Dados recebidos: ", dict)
    querry = querry_one("""SELECT username, adm, employee FROM users WHERE username = %s AND password = %s""",
            dict['username'], dict['password'])
    if querry is None:
        return json.dumps({'username': 'None', 'auth_key': 'None'}).encode()
    else:
        auth_key = secrets.token_hex()
        auth_key_init_datetime = datetime.now()
        result = {'username': querry[0], 'adm': querry[1], 'employee': [2], 'auth_key': auth_key}
        commit_querry("""UPDATE users SET auth_key = %s, auth_key_init_datetime = %s 
                        WHERE username = %s AND password = %s""",
        auth_key, auth_key_init_datetime, result['username'], dict['password'])

        return json.dumps(result).encode() 


def sign_up(dict):
    print("Dados recebidos: ", dict)
    if authenticate_user(dict['auth_name'], dict['auth_key']) is True:
        level = querry_one("SELECT adm, employee FROM users WHERE username = %s", dict['auth_name'])
        if level[0] is True:
            status = commit_querry("""INSERT INTO users (username, password, name, cpf, email, phone, adm, employee)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", 
                        dict['username'], dict['password'], dict['name'], dict['cpf'], dict['email'], dict['phone'],
                        dict['adm_status'], dict['employee_status'])
        elif level[1] is True:
            status = commit_querry("""INSERT INTO users (username, password, name, cpf, email, phone, employee)
                        VALUES (%s,%s,%s,%s,%s,%s)""", 
                        dict['username'], dict['password'], dict['name'], dict['cpf'], dict['email'], dict['phone'], dict['employee_status'])    
        else:
            return "ERRO 403".encode()
        return status.encode()
    else:
        return 'ERRO 401!'.encode()


def list_bills(dict):
    if authenticate_user(dict['username'], dict['auth_key']) is True:
        user_id = querry_one(
            """SELECT id FROM users WHERE users.username = %s""", dict['username'])
        list_of_bills = querry_all("""SELECT id, payment, registration_date, due_date FROM bills b WHERE b.fk_user_id = %s""", user_id)

        bills_dict = {'id': [], 'pagamento': [], 'cadastro': [], 'vencimento': []}
        for bill in list_of_bills:
            bills_dict['id'].append(str(bill[0]))
            bills_dict['pagamento'].append(str(bill[1]))
            bills_dict['cadastro'].append(str(bill[2]))
            bills_dict['vencimento'].append(str(bill[3]))
        if list_of_bills is None:
            return "ERRO 404"
        return json.dumps(bills_dict).encode()
    else:
        return "ERRO 401".encode()

def list_unchecked_payments(dict):
    if authenticate_user(dict['username'], dict['auth_key']) is True:
        user_id = querry_one("""SELECT id FROM users WHERE users.username = %s""", dict['username'])
        list_of_bills = querry_all("""SELECT id, payment, registration_date, due_date FROM bills b WHERE b.fk_user_id = %s and validated = 'f'""", user_id)
        if list_of_bills is None:
            return "ERRO 404".encode()
        bills_dict = {'id': [], 'pagamento': [], 'cadastro': [], 'vencimento': []}
        for bill in list_of_bills:
            bills_dict['id'].append(str(bill[0]))
            bills_dict['pagamento'].append(str(bill[1]))
            bills_dict['cadastro'].append(str(bill[2]))
            bills_dict['vencimento'].append(str(bill[3]))

        return json.dumps(bills_dict).encode() 
    else:
        return "ERRO 401".encode()
    

def add_bills(dict):
    if authenticate_user(dict['username'], dict['auth_key']) is True:
        adm, emp = querry_one("SELECT adm, employee FROM users WHERE username = %s", dict['username'])
        print("adm: ",adm, ", employee: ",emp)
        if adm is True or emp is True:
            print("##### ADICIONANDO CONTA #####")
            print("Dados recebidos: ", dict)
            user_id = querry_one("""SELECT id FROM users WHERE users.cpf = %s""", dict['cpf'])
            if user_id is None:
                return 'ERRO 404'.encode()
            fk_employee_id = querry_one("""SELECT id FROM users WHERE users.username = %s""", dict['username'])
            status = commit_querry("""INSERT INTO bills (payment, due_date, fk_employee_id, fk_user_id) 
            VALUES (%s,%s,%s,%s)""", dict['payment'], dict['due_date'], fk_employee_id, user_id)
            return "INSERTED".encode()
        return "ERRO 403!".encode()
    return "ERRO 401!".encode()

def list_all_bills(dict):
    all_bills = querry_all("""SELECT id, payment, fk_user_id FROM bills""")
    if all_bills is None:
        return "ERRO 404".encode()
    bills_dict = {'id': [], 'pagamento': [], 'vencimento': []}
    for bill in all_bills:
            bills_dict['id'].append(str(bill[0]))
            bills_dict['pagamento'].append(str(bill[1]))
            bills_dict['vencimento'].append(str(bill[2]))

    return json.dumps(bills_dict).encode()

def del_bills(dict):
    if authenticate_user(dict['username'], dict['auth_key']) is True:
            level = querry_one("SELECT adm, employee FROM users WHERE username = %s", dict['username'])
            if level[0] is True or level[1] is True:
                print("Dados recebidos: ", dict)
                commit_querry("""DELETE FROM bills WHERE id = %s""", dict['id'])
                return "DELETED".encode()
            return "ERRO 403!".encode()
    return "ERRO 401!".encode()

def auth_bills(dict):
    if authenticate_user(dict['username'], dict['auth_key']) is True:
        print("Dados recebidos: ", dict)
        status = commit_querry("""UPDATE bills SET validated = 't', payment_authentication_key = %s WHERE id = %s""", dict['auth_token'],
                                dict['id'])
        if status == "UPDATE 1":
            return "Conta verificada".encode()
        else:
            return 'ERRO 404'.encode()
    else:
        return "ERRO 401".encode()
    
def main(con, cliente):
    while True:
        while True:
            msg = con.recv(1024).decode('utf-8')
            if not msg:
                break
            recv_json = json.loads(msg)
            print("Comando: ", recv_json['command'])
            con.send(globals()[recv_json['command']](recv_json))
        print('Finalizando conexao do cliente ', cliente)
        con.close()



HOST = 'localhost'
PORT = 30000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    print ('Conectado por: ', cliente)
    t = threading.Thread(target=main, args=(tuple([con, cliente])))
    t.start()

tcp.close()
    
##############################################################################
'''                              AUTENTICACAO
    RECEBE CHAVE E USUÁRIO
    BUSCA O TEMPO EM QUE A CHAVE DO USUÁRIO FOI AUTENTICADO PELA ULTIMA VEZ
    CASO A DIFERENÇA SEJA MAIOR QUE X O BANCO VAI APAGAR A SUA CHAVE DE AUTENTICACAO
'''
##############################################################################
