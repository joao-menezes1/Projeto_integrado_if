class Node:
  '''
    Classe de objetos para um nó dinâmico na memória
    '''

  def __init__(self, data):
    self.__data = data
    self.__next = None

  @property
  def data(self):
    return self.__data

  @data.setter
  def data(self, newData):
    self.__data = newData

  @property
  def next(self):
    return self.__next

  @next.setter
  def next(self, newNext):
    self.__next = newNext

  def hasNext(self):
    return self.__next != None

  def __str__(self):
    return str(self.__data)


class ListException(Exception):
  """Classe de exceção lançada quando uma violação de ordem genérica
       da lista é identificada.
    """

  def __init__(self, msg):
    """ Construtor padrão da classe, que recebe uma mensagem que se deseja
            embutir na exceção
        """
    super().__init__(msg)


class LinkedList:
  """
    A classe ListaEncadeada implementa a estrutura de dados Lista Encadeada.
    Esta implementação utiliza nós encadeados para armazenar e manipular dados.
    A lista encadeada pode ser usada para armazenar qualquer tipo de dado, seja
    um tipo primitivo ou um objeto.

    Attributes:
        head (Node): O nó de início da lista encadeada.
        tail (Node): o nó final da lista encadeada.
        size (int): A quantidade de elementos na lista encadeada.
        pointer (Node): O ponteiro ou cursor que apontará em qual nó a lista está e que também serve para passar pelos nós no percorrer da lista
    """

  def __init__(self) -> None:
    """ Construtor padrão da classe Lista. Ao instanciar
            um objeto do tipo Lista, este iniciará vazio. 
        """
    self.__head = None
    self.__tail = None
    self.__size = 0
    self.__pointer = self.__head

  def isEmpty(self):
    """ Método que verifica se a lista está vazia ou não.

        Returns:
            boolean: True se a lista estiver vazia, False caso contrário.
        """
    return self.__size == 0

  def __len__(self):
    """ Método que retorna a quantidade de elementos existentes na lista

        Returns:
            int: um número inteiro que determina o número de elementos existentes na lista
        """
    return self.__size

  def insert(self, value, position):
    """ Método que adiciona um novo elemento à lista.

        Args:
            position (int): um número correpondente à posição em que se deseja
                  inserir um novo valor
            value (any): o conteúdo que deseja armazenar na lista.

        Raises:
            ListaException: Exceção lançada quando uma posição inválida é fornecida pelo usuário. São inválidas posições que se referem a:
                  (a) números negativos
                  (b) zero
                  (c) número natural correspondente a um elemento que excede a
                      quantidade de elementos da lista.
        """
    try:
      assert position > 0 and position <= len(
          self) + 1, f'Posicao invalida. Lista contém {self.__size} elementos'
      if self.isEmpty():
        if (position != 1):
          raise ListException(
              f'A lista esta vazia. A posicao correta para insercao é 1.')
        new = Node(value)
        self.__head = new
        self.__tail = new
        self.__tail.next = self.__head
        self.__size += 1
        self.__pointer = self.__head

      elif position == 1:
        new = Node(value)
        new.next = self.__head
        self.__head = new
        self.__tail.next = self.__head
        self.__size += 1
        self.__pointer = self.__head

      elif position == len(self) + 1:
        new = Node(value)
        self.__tail.next = new
        self.__tail = new
        self.__tail.next = self.__head
        self.__size += 1

      else:
        new = Node(value)
        pointer = self.__head
        count = 1
        while (count < (position - 1)):
          pointer = pointer.next
          count += 1
        new.next = pointer.next
        pointer.next = new
        self.__size += 1

    except TypeError:
      raise ListException(f'A posição deve ser um número inteiro')
    except AssertionError as ae:
      raise ListException(ae)

  def advance(self):
    """ Método que avança o ponteiro da lista.

            Returns: Ponteiro que representa o próximo jogador da partida.
        """
    self.__pointer = self.__pointer.next
    return self.__pointer.data

  def goTo(self, start, quantity):
    """ Método que recebe quem começa o jogo(start) e a quantidade de iterações, servindo para percorrer até a posição do eliminado.

        Args:
            start (any): quem começa o jogo.
            qunatity (int): quantidade de iterações.

        Returns: Posição do jogador eliminado.
        """
    pointer = self.__head
    count = 1
    while (count < start):
      pointer = pointer.next
      count += 1
    for i in range(quantity):
      pointer = pointer.next
    return pointer.data


  def tamanho(self):
    return self.__size
    
  def remove(self, position):
    """ Método que remove um elemento da lista.

        Args:
            position (int): um número correpondente à ordem do elemento na lista.
        
        Returns:
            qualquer tipo primitivo: o valor encontrado no elemento removido

        Raises:
            ListaException: Exceção lançada quando uma posição inválida é
                  fornecida pelo usuário. São inválidas posições que se referem a:
                  (a) números negativos
                  (b) zero
                  (c) número natural correspondente a um elemento que excede a
                      quantidade de elementos da lista.                      
        """
    try:
      if (self.isEmpty()):
        raise ListException(f'Não é possível remover de uma lista vazia')
      assert position > 0 and position <= len(
          self), f'Posicao invalida. Lista contém {self.__size} elementos'

      if position == 1:
        data = self.__head.data
        pointer = self.__head
        self.__tail.next = pointer.next
        self.__head = pointer.next
        self.__size -= 1
        self.__pointer = self.__head
        if data == self.__pointer.data:
          self.__pointer = self.__pointer.next
        return data

      elif position == len(self):
        data = self.__tail.data
        count = 1
        pointer = self.__head
        while count < position - 1:
          pointer = pointer.next
          count += 1
        pointer.next = self.__head
        self.__tail = pointer
        self.__size -= 1
        if data == self.__pointer.data:
          self.__pointer = self.__pointer.next
        return data

      else:
        pointer = self.__head
        ant = self.__head
        count = 1
        while (count < position):
          ant = pointer
          pointer = pointer.next
          count += 1
        ant.next = pointer.next
        data = pointer.data
        if data == self.__pointer.data:
          self.__pointer = self.__pointer.next
        self.__size -= 1
        return data

    except TypeError:
      raise ListException(f'A posição deve ser um número inteiro')
    except AssertionError as ae:
      raise ListException(ae)

  def index(self, elem):
    """ Método que recupera a posicao ordenada, dentro da lista, em que se
            encontra um elemento passado como argumento. No caso de haver mais de uma
            ocorrência do valor, a primeira ocorrência será levada em conta.
        Args:
            elem (any): o elemento que deverá ser buscada a sua posição.
        
        Returns:
            int: um número inteiro representando a posição, na lista, em que foi
                 encontrado "elem".

        Raises:
            ListException: Exceção lançada quando o argumento "elem"
                  não está presente na lista ou se a lista estiver vazia.
        """
    if (self.isEmpty()):
      raise ListException(f'Lista vazia')
    pointer = self.__head
    count = 1
    while True:
      if pointer.data == elem:
        return count
      pointer = pointer.next
      count += 1
      if pointer == self.__head:
        break
    raise ListException(f'O elemento {elem} não está armazenado na lista')

  def element(self, index):
    """ Método que recupera o elemento, dentro da lista, em que se
            encontrado através do seu índice passado como argumento. No caso de haver mais de uma
            ocorrência do element, a primeira ocorrência será levada em conta.
            
        Args:
            index (int): Índex do elemento que será buscado na lista.

        Raises:
            ListaException: Exceção lançada quando o argumento no índice é inválida,sendo negativa
        """
    try:
      assert not self.isEmpty(), 'Lista vazia'
      assert index >= 0 and index <= len(
          self), f'Posicao invalida. Lista contém {self.__size} elementos'

      pointer = self.__head
      count = 1
      while (count <= index):
        pointer = pointer.next
        count += 1
      return pointer.data
    except TypeError:
      raise ListException(f'A posição deve ser um número inteiro')
    except AssertionError as ae:
      raise ListException(ae)

  def verifyElement(self, element):

    """ Método que verifica se o elemento dentro da lista está igual a outro elemento.
        Args:
            element (any): Elemento que será comparado na lista.
        
        Returns:
            any: um elemento que foi achado na lista com base na sua posição.

        Raises:
            ListaException: Erro se um elemento for igual a outro que já pertencia a lista ou AssertionError.
        """
    try:
      pointer = self.__head
      for i in range(len(self)):
        assert pointer.data != element, f'O elemento [{element}] já está na lista e não pode ser adicionado de novo.'
        pointer = pointer.next
    except AssertionError as ae:
      raise ListException(ae)

  def __str__(self) -> str:
    str = '[ '
    if self.isEmpty():
      str += ']'
      return str
    pointer = self.__head
    for i in range(1, len(self) + 1):
      str += f'{pointer.data}, '
      pointer = pointer.next
    str = str[:-2] + " ]"
    return str

