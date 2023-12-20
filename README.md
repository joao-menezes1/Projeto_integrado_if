# Projeto-Integrado
    jogo da forca 
    
    
    Servidor de Jogo Multiplayer


Este projeto implementa um servidor para um jogo multiplayer utilizando sockets em Python. O servidor gerencia as salas, a entrada dos jogadores nelas e inicia os jogos quando todos estão prontos.

Funcionalidades:

Criação e Entrada em Salas: Os clientes podem criar novas salas e entrar em salas existentes, desde que haja vagas disponíveis.
Apelidos Personalizados: Os jogadores podem escolher apelidos para serem identificados nas salas e nos jogos.
Início de Jogo Assíncrono: O servidor aguarda todos os jogadores estarem prontos antes de iniciar um jogo.
Estrutura do Projeto:
    Arquivos
    server.py: Implementação do servidor que controla as conexões e comunicação com os clientes.
    hashtable.py: Implementação de uma hashtable encadeada para gerenciamento de salas e nicknames.
    lista_circular.py: Implementação de uma lista circular.
    jogo.py: Implementação da lógica do jogo.

Dependências:
    Python 3.x
    Biblioteca socket
    Biblioteca threading

Como Usar:
Execute o servidor:
    python server.py HOST PORT

Execute o cliente:
    python cliente.py HOST PORT
    
Substitua HOST pelo endereço IP do servidor e PORT pela porta desejada.

Conecte-se ao servidor utilizando um cliente adequado.

Como Contribuir
Sinta-se à vontade para contribuir com sugestões, reportar bugs ou melhorar este projeto através de pull requests.

Autores

João Vittor Pereira Menezes
Kauã Victor Gomes Paiva


