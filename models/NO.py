# Wyctor Fogos da Rocha
# matrícula: 2024230514
class NoABB:
    def __init__(self, ordem, folha=True):
        """
        Inicializa um nó da Árvore B.

        :param ordem: Número máximo de filhos por nó.
        :param folha: Indica se o nó é uma folha (True) ou um nó interno (False).
        """
        self.ordem = ordem  # Número máximo de filhos do nó
        self.folha = folha  # Se True, o nó é folha
        self.chaves = []  # Lista de chaves armazenadas no nó
        self.registros = []  # Lista de registros associados às chaves
        self.filhos = []  # Ponteiros para os filhos (se não for folha)

    def __str__(self):
        """
        Representação do nó como string para facilitar a visualização.
        """
        return f"Nó(folha={self.folha}, chaves={self.chaves})"
