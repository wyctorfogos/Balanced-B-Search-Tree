from .no_arvore_b import NodaArvoreB

class ArvoreB:
    def __init__(self, ordem):
        self.ordem = ordem
        self.raiz = NodaArvoreB(ordem)

    def inserir(self, chave):
        raiz = self.raiz
        if len(raiz.chaves) == self.ordem - 1:
            nova_raiz = NodaArvoreB(self.ordem, folha=False)
            nova_raiz.filhos.append(raiz)
            self._dividir_filho(nova_raiz, 0, raiz)
            self.raiz = nova_raiz
        self._inserir_nao_cheio(self.raiz, chave)

    def _inserir_nao_cheio(self, no, chave):
        i = len(no.chaves) - 1
        if no.folha:
            no.chaves.append(0)
            while i >= 0 and chave < no.chaves[i]:
                no.chaves[i+1] = no.chaves[i]
                i -= 1
            no.chaves[i + 1] = chave
        else:
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            if len(no.filhos[i].chaves) == self.ordem - 1:
                self._dividir_filho(no, i, no.filhos[i])
                if chave > no.chaves[i]:
                    i += 1
            self._inserir_nao_cheio(no.filhos[i], chave)


    def _dividir_filho(self, pai, i, filho):
        ordem = self.ordem
        meio = (ordem - 1) // 2

        novo_no = NodaArvoreB(ordem=self.ordem, folha=filho.folha)

        # Chave que sobe para o pai
        chave_sobe = filho.chaves[meio]

        # Novo nó pega chaves depois do meio
        novo_no.chaves = filho.chaves[meio+1:]
        filho.chaves = filho.chaves[:meio]

        if not filho.folha:
            novo_no.filhos = filho.filhos[meio+1:]
            filho.filhos = filho.filhos[:meio+1]

        pai.chaves.insert(i, chave_sobe)
        pai.filhos.insert(i + 1, novo_no)

    def percorrer_em_largura(self):
        if not self.raiz:
            return []

        resultado = []
        fila = [self.raiz]

        while fila:
            nivel_str = ""
            prox_nivel = []

            for no in fila:
                chaves_str = ", ".join(f"key: {chave}" for chave in no.chaves)
                nivel_str += f"[{chaves_str}] "
                prox_nivel.extend(no.filhos)

            resultado.append(nivel_str.strip())
            fila = prox_nivel

        return resultado

    def buscar(self, chave, no=None):
        if no is None:
            no = self.raiz
        
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1

        if i < len(no.chaves) and chave == no.chaves[i]:
            return True  # Chave encontrada

        if no.folha:
            return False  # Chegou em uma folha e não achou a chave

        # Busca no filho correto
        return self.buscar(chave, no.filhos[i])

    def remover(self, chave, no=None):
        if no is None:
            no = self.raiz

        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1

        if i < len(no.chaves) and chave == no.chaves[i]:  # Chave encontrada
            if no.folha:
                no.chaves.pop(i)  # Removemos diretamente da folha
            else:
                sucessor_chave = self._pegar_sucessor(no.filhos[i + 1])
                no.chaves[i] = sucessor_chave
                self.remover(sucessor_chave, no.filhos[i + 1])
        elif not no.folha:
            if i < len(no.filhos):
                self.remover(chave, no.filhos[i])


    def _pegar_sucessor(self, no):
        atual = no
        while not atual.folha:
            atual = atual.filhos[0]
        return atual.chaves[0]  # Agora só retorna a chave
