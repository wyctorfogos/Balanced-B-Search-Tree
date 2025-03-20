# Wyctor Fogos da Rocha
# matrícula: 2024230514

class Empty(Exception):
    pass
class UnknownOperator(Exception):
    pass

class TadPilha:
    # Pilha como uma lista
    # Esse Tad foi feito com base na aula 04 de Estrutura de Dados (confira os slides!)
    # Construtor da classe PilhaLista
    def __init__(self):
        self._pilha = [] # lista que conterá a pilha

    # Retorna o tamanho da pilha
    def __len__ (self):
        return len(self._pilha)

    # retorna True se pilha vazia
    def is_empty(self):
        return len(self._pilha) == 0

    # empilha novo elemento e 
    def push(self, e):
        self._pilha.append(e)


    # Retorna o elemento do topo da pilha (o último adicionado) sem retirá-lo
    # Exceção se pilha vazia
    def top(self):
        if self.is_empty( ):
            raise Empty("Pilha vazia")
        return self._pilha[-1]

    # desempilha elemento
    # excessão se pilha vazia
    def pop(self):
        if self.is_empty():
            raise Empty("Pilha vazia")
        return self._pilha.pop()