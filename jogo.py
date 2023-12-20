import dicionario_temas_palavras
from unidecode import unidecode
import random
import re
from lista_circular import *
from fila import *
import socket
import time


''' Classe Jogo

        A classe Jogo é responsável por gerenciar o jogo da forca. Ela possui os seguintes atributos:

        jogadores: uma lista circular de jogadores
        Os seguintes métodos são implementados na classe Jogo:

        __init__(): inicializa a classe Jogo
        __enviar_msg_cliente(): envia uma mensagem para um cliente
        __receber_msg_cliente(): recebe uma mensagem de um cliente
        __enviar_msg_cliente_broadcast(): envia uma mensagem para todos os clientes
        limpar_entrada(): limpa uma entrada do usuário
        __palavra_usuario(): gera uma palavra secreta para o jogo
        __mostrar_temas()`: mostra os temas disponíveis para o jogo
        __buscar_palavra()`: busca uma palavra secreta de um tema específico
        letras(): preenche a palavra secreta com as letras corretas
        chutar_palavra(): verifica se a palavra secreta foi acertada
        adicionar_jogadores_a_lista(): adiciona os jogadores à lista de jogadores
        __passar_a_vez_jogador()`: passa a vez para o próximo jogador
        _iniciar_jogo(): inicia o jogo da forca 
    '''

