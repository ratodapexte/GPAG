from models import Cliente


def cadastrar_cliente(tcp):
    nome = tcp.sendinput('Digite o nome do cliente: ')
    login = input('Digite o login: ')
    senha = input('Digite a senha: ')
    cpf = input('Digite o cpf: ')
    email = input('Digite o email: ')

    print('Cliente cadastrado!')

    return Cliente(nome, login, senha, cpf, email)

