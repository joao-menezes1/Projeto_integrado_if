import socket
import threading
from hashtable import *
from lista_circular import *
from jogo import Jogo
import sys
import time

class Server():
    
    ''' Classe Server

        A classe Server é responsável por gerenciar as salas do jogo e contralar a entrada em regiões crítica. Ela possui os seguintes atributos:

        salas: uma Hashtable encadeada que armazena a como chave a sala criada pelo usuário e valor o socket correspondente ao usúario.
        nickname_list: uma Hashtable encadeada que armazena a como chave o socket do usuário e  o valor é o nick escolhido pelo jogador.
        salas: uma Hashtable encadeada que serve como uma cópia da hashtable de salas, mas ela só adiciona os jogadores se eles estiveream prontos para iniciar a partida, permitindo que o jogo da sala só inicie se todos os cliente derem permissão.
        respectivos semaphoros para tratar cada estrutura de dados.
        semaphore_salas: Semaphore para controle de acesso às salas.
        Semaphore_nickname: Semaphore para controle de acesso à lista de nicknames.
        semaphore_jogadores_prontos: Semaphore para controle de acesso à lista de jogadores prontos.

        Métodos:
        - iniciar_servidor(HOST, PORT): Inicia o servidor, aguardando conexões.
        - comunicacao_cliente(cliente_socket, cliente_address): Gerencia a comunicação com o cliente.
        - comandos(cliente_socket): Processa comandos recebidos do cliente.
        - nickname(cliente_socket, nickname): Associa o nickname ao cliente.
        - jogador_pronto(cliente_socket, sala): Gerencia o status do jogador, indicando prontidão para iniciar o jogo.
        - iniciar_jogo_todos_prontos(sala): Verifica se todos os jogadores de uma sala estão prontos para iniciar o jogo.
        - jogo(lista_jogadores, chave): Inicia o jogo para a lista de jogadores em uma sala específica.
        - __enviar_msg_cliente(mensagem, cliente_socket): Envia mensagem para um cliente específico.
        - __receber_msg_cliente(cliente_socket): Recebe mensagem de um cliente específico.
        - __enviar_msg_cliente_broadcast(mensagem, lista_jogadores): Envia mensagem para uma lista de clientes.
        - mostrar_salas_disponiveis(): Mostra as salas disponíveis.
        - __criar_sala(cliente_socket, nome_sala): Cria uma nova sala.
        - __entrar_na_sala(sala, cliente_socket): Permite um cliente entrar em uma sala existente.
    '''
    
    def __init__(self):
        
        '''  __init__(self)
        Objetivo: Método construtor da classe Server.
        Parâmetros de Entrada: self (referência à própria instância).
        Descrição: Inicializa os semáforos para controlar o acesso a diferentes partes críticas do servidor (semaphore_salas, semaphore_nickname, semaphore_jogadores_prontos). Também inicializa três estruturas de dados (Hashtable) para armazenar salas, nicknames e jogadores prontos. '''
        
        self.semaphore_salas = threading.Semaphore(1)
        self.semaphore_nickname = threading.Semaphore(1)
        self.semaphore_jogadores_prontos = threading.Semaphore(1)
        self.salas = HashTable()
        self.nickname_list = HashTable()
        self.jogadores_prontos = HashTable()

    def iniciar_servidor(self, HOST, PORT):
        
        '''  iniciar_servidor(self, HOST, PORT)
        Objetivo: Inicia o servidor para escutar conexões de clientes.
        Parâmetros de Entrada: self (referência à própria instância), HOST (string: endereço IP do servidor), PORT (int: número da porta).
        Descrição: Configura um socket de escuta para aguardar conexões de clientes. O método aceita as conexões dos clientes e inicia threads para lidar com cada cliente conectado. '''
        
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            orig = (HOST, PORT)

            server.bind(orig)
            server.listen()

            print("Aguardando conexões...")

            while True:
                cliente_socket, cliente_address = server.accept()
                cliente_thread = threading.Thread(target=self.comunicacao_cliente, args=(cliente_socket, cliente_address))
                cliente_thread.start()
        except OSError as e:
            print(f"Erro ao iniciar o servidor: {e}")
            sys.exit(1)
    

    def comunicacao_cliente(self, cliente_socket, cliente_address):
        
        ''' comunicacao_cliente(self, cliente_socket, cliente_address)
        Objetivo: Lida com a comunicação com o cliente.
        Parâmetros de Entrada: self (referência à própria instância), cliente_socket (socket do cliente), cliente_address (endereço IP e porta do cliente).
        Descrição: Gerencia a comunicação entre o servidor e um cliente específico, chamando o método comandos para interpretar e executar os comandos enviados pelo cliente.'''
        
        print(f"Cliente conectado: {cliente_address}")
        self.comandos(cliente_socket)
    
    def comandos(self, cliente_socket):
        
        ''' comandos(self, cliente_socket)
        Objetivo: Interpreta e executa os comandos recebidos do cliente.
        Parâmetros de Entrada: self (referência à própria instância), cliente_socket (socket do cliente).
        Descrição: Recebe comandos do cliente, os interpreta e os direciona para os métodos correspondentes, como nickname, entrar_na_sala, jogador_pronto, criar_sala, ou salas_disponiveis. '''
        
        while True:
            comando = self.__receber_msg_cliente(cliente_socket)
            if ',' in comando:
                comando = comando.split(',')
                if comando[0] == 'nickname':
                    self.nickname(cliente_socket, comando[1])
                    continue
                elif comando[0] == 'entrar_na_sala':
                    entrar = self.__entrar_na_sala(comando[1], cliente_socket)
                    self.__enviar_msg_cliente(entrar, cliente_socket)
                    continue

                elif comando[0] == 'jogador_pronto':
                    for chave, valor in self.salas.items():
                        for socket in valor:
                            if socket == cliente_socket:
                                resp = self.jogador_pronto(cliente_socket, chave)
                                if resp == '200':
                                    self.__enviar_msg_cliente(resp, cliente_socket)
                                else:
                                    self.__enviar_msg_cliente('200', cliente_socket)
                                    self.jogo(resp, chave)
                                        
                    break
                                
                
                elif comando[0] == 'criar_sala':
                    nome_sala = comando[1]
                    resp = self.__criar_sala(cliente_socket, nome_sala)
                    self.__enviar_msg_cliente(f"{resp}", cliente_socket)
                    continue
                    

            else:
                if comando == 'salas_disponiveis':
                    resp = self.mostrar_salas_disponiveis()
                    self.__enviar_msg_cliente(resp, cliente_socket)
                    continue


    def nickname(self, cliente_socket, nickname):
        
        ''' nickname(self, cliente_socket, nickname)
        Objetivo: Armazena o nickname associado a um cliente.
        Parâmetros de Entrada: self (referência à própria instância), cliente_socket (socket do cliente), nickname (string: nickname escolhido pelo cliente).
        Descrição: Armazena o nickname escolhido pelo cliente em uma Hashtable, associando-o ao socket correspondente.'''
        
        self.semaphore_nickname.acquire()
        self.nickname_list.put(cliente_socket, nickname)
        self.semaphore_nickname.release()
    
    def jogador_pronto(self, cliente_socket, sala):
        
        ''' jogador_pronto(self, cliente_socket, sala)
    Objetivo: Indica que um jogador está pronto para iniciar um jogo em uma sala específica.
    Parâmetros de Entrada: self (referência à própria instância), cliente_socket (socket do cliente), sala (string: nome da sala).
    Descrição: Marca o jogador como pronto para iniciar o jogo na sala específica, armazenando os jogadores prontos NA HASHTABLE '''
        
        self.semaphore_jogadores_prontos.acquire()
        lista = self.salas.get(f'{sala}')
        chaves = self.jogadores_prontos.keys()
        if (f'{sala}') in chaves:
            lista = self.jogadores_prontos.get(f'{sala}')
            lista.append(cliente_socket)
            self.jogadores_prontos.put(f'{sala}', lista)
            self.semaphore_jogadores_prontos.release()
            rsp = self.iniciar_jogo_todos_prontos(sala)
            if rsp == '200ok':
                return lista
            else:
                return '200'
        else:
            self.jogadores_prontos.put(f'{sala}', [cliente_socket])
            self.semaphore_jogadores_prontos.release()
            return '200'

    def iniciar_jogo_todos_prontos(self, sala):
        
        ''' iniciar_jogo_todos_prontos(self, sala)
        Objetivo: Verifica se todos os jogadores em uma sala estão prontos para iniciar o jogo.
        Parâmetros de Entrada: self (referência à própria instância), sala (string: nome da sala).
        Descrição: Verifica se o número de jogadores prontos na sala atingiu o número necessário para iniciar o jogo.'''
        
        while True:
            if len(self.jogadores_prontos.get(f'{sala}')) == 3:
                return '200ok'
            else: return '200'
    

    def jogo(self, lista_jogadores, chave):
        
        ''' Objetivo: Inicia o jogo para uma lista de jogadores em uma sala específica.
        Parâmetros de Entrada: self (referência à própria instância), lista_jogadores (lista de sockets de jogadores), chave (string: chave para identificar a sala).
        Descrição: Inicia o jogo para os jogadores da lista especificada na sala correspondente e remove a sala das estruturas de dados após o jogo ser iniciado.'''
        
        jogo = Jogo()
        parametro, ganhador = jogo._iniciar_jogo(lista_jogadores)
        if parametro == 'Jogo_encerrado' and ganhador != 'nenhum':
            nick_ganhador = self.nickname_list.get(ganhador)
            self.__enviar_msg_cliente_broadcast(f'\nO jogador {nick_ganhador} acertou a palavra.', lista_jogadores)
            time.sleep(2)
            self.__enviar_msg_cliente_broadcast("Jogo encerrado", lista_jogadores)
            self.semaphore_salas.acquire()
            self.salas.remove(chave)
            self.semaphore_salas.release()
            self.semaphore_jogadores_prontos.acquire()
            self.jogadores_prontos.remove(chave)
            self.semaphore_jogadores_prontos.release()
        else:
            self.__enviar_msg_cliente_broadcast(f'\nVocê perdeu! A palavra era "..."', lista_jogadores)
            time.sleep(2)
            self.__enviar_msg_cliente_broadcast("Jogo encerrado", lista_jogadores)
            self.semaphore_salas.acquire()
            self.salas.remove(chave)
            self.semaphore_salas.release()
            self.semaphore_jogadores_prontos.acquire()
            self.jogadores_prontos.remove(chave)
            self.semaphore_jogadores_prontos.release()
            
        
    
    def __enviar_msg_cliente(self, mensagem, cliente_socket):
        
        ''' __enviar_msg_cliente(self, mensagem, cliente_socket)
        Objetivo: Envia uma mensagem para um cliente específico.
        Parâmetros de Entrada: self (referência à própria instância), mensagem (string: mensagem a ser enviada), cliente_socket (socket do cliente).
        Descrição: Envia a mensagem fornecida para o cliente correspondente usando o socket.'''
        
        cliente_socket.send(mensagem.encode('utf8'))

    def __receber_msg_cliente(self, cliente_socket):
        
        ''' __receber_msg_cliente(self, cliente_socket)
        Objetivo: Recebe uma mensagem do cliente.
        Parâmetros de Entrada: self (referência à própria instância), cliente_socket (socket do cliente).
        Descrição: Recebe e decodifica uma mensagem enviada pelo cliente usando o socket especificado. '''
        
        msg = cliente_socket.recv(1024).decode('utf8')
        return msg
    
    def __enviar_msg_cliente_broadcast(self, mensagem, lista_jogadores):
        
        ''' __enviar_msg_cliente_broadcast(self, mensagem, lista_jogadores)
        Objetivo: Envia uma mensagem para todos os jogadores em uma lista.
        Parâmetros de Entrada: self (referência à própria instância), mensagem (string: mensagem a ser enviada), lista_jogadores (lista de sockets dos jogadores).
        Descrição: Envia a mensagem fornecida para todos os jogadores na lista usando seus respectivos sockets.'''
        
        for cliente in lista_jogadores:
            self.__enviar_msg_cliente(mensagem, cliente)
    

    def mostrar_salas_disponiveis(self):
        
        ''' mostrar_salas_disponiveis(self)
        Objetivo: Mostra as salas disponíveis para os clientes.
        Parâmetros de Entrada: self (referência à própria instância).
        Descrição: Retorna uma string contendo a lista das salas disponíveis para os clientes.'''
        
        self.semaphore_salas.acquire()
        salas = self.salas.keys()
        self.semaphore_salas.release()
        if len(salas) == 0:
            return "404"
        else:
            salas_str = ''
            for sala in salas:
                salas_str += (f'-  {sala}\n')
            return salas_str

    def __criar_sala(self, cliente_socket, nome_sala):
        
        ''' __criar_sala(self, cliente_socket, nome_sala)
        Objetivo: Cria uma nova sala e adiciona um cliente a ela.
        Parâmetros de Entrada: self (referência à própria instância), cliente_socket (socket do cliente), nome_sala (string: nome da sala).
        Descrição: Cria uma nova sala com o nome fornecido e adiciona o cliente à sala usando seu socket.'''
        
        self.semaphore_salas.acquire()
        if nome_sala in self.salas.keys():
            self.semaphore_salas.release()
            return '402'
        self.salas.put(nome_sala, [cliente_socket])
        self.semaphore_salas.release()
        return '200'
    
    def __entrar_na_sala(self, sala, cliente_socket):
        
        ''' __entrar_na_sala(self, sala, cliente_socket)
        Objetivo: Permite que um cliente entre em uma sala existente.
        Parâmetros de Entrada: self (referência à própria instância), sala (string: nome da sala), cliente_socket (socket do cliente).
        Descrição: Permite que um cliente entre em uma sala existente se houver espaço disponível. '''
        
        self.semaphore_salas.acquire()
        chaves = self.salas.keys()
        if sala in chaves:
            lista = self.salas.get(f'{sala}')
            if len(lista) < 3:    
                lista.append(cliente_socket)
                self.salas.put(f'{sala}', lista)
                self.semaphore_salas.release()
                return '200'
            else:
                self.semaphore_salas.release()
                return '404'
        else:
            self.semaphore_salas.release() 
            return '401'

if len(sys.argv) != 3:
        print("Uso: python seu_script.py HOST PORT")
        sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

server = Server()
server.iniciar_servidor(host, port)