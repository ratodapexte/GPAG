import socket

host = ''       #ip ao qual ele vai se vincular
port = 20000    #porta que ele vai usar

serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #internet e TCP
origin = (host,port)
serversocket.bind(origin) #se linka ao IP e à porta
serversocket.listen(1) #entra em modo de espera
msg = 'Servidor iniciado'
print(msg)
while msg != 'sair':
    client, adress = serversocket.accept() #recebe o cliente e suas configurações em client, e o IP do cliente em adress
    print("conectado a ", adress)
    while msg != 'sair':
        msg = client.recv(1024).decode() #recebe mensagem do cliente e transforma de byte-type pra str (decode)
        print(adress,": ", msg)
    print("Conexao com ", adress, " finalizada.")
print("Servidor finalizado")
