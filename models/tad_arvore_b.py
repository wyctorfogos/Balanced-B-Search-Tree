class NodaArvoreB:
    def __init__(self, ordem, folha=True):
        self.ordem = ordem
        self.folha = folha
        self.chaves = []
        self.registros = []
        self.filhos = []

class ArvoreB:
    def __init__(self, ordem):
        self.ordem = ordem
        self.raiz = NodaArvoreB(ordem, folha=True)

    def buscar(self, chave, no=None):
        """Busca uma chave na árvore B a partir de um nó (padrão: raiz)."""
        if no is None:
            no = self.raiz  # Define raiz como padrão

        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1

        if i < len(no.chaves) and chave == no.chaves[i]:
            return True  # Chave encontrada

        if no.folha:
            return False  # Chave não encontrada

        return self.buscar(chave, no.filhos[i])  # Busca recursiva


    def inserir(self, chave, registro):
        raiz = self.raiz
        if len(raiz.chaves) == self.ordem - 1:
            nova_raiz = NodaArvoreB(self.ordem, folha=False)
            nova_raiz.filhos.append(raiz)
            self._dividir_filho(nova_raiz, 0, raiz)
            self.raiz = nova_raiz
        self._inserir_nao_cheio(self.raiz, chave, registro)

    def _dividir_filho(self, pai, i, filho):
        ordem = self.ordem
        novo_no = NodaArvoreB(ordem, filho.folha)
        meio = ordem // 2

        novo_no.chaves = filho.chaves[meio + 1:]
        novo_no.registros = filho.registros[meio + 1:]

        if not filho.folha:
            novo_no.filhos = filho.filhos[meio + 1:]

        pai.chaves.insert(i, filho.chaves[meio])
        pai.registros.insert(i, filho.registros[meio])
        pai.filhos.insert(i + 1, novo_no)

        filho.chaves = filho.chaves[:meio]
        filho.registros = filho.registros[:meio]
        if not filho.folha:
            filho.filhos = filho.filhos[:meio + 1]

    def _inserir_nao_cheio(self, no, chave, registro):
        i = len(no.chaves) - 1
        if no.folha:
            no.chaves.append(None)
            no.registros.append(None)
            while i >= 0 and chave < no.chaves[i]:
                no.chaves[i + 1] = no.chaves[i]
                no.registros[i + 1] = no.registros[i]
                i -= 1
            no.chaves[i + 1] = chave
            no.registros[i + 1] = registro
        else:
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            if len(no.filhos[i].chaves) == self.ordem - 1:
                self._dividir_filho(no, i, no.filhos[i])
                if chave > no.chaves[i]:
                    i += 1
            self._inserir_nao_cheio(no.filhos[i], chave, registro)

    def remover(self, chave):
        if not self.raiz:
            return
        self._remover(self.raiz, chave)
        if len(self.raiz.chaves) == 0:
            if self.raiz.filhos:
                self.raiz = self.raiz.filhos[0]
            else:
                self.raiz = None

    def _remover(self, no, chave):
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1

        if i < len(no.chaves) and chave == no.chaves[i]:
            if no.folha:
                no.chaves.pop(i)
            else:
                no.chaves[i] = self._pegar_maior(no.filhos[i])
                self._remover(no.filhos[i], no.chaves[i])
        elif not no.folha:
            self._remover(no.filhos[i], chave)

    def _pegar_maior(self, no):
        while not no.folha:
            no = no.filhos[-1]
        return no.chaves[-1]

    def percorrer_em_largura(self):
        if not self.raiz:
            return []

        resultado = []
        fila = [self.raiz]

        while fila:
            nivel = []
            prox_nivel = []

            for no in fila:
                chaves_str = ", ".join([f"key: {chave}" for chave in no.chaves])
                nivel.append(f"[{chaves_str}]")
                prox_nivel.extend(no.filhos)

            resultado.append(" ".join(nivel))
            fila = prox_nivel

        return resultado
