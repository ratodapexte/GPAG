import socket

host = '127.0.0.1'  #ip do servidor
port = 20000        #porta que o servidor vai usar pra trocar informações

tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #AF_INET é usar a internet, SOCK_STREAM é TCP
server = (host,port) #tupla
tcp.connect(server) #conecta o servidor

print("Conectado ao servidor ", host)
print("Para sair digite 'sair'")
msg = "Digite sua mensagem:"
print(msg)

while msg != 'sair':
    msg = input()
    tcp.send(msg.encode()) #envia mensagem para o servidor em byte-type (encode)

tcp.close() #encerra o cliente
