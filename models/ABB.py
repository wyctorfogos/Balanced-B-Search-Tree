class ABB:
    def __init__(self, chave):
        """
        Inicializa um nó da Árvore Binária de Busca (ABB).
        
        :param chave: Valor armazenado no nó (chave da ABB).
        """
        self.chave = chave  # Armazena a chave do nó
        self.esquerda = None  # Ponteiro para a subárvore esquerda
        self.direita = None  # Ponteiro para a subárvore direita
        self.folha = True  # Inicialmente, assume-se que o nó é folha

    def __str__(self):
        """
        Retorna a representação do nó.
        """
        return f"Nó(chave={self.chave}, folha={self.folha})"

    def insere_recursivo(self, h, chave):
        """
        Insere um novo nó na ABB recursivamente.
        
        :param h: Raiz da ABB atual.
        :param chave: Valor a ser inserido.
        :return: Retorna a raiz original após a modificação.
        """
        if h is None:
            return ABB(chave)

        if chave < h.chave:
            h.esquerda = self.insere_recursivo(h.esquerda, chave)
        else:
            h.direita = self.insere_recursivo(h.direita, chave)

        # Atualiza a propriedade folha
        h.folha = h.esquerda is None and h.direita is None
        return h

    def busca_recursiva(self, h, chave):
        """
        Busca um valor na ABB recursivamente.
        
        :param h: Raiz da ABB atual.
        :param chave: Valor a ser buscado.
        :return: Retorna o nó se encontrado, ou None se não existir.
        """
        if h is None:
            print("Árvore vazia!")
            return None

        if chave == h.chave:
            return h

        if chave < h.chave:
            return self.busca_recursiva(h.esquerda, chave)

        return self.busca_recursiva(h.direita, chave)   
    
    def altura(self, h):
        if h is None:
            return 0
        
        altura_esquerda=self.altura(h.esqueda)
        altura_direita=self.altura(h.direita)

        return max(altura_esquerda+altura_direita)+1

    def remover_recursivo(self, h, chave):
        """
        Remove um nó da ABB recursivamente.
        """
        if h is None:
            return h

        if chave < h.chave:
            h.esquerda = self.remover_recursivo(h.esquerda, chave)
        elif chave > h.chave:
            h.direita = self.remover_recursivo(h.direita, chave)
        else:
            # 🚀 Caso 1: Nó sem filhos (é uma folha)
            if h.esquerda is None and h.direita is None:
                return None

            # 🚀 Caso 2: Nó com apenas um filho
            if h.esquerda is None:
                return h.direita
            elif h.direita is None:
                return h.esquerda

            # 🚀 Caso 3: Nó com dois filhos
            sucessor = self._minimo_no(h.direita)
            h.chave = sucessor.chave
            h.direita = self.remover_recursivo(h.direita, sucessor.chave)

        return h

    def _minimo_no(self, h):
        """
        Encontra o menor nó na subárvore.
        """
        atual = h
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual
