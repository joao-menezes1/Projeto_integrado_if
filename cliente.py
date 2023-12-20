import socket
import threading
import sys

class Cliente:
    
    ''' A classe Cliente é a classe principal do cliente. Ela contém todos os métodos e atributos necessários para conectar o cliente ao servidor e jogar o jogo.

    Os métodos mais importantes da classe Cliente são:

    iniciar_cliente(host, port): Conecta o cliente ao servidor.
    __receber_mensagens_servidor(): Recebe uma mensagem do servidor.
    __request(objeto_desejado): Envia uma mensagem ao servidor.
    menu_jogo(): Exibe o menu principal do jogo.
    menu_salas(): Exibe o menu de salas disponíveis.
    __nickname(): Solicita o nome do jogador.
    menu_jogo_chutes(): Exibe o menu de chutes do jogo.
    escolher_tema(): Solicita o tema do jogo.
    loop_para_iniciar_jogo(nickname, sala): Inicia o jogo na sala especificada.'''
    
    
    def __init__(self):
        self.cliente = None

    def iniciar_cliente(self, HOST, PORT):
        
        ''' Método iniciar_cliente(self, HOST, PORT)

        Este método inicializa o cliente, conectando-o ao servidor. Ele recebe os seguintes parâmetros:

        HOST: O endereço IP do servidor.
        PORT: A porta do servidor.
        Este método faz o seguinte:

        Cria uma conexão TCP com o servidor.'''
        
        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((HOST, PORT))
            self.iniciar_jogo()
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar ao servidor. Verifique o HOST e PORT e tente novamente.")
            sys.exit(1)
        except ValueError:
            print("Erro: O valor do PORT deve ser um número inteiro.")
            sys.exit(1)

    def __receber_mensagens_servidor(self):
        
        ''' Método receber_mensagens_servidor(self)

        Este método recebe uma mensagem do servidor. Ele não recebe parâmetros.

        Este método faz o seguinte:

        Recebe uma mensagem do servidor.
        Decodifica a mensagem de bytes para string.
        Retorna a mensagem.'''
        
        msg_servidor = self.cliente.recv(1024).decode('utf8')
        return msg_servidor

    def __request(self, objeto_desejado):
        
        ''' Método request(self, objeto_desejado)

        Este método envia uma mensagem para o servidor. Ele recebe o seguinte parâmetro:

        objeto_desejado: A mensagem a ser enviada para o servidor.
        Este método faz o seguinte:

        Codifica a mensagem em bytes.
        Envia a mensagem para o servidor.'''
        
        self.cliente.send(objeto_desejado.encode('utf8'))

    def menu_jogo(self):
        
        ''' Método menu_jogo(self)

        Este método exibe o menu principal do jogo. Ele não recebe parâmetros.

        Este método faz o seguinte:

        Exibe um menu com as seguintes opções:
        Salas disponíveis
        Criar uma nova sala'''
        
        menu = "\n      MENU      \n\n1  - Salas disponíveis\n2 - Criar uma nova sala\n"
        print(menu)
        opcao = input("\nDigite a opção desejada: ")
        return opcao
    
    def menu_salas(self):
        
        ''' Método menu_salas(self)

        Este método exibe o menu de salas disponíveis. Ele não recebe parâmetros.

        Este método faz o seguinte:

        Exibe uma lista com as salas disponíveis.
        Solicita ao jogador que escolha uma sala.'''
        
        menu = '\n      MENU      \n\n1  - Entrar em uma sala\n2 - Voltar para o menu principal\n'
        print(menu)
        opcao_sala = input("Digite a opção desejada: ")
        return opcao_sala
    
    def __nickname(self):
        
        ''' Método nickname(self)

        Este método solicita o nickname do jogador. Ele não recebe parâmetros.

        Este método faz o seguinte:

        Solicita ao jogador que digite seu nickname.
        Retorna o nickname digitado pelo jogador.'''
        
        nickname = input('Digite o seu nickname: ')
        return nickname
    
    def menu_jogo_chutes(self):
        
        '''Método menu_jogo_chutes(self)

        Este método exibe o menu de chutes do jogo. Ele não recebe parâmetros.

        Este método faz o seguinte:

        Exibe um menu com as seguintes opções E RETORNA A OPÇÃO ESCOLHIDA:
        Adivinhar a palavra
        Escolher uma letra'''
        
        while True:
            menu = '\n\n1  - Adivinhar a palavra\n2 - Escolher uma letra\n'
            print(menu)
            opcao_sala = input("Digite a opção desejada: ")
            if opcao_sala == '1':
                palavra = input('Digite a palavra: ')
                return (f'chutar_palavra,{palavra}')
            elif opcao_sala == '2':
                letra = input('Digite uma letra: ') 
                return (f'digitar_letra,{letra}')
            else:
                print("Opção inválida, tente novamente.")
                continue
    
    def escolher_tema(self, temas):
        
        ''' Método escolher_tema(self)

        Este método solicita o tema do jogo. Ele não recebe parâmetros.

        Este método faz o seguinte:

        Solicita ao jogador que digite o tema do jogo.
        Retorna o tema digitado pelo jogador.'''
        while True:
            tema =input('Digite o tema: ')
            if tema not in temas:
                print("Algo de errado aconteceu, Digite o tema novamente!!")
                continue
            else:
                return tema
        
    
    def iniciar_jogo(self):
        
        ''' Método loop_para_iniciar_jogo(self, nickname, sala)

        Este método inicia o jogo, esperando que haja pelo menos dois jogadores. Ele recebe os seguintes parâmetros:

        nickname: O nickname do jogador.
        sala: O nome da sala em que o jogador está jogando.
        Este método faz o seguinte:

        Envia uma mensagem para o servidor, informando que o jogador está pronto para iniciar o jogo.
        Fica em loop, esperando que o servidor envie uma mensagem informando que o jogo pode ser iniciado.
        Quando o servidor envia a mensagem, o jogo é iniciado.'''
        
        nickname = self.__nickname()
        self.__request(f'nickname,{nickname}') 

        while True:
            opcao_cliente = self.menu_jogo()
            if opcao_cliente == '1':
                self.__request('salas_disponiveis')
                resposta_servidor = self.__receber_mensagens_servidor()
                if resposta_servidor == '404':
                    print("Nenhuma sala disponível")
                    continue
                else:
                    print(resposta_servidor)
                menu_salas = self.menu_salas()
                if menu_salas == '1':
                    while True:
                        sala_desejada = (input('Digite a sala que deseja entrar: '))
                        self.__request(f'entrar_na_sala,{sala_desejada}')
                        resposta_servidor = self.__receber_mensagens_servidor()
                        if resposta_servidor == '401':
                            print("Sala não encontrada, tente novamente!!\n")
                            continue
                        elif resposta_servidor == '404':
                            print("A Sala desejada esta com lotação máxima, tente novamente!!\n")
                            continue
                        elif resposta_servidor == '200':
                            print("Você entrou na sala\n")
                            self.loop_para_iniciar_jogo(nickname, sala_desejada)
                            break
                elif menu_salas == '2':
                    continue

            elif opcao_cliente == '2':
                nome_sala = input('Digite o nome da sala: ')
                self.__request(f'criar_sala,{nome_sala}')
                while True:
                    resp = self.__receber_mensagens_servidor() 
                    if resp == '402':
                        print("O nome da sala já este em uso, tente outro nome, por favor!\n")
                        nome_sala = input('Digite o nome da sala: ')
                        self.__request(f'criar_sala,{nome_sala}')
                        continue
                    elif resp == '200':
                        print("Sala criada!!")
                        print("Você entrou na sala")
                        self.loop_para_iniciar_jogo(nickname, nome_sala)
                        break
            else:
                print("Opção inválida. Tente novamente.")
                continue
    

    def loop_para_iniciar_jogo(self, nickname, sala):
        self.__request(f'jogador_pronto,{nickname}') 
        while True: 
            if self.__receber_mensagens_servidor() == '200':
                print("Aguardando mais jogadores para iniciar a partida...")
                while True:
                    resposta = self.__receber_mensagens_servidor()
                    if resposta == 'menu':
                        resposta_jogador = self.menu_jogo_chutes()
                        self.__request(resposta_jogador)
                    elif 'tema,' in resposta:
                        array_temas = resposta.split(',')
                        print(array_temas[1])
                        resposta_jogador = self.escolher_tema(array_temas[1])
                        self.__request(resposta_jogador)
                    elif resposta == 'Jogo encerrado':
                        print(resposta)
                        sys.exit()
                    else:
                        print(f'{resposta}\n') 
            break




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python seu_script.py HOST PORT")
        sys.exit(1)

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Erro: O valor do PORT deve ser um número inteiro.")
        sys.exit(1)

    cliente = Cliente()
    cliente.iniciar_cliente(host, port)