class Jogo:

    def __init__(self):
        
        '''
            Método init()`

            O método __init__() É O CONSTRUTOR  QUE inicializa a A ESTRUTURA DE DADOS da classe Jogo.
            jogadores: é uma lista encadeada circular de jogadores.'''
        
        self.jogadores = LinkedList()

    def __enviar_msg_cliente(self, mensagem, cliente):
        
        '''  O método __enviar_msg_cliente() envia uma mensagem para um cliente usando o socket do servidor. Ele recebe os seguintes parâmetros de entrada:

        mensagem: a mensagem a ser enviada
        cliente: o socket do cliente '''
        
        cliente.send(f'{mensagem}'.encode('utf8'))

    def __receber_msg_cliente(self, cliente):
        
        '''  O método __receber_msg_cliente() recebe uma mensagem de um cliente. Ele recebe os seguintes parâmetros de entrada:
        
        cliente: o socket do cliente e retorna a mensagem que chegou. '''
        
        msg = cliente.recv(1024).decode('utf8')
        return msg
    
    def __enviar_msg_cliente_broadcast(self, mensagem, clientes_lista):
        
        '''  O método __enviar_msg_cliente_broadcast() envia uma mensagem para todos os clientes. Ele recebe os seguintes parâmetros de entrada:

        mensagem: a mensagem a ser enviada
        clientes_lista: uma lista de sockets dos clientes '''
        
        for cliente in clientes_lista:
            self.__enviar_msg_cliente(mensagem, cliente)

    def limpar_entrada(self, entrada):
        
        '''  O método limpar_entrada() limpa uma entrada do usuário. Ele recebe os seguintes parâmetros de entrada:

        entrada: a entrada a ser limpa
        Este método remove os acentos, números e caracteres especiais da entrada entrada e retorna a entrada limpa. '''
        
        entrada_sem_acentos = unidecode(entrada)
        entrada_sem_numeros = re.sub(r'\d+', '', entrada_sem_acentos)
        entrada_apenas_letras = re.sub(r'[^a-zA-Z]', '-', entrada_sem_numeros)
        return entrada_apenas_letras

    def __palavra_usuario(self, cliente, lista_jogadores):
        
        '''  O método __palavra_usuario() gera uma palavra secreta para o jogo. Ele recebe os seguintes parâmetros de entrada:

        cliente: o socket do cliente
        lista_jogadores: uma lista de sockets dos clientes
        Este método solicita ao cliente cliente que escolha um tema e uma palavra para o jogo. O método então retorna a palavra secreta escolhida. '''
        
        tema = self.__mostrar_temas()
        self.__enviar_msg_cliente(f'tema,{tema}', cliente)
        tema_escolhido = self.__receber_msg_cliente(cliente)
        self.__enviar_msg_cliente_broadcast(f'\nO tema escolhido foi {tema_escolhido}\n', lista_jogadores)
        palavra = self.__buscar_palavra(tema_escolhido)
        return self.limpar_entrada(palavra)

    def __mostrar_temas(self):
        
        '''  O método __mostrar_temas() mostra os temas disponíveis para o jogo. Ele não recebe parâmetros de entrada e serve para montar uma string com os temas disponíveis no dicionário de temas e retorna esta string.

        Este método retorna uma lista em forma de string com os temas disponíveis para o jogo. '''
         
        temas = dicionario_temas_palavras.Temas
        tema_escolhido = "      TEMAS      \n\n"
        for tema, array in temas.items():
            tema_escolhido += (f'-  {tema}\n')
        return tema_escolhido

    def __buscar_palavra(self, tema_escolhido):
        
        '''  O método __buscar_palavra() busca uma palavra secreta de um tema específico. Ele recebe os seguintes parâmetros de entrada:

        tema_escolhido: o tema da palavra secreta
        Este método busca uma palavra secreta do tema tema_escolhido no dicionário de palavras da forca. O método então retorna a palavra secreta encontrada. '''
        
        palavras_tema = dicionario_temas_palavras.Temas.get(tema_escolhido)
        palavra_aleatoria_escolhida = random.choice(palavras_tema)
        return palavra_aleatoria_escolhida

    def letras(self, letra, array_palavra_jogo, palavra):
        
        ''' O método letras() preenche a palavra secreta com as letras corretas. Ele recebe os seguintes parâmetros de entrada:

        letra: a letra a ser inserida na palavra secreta
        array_palavra_jogo: um array com as letras já acertadas da palavra secreta
        palavra: a palavra secreta
        Este método percorre todas as letras da palavra secreta palavra e compara cada letra com a letra letra passada como parâmetro.
        Se a letra for igual, a letra correspondente no array array_palavra_jogo é substituída pela letra letra.
        O método então retorna o array array_palavra_jogo com as letras preenchidas.
        Este método insere a letra letra no array se a letra estiver na palavra. '''
        
        for i, let in enumerate(palavra):
            if letra == let:
                array_palavra_jogo[i] = letra
        palavra_letras = (' '.join(array_palavra_jogo))
        return palavra_letras
    
    def chutar_palavra(self, palavra, palavra_chute):
        
        '''  O método chutar_palavra() verifica se a palavra secreta foi acertada. Ele recebe os seguintes parâmetros de entrada:
        palavra: a palavra secreta
        palavra_chute: a palavra chutada pelo jogador
        Este método remove os acentos e caracteres especiais de ambas as palavras e transforma ambas em minúsculas.
        O método então compara as duas palavras.
        Se as palavras forem iguais, o método retorna True.
        Caso contrário, o método retorna False. '''
        
        palavra_normalizada = ''.join(palavra)
        if palavra_normalizada.lower() == palavra_chute:
            return True
    
    def adicionar_jogadores_a_lista(self, lista_jogadores):
        
        '''  O método adicionar_jogadores_a_lista() adiciona os jogadores à lista de jogadores. Ele recebe os seguintes parâmetros de entrada:
        lista_jogadores: uma lista de sockets dos clientes recebido pelo servidor
        Este método percorre a lista lista_jogadores e insere cada jogador na lista jogadores da classe Jogo.
        Para cada jogador, o método também insere um identificador numérico que indica a posição do jogador na lista de jogadores. '''
        
        for i in range(len(lista_jogadores)):
            self.jogadores.insert(lista_jogadores[i], (i+1))
    
    def __passar_a_vez_jogador(self):
        
        '''  O método __passar_a_vez_jogador() passa a vez para o próximo jogador. Ele não recebe parâmetros de entrada e não retorna nenhum valor.
        Este método avança a lista de jogadores em uma posição, indicando assim que o próximo jogador da lista terá a vez de jogar. '''
        
        return self.jogadores.advance()

    def _iniciar_jogo(self, lista_jogadores):
        
        '''  O método _iniciar_jogo() inicia o jogo da forca. Ele recebe os seguintes parâmetros de entrada:
        
            lista_jogadores: uma lista de sockets dos clientes
            
            Este método é o principal responsável pelo fluxo do jogo. Ele executa os seguintes passos:
                Adiciona os jogadores à lista de jogadores.
                Define o número máximo de tentativas, a palavra secreta, o array para mostrar o progresso da palavra, a fila para armazenar as letras erradas, o número de tentativas realizadas, o número de rodadas e o jogador atual.
                
                Entra em um loop que continua até que a palavra secreta seja acertada ou o número máximo de tentativas seja atingido:
                    Envia uma mensagem para o jogador atual indicando que é sua vez de jogar.
                    Recebe a resposta do jogador, que pode ser chutar a palavra, digitar uma letra ou outras ações.
                    Verifica a resposta do jogador e executa as ações apropriadas:
                        Se o jogador chutar a palavra: verifica se a palavra está correta. Se estiver, o jogo termina e o jogador que acertou é anunciado. Caso contrário, o jogador perde a vez.
                        Se o jogador digitar uma letra: verifica se a letra está na palavra secreta. Se estiver, preenche a palavra secreta com a letra e avança para o próximo jogador. Caso contrário, adiciona a letra à fila de letras erradas e passa a vez para o próximo jogador.
                    Envia uma mensagem para todos os jogadores atualizando o estado do jogo: o progresso da palavra secreta, as letras erradas, o número de tentativas restantes e o desenho da forca de acordo com o número de tentativas feitas.
                    
            Ao final do loop, se a palavra secreta foi acertada, o jogo termina e o jogador que acertou é anunciado. Caso contrário, o jogo termina e todos os jogadores são informados que a palavra não foi acertada. '''

        self.adicionar_jogadores_a_lista(lista_jogadores)
        tentativas_maximas = 6
        palavra = list(self.__palavra_usuario(self.jogadores.element(0), lista_jogadores).upper())
        array_palavra_jogo = ['_'] * len(palavra)
        fila_letras_erradas = Fila()
        tentativas = 0
        rodadas = 0
        jogador = self.jogadores.element(0)
        partes_forca = [
        '''
           -----
           |   |
               |
               |
               |
               |
        ''',
        '''
           -----
           |   |
           O   |
               |
               |
               |
        ''',
        '''
           -----
           |   |
           O   |
           |   |
               |
               |
        ''',
        '''
           -----
           |   |
           O   |
          /|   |
               |
               |
        ''',
        '''
           -----
           |   |
           O   |
          /|\  |
               |
               |
        ''',
        '''
           -----
           |   |
           O   |
          /|\  |
          /    |
               |
        ''',
        '''
           -----
           |   |
           O   |
          /|\  |
          / \  |
               |
        '''
        ]
        
        while '_' in array_palavra_jogo and tentativas < tentativas_maximas:
            self.__enviar_msg_cliente('menu', jogador)
            resposta = self.__receber_msg_cliente(jogador)
            print(resposta)

            if 'chutar_palavra' in resposta:
                array_resposta = resposta.split(',')
                palavra_chute = array_resposta[1]
                resultado = self.chutar_palavra(palavra, palavra_chute)
                if resultado == True:
                    break
                else: 
                    self.__enviar_msg_cliente("Palavra incorreta, você perdeu a vez...", jogador)
                    tentativas += 1
                    rodadas += 1
                    self.__enviar_msg_cliente_broadcast(f'\nRODADA {rodadas}\n\nLetras erradas = {fila_letras_erradas}\nTentativas restantes = {tentativas_maximas - tentativas}\n\n\n{partes_forca[tentativas]}', lista_jogadores)
                    jogador = self.jogadores.advance()
                    continue
            
            elif 'digitar_letra' in resposta:
                array_resposta = resposta.split(',')
                entrada_jogador = array_resposta[1]

                letra = self.limpar_entrada(entrada_jogador.upper())
                if len(letra) != 1:
                    self.__enviar_msg_cliente('Por favor, digite apenas uma letra.', jogador)
                    continue

                elif fila_letras_erradas.busca(letra) or letra in array_palavra_jogo:
                    self.__enviar_msg_cliente('Você já tentou essa letra. Tente outra.', jogador)
                    continue

                elif letra in palavra:
                    palavra_rasurada = self.letras(letra, array_palavra_jogo, palavra)
                    rodadas += 1
                    self.__enviar_msg_cliente_broadcast(f'\nRODADA {rodadas}\n\nPalavra = {palavra_rasurada}\nLetras erradas = {fila_letras_erradas}\nTentativas restantes = {tentativas_maximas - tentativas}\n\n\n{partes_forca[tentativas]}', lista_jogadores)
                    if '_' not in array_palavra_jogo:
                        break
                    jogador = self.jogadores.advance()

                else:
                    tentativas += 1
                    rodadas += 1
                    fila_letras_erradas.enfileirar(letra)
                    self.__enviar_msg_cliente_broadcast(f'\nRODADA {rodadas}\n\nLetras erradas = {fila_letras_erradas}\nTentativas restantes = {tentativas_maximas - tentativas}\n\n\n{partes_forca[tentativas]}', lista_jogadores)
                    jogador = self.jogadores.advance()

        if '_' not in array_palavra_jogo:
            # self.__enviar_msg_cliente_broadcast(f'\nParabéns! O jogador {jogador} acertou a palavra.', lista_jogadores)
            # self.__enviar_msg_cliente_broadcast("Jogo encerrado", lista_jogadores)
            return ("Jogo_encerrado", jogador)
            ##self.__encerrar_jogo(pass)
        elif tentativas >= tentativas_maximas:
            # self.__enviar_msg_cliente_broadcast(f'\nVocê perdeu! A palavra era "{" ".join(palavra)}"', lista_jogadores)
            # self.__enviar_msg_cliente_broadcast("Jogo encerrado", lista_jogadores)
            return (f"Jogo_encerrado", 'nenhum')
        
        else:
            # self.__enviar_msg_cliente_broadcast(f'\nParabéns! O jogador {jogador} acertou a palavra.', lista_jogadores)
            # self.__enviar_msg_cliente_broadcast("Jogo encerrado", lista_jogadores)
            
            return ("Jogo_encerrado", jogador)