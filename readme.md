# Aplicação
## Função
Gerenciador de pagamento de contas, onde existem 2 tipos de perfil: adm e cliente. 

 - Amd: pode adicionar contas e clientes, bem como visualizar as contas e declarar como pagas.
 - Cliente: visualizar suas contas ou tentar comprovar um pagamento.

## Rodando aplicação
### Banco de dados

 - Postegres foi o banco de dados utilizado.
 - Modelo do banco de dados se encontra no arquivo **bdscript.sql**.
 - Variáveis de conexão se encontram no arquivo **database.ini.exemplo**. Para utilizá-lo basta renomear para **database.ini** e alterar as informações para as do banco de dados que a aplicação vai se comunicar.

  ```
[postgresql]
host=localhost //ip de onde o banco de dados se encontra 
database=[nomeDoBanco] // nome do banco de dados para a aplicação
user=[nomeDoUsuario] // usuário que irá logar no banco
password=[senhaDoUsuario] // senha do usuário
```
### Codificação
Python foi a linguagem utilizada.

 - **cliente.py:** executar para rodar a aplicação a nível de cliente.
 - **servidor.py:** executar para rodar a aplicação a nível de servidor.
