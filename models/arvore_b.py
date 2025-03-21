# Wyctor Fogos da Rocha
# matrícula: 2024230514
from .no_arvore_b import NodaArvoreB
from .no_arvore_b import NodaArvoreB

class ArvoreB:
    def __init__(self, ordem):
        self.ordem = ordem
        self.raiz = NodaArvoreB(ordem)

    def buscar(self, chave, no=None):
        # Procura recursivamente pela chave na árvore. 
        # Inicia a busca na raiz (ou em um nó informado).
        if no is None:
            no = self.raiz

        # Percorre as chaves do nó atual para identificar a posição correta.
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1

        # Se a chave for encontrada
        if i < len(no.chaves) and chave == no.chaves[i]:
            return True

        # Se for nó folha e a chave não existir
        if no.folha:
            return False
        # Se o nó não for folha, a função chama a si mesma para o filho apropriado.
        return self.buscar(chave, no.filhos[i])

    def inserir(self, chave, registro):
        # Insere uma nova chave e seu registro associado na árvore.
        raiz = self.raiz
        
        # Antes da inserção, verifica se a raiz está cheia.
        if len(raiz.chaves) == self.ordem - 1:
            nova_raiz = NodaArvoreB(self.ordem, folha=False)
            nova_raiz.filhos.append(raiz)
            self._dividir_filho(nova_raiz, 0, raiz)
            self.raiz = nova_raiz
        # Chama  _inserir_nao_cheio para inserir a chave em um nó que tenha espaço disponível.
        self._inserir_nao_cheio(self.raiz, chave, registro)

    def _inserir_nao_cheio(self, no, chave, registro):
        # Insere a chave em um nó que ainda não está cheio.
        i = len(no.chaves) - 1
        if no.folha:
            # Procura a posição para inserir a nova chave
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            if i >= 0 and no.chaves[i] == chave:
                # Atualiza o registro se a chave já existir
                no.registros[i] = registro
            else:
                no.chaves.insert(i + 1, chave)
                no.registros.insert(i + 1, registro)
        else:
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            # Se o filho está cheio, divide-o antes de continuar
            if len(no.filhos[i].chaves) == self.ordem - 1:
                self._dividir_filho(no, i, no.filhos[i])
                if chave > no.chaves[i]:
                    i += 1
            self._inserir_nao_cheio(no.filhos[i], chave, registro)

    def _dividir_filho(self, pai, i, filho):
        # Divide um nó filho que está cheio, promovendo a chave mediana para o nó pai.
        ordem = self.ordem
        # Cálculo do índice do meio; observe que a definição pode variar conforme a implementação
        meio = (ordem // 2) - 1  
        novo_no = NodaArvoreB(ordem=self.ordem, folha=filho.folha)

        # A chave do meio sobe para o pai
        chave_sobe = filho.chaves[meio]

        # Redistribui as chaves para o novo nó e mantém as do filho
        novo_no.chaves = filho.chaves[meio + 1:]
        filho.chaves = filho.chaves[:meio]

        if filho.folha:
            novo_no.registros = filho.registros[meio + 1:]
            filho.registros = filho.registros[:meio + 1]
        else:
            novo_no.filhos = filho.filhos[meio + 1:]
            filho.filhos = filho.filhos[:meio + 1]
        
        # Em nós folha, os registros associados são também divididos.
        pai.chaves.insert(i, chave_sobe)
        pai.filhos.insert(i + 1, novo_no)

    def remover(self, chave, no=None):
        #  Remove uma chave da árvore B, tratando casos em que a chave está em um nó folha ou em um nó interno.
        if no is None:
            no = self.raiz

        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1

        if i < len(no.chaves) and chave == no.chaves[i]:
            # Se a chave estiver em um nó folha, é simplesmente removida.
            if no.folha:
                no.chaves.pop(i)
                if no.registros:
                    no.registros.pop(i)
            # Se a chave estiver em um nó interno, tenta substituí-la pelo predecessor (maior chave à esquerda) ou sucessor (menor chave à direita)
            else:
                # Em nó interno, substitui a chave pelo seu sucessor
                sucessor_chave, sucessor_registro, no_sucessor = self._pegar_sucessor(no.filhos[i + 1])
                no.chaves[i] = sucessor_chave
                if sucessor_registro is not None:
                    if i < len(no.registros):
                        no.registros[i] = sucessor_registro
                    else:
                        no.registros.append(sucessor_registro)
                self.remover(sucessor_chave, no_sucessor)
        elif not no.folha:
            self.remover(chave, no.filhos[i])

        # Após a remoção, verifica se o nó possui o número mínimo de chaves
        min_keys = ((self.ordem + 1) // 2) - 1
        if len(no.chaves) < min_keys:
            self._balancear_depois_remover(no)

        # Se a raiz ficar sem chaves, atualiza a raiz (reduzindo a altura da árvore)
        if self.raiz and not self.raiz.chaves:
            self.raiz = self.raiz.filhos[0] if self.raiz.filhos else None

    def _balancear_depois_remover(self, no):
        # Se o nó for a raiz ou já estiver com número suficiente de chaves, não há necessidade de balancear
        if no == self.raiz or len(no.chaves) >= ((self.ordem + 1) // 2) - 1:
            return

        pai = self._encontrar_no_pai(self.raiz, no)
        if pai is None:
            return

        indice_no = pai.filhos.index(no)
        min_keys = ((self.ordem + 1) // 2) - 1

        # Tenta redistribuir com o irmão à esquerda, se possível
        if indice_no > 0:
            irmao_esq = pai.filhos[indice_no - 1]
            if len(irmao_esq.chaves) > min_keys:
                no.chaves.insert(0, pai.chaves[indice_no - 1])
                pai.chaves[indice_no - 1] = irmao_esq.chaves.pop(-1)
                if not irmao_esq.folha:
                    no.filhos.insert(0, irmao_esq.filhos.pop(-1))
                return

        # Tenta redistribuir com o irmão à direita, se possível
        if indice_no < len(pai.filhos) - 1:
            irmao_dir = pai.filhos[indice_no + 1]
            if len(irmao_dir.chaves) > min_keys:
                no.chaves.append(pai.chaves[indice_no])
                pai.chaves[indice_no] = irmao_dir.chaves.pop(0)
                if not irmao_dir.folha:
                    no.filhos.append(irmao_dir.filhos.pop(0))
                return

        # Se não for possível redistribuir, realiza a fusão dos nós
        if indice_no > 0:
            # Mescla com o irmão à esquerda
            irmao_esq = pai.filhos[indice_no - 1]
            chave_pai = pai.chaves.pop(indice_no - 1)
            irmao_esq.chaves.append(chave_pai)
            irmao_esq.chaves.extend(no.chaves)
            if not no.folha:
                irmao_esq.filhos.extend(no.filhos)
            pai.filhos.pop(indice_no)
        else:
            # Mescla com o irmão à direita
            irmao_dir = pai.filhos[indice_no + 1]
            chave_pai = pai.chaves.pop(indice_no)
            no.chaves.append(chave_pai)
            no.chaves.extend(irmao_dir.chaves)
            if not irmao_dir.folha:
                no.filhos.extend(irmao_dir.filhos)
            pai.filhos.pop(indice_no + 1)

        # Verifica recursivamente se o nó pai necessita de balanceamento após a fusão
        if pai != self.raiz and len(pai.chaves) < min_keys:
            self._balancear_depois_remover(pai)

    def _pegar_sucessor(self, no):
        # Retorna a menor chave (e seu registro) da subárvore do nó informado.
        while not no.folha:
            no = no.filhos[0]
        if no.registros:
            return no.chaves[0], no.registros[0], no
        return no.chaves[0], None, no

    def _encontrar_no_pai(self, no, filho):
        # Localiza recursivamente o nó pai de um nó específico.
        if no is None or no.folha:
            return None
        for f in no.filhos:
            if f == filho:
                return no
            p = self._encontrar_no_pai(f, filho)
            if p:
                return p
        return None

    def percorrer_em_largura(self):
        #  Faz a varredura da árvore, retornando a representação dos nós pra cada nível.
        if not self.raiz:
            return []
    
        resultado = []
        fila = [self.raiz]
    
        while fila:
            nivel = []
            prox_nivel = []
    
            for no in fila:
                chaves_str = ', '.join(f'key: {chave}' for chave in no.chaves)
                nivel.append(f'[{chaves_str}]')
                prox_nivel.extend(no.filhos)
    
            resultado.append(' '.join(nivel))
            fila = prox_nivel
    
        return resultado
