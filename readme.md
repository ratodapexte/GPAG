Como rodar a aplicação:
    Banco de dados    
cliente.py - o cliente que irá fazer a conexão com o servidor e fazer as solicitações. a configuração já está pré estabelecida para se conectar com o servidor (IP: 83.136.219.66). Basta rodar esse arquivo para ver a aplicação funcionando. Caso queira rodar o servidor localmente, será necessário mudar o host do cliente.py para localhost.

config.py - arquivo que pega as informações de database.ini para iniciar a conexão com o banco de dados postgresql. Uma cópia deste arquivo se encontra sendo executada no servidor. Não há necessidade de alteração deste arquivo

database.ini.exemplo - arquivo que conecta com o postgresql. caso queira rodar o servidor localmente, será necessário criar um banco de dados local e uma conexão com o mesmo. basta alterar neste arquivo o nome do seu banco e seu usuário e senha do postgresql. Uma cópia deste arquivo se encontra sendo executada no servidor.

reused_code.py - contém funções que serão constantemente utilizadas para que o servidor possa acessar o banco. este arquivo está utilizando uma biblioteca python externa chamada psycopg2 para executar os comandos sql. caso queira rodar o servidor localmente, será necessário instalar essa biblioteca com o comando 'pip install psycopg2'. Uma cópia deste arquivo se encontra sendo executada no servidor.

servidor.py - arquivo de servidor que receberá a conexão através de socket e irá montar a thread e executar as funções solicitadas pelo cliente. Uma cópia deste arquivo se encontra sendo executada no servidor.  Não há necessidade de alteração deste arquivo

bdscript.sql - arquivo que contém o comando sql utilizado para a criação do banco de dados em postgresql. caso queira rodar o servidor localmente, será necessário utilizar esse script para criar o banco de dados na máquina, bem realizar um insert de algum perfil para poder realizar o login.

Estamos cientes de que existem várias falhas no programa, incluindo questões de segurança. Mas como fazemos estágio e não estamos de férias dele, o tempo para programar se mostrou curto e tivemos que abrir mão de alguns detalhes e focar mais nas funcionalidades principais. Estamos abertos a quaisquer sugestões e críticas, não somente da parte que vale nota, mas do projeto como um todo, pois pretendemos prosseguir com a implementação deste sistema para conseguir a experiência de ter o primeiro projeto feito que seja completamente utilizável por qualquer pessoa.

Qualquer dúvida estamos à disposição.
Área de anexos
