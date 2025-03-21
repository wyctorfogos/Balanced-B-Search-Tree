# Wyctor Fogos da Rocha
# matrícula: 2024230514

from .no_arvore_b import NodaArvoreB

class ArvoreB:
    def __init__(self, ordem):
        self.ordem = ordem
        self.raiz = NodaArvoreB(ordem)

    def buscar(self, chave, no=None):
        #  Procura recursivamente pela chave na árvore. Inicia a busca na raiz (ou em um nó informado)
        #  e percorre os nós de acordo com a ordem dos elementos.
        if no is None:
            no = self.raiz
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1
        if i < len(no.chaves) and chave == no.chaves[i]:
            return True
        if no.folha:
            return False
        return self.buscar(chave, no.filhos[i])

    def inserir(self, chave, registro):
        # Insere uma nova chave e seu registro associado na árvore.
        raiz = self.raiz
        # Aqui o nó é considerado cheio se tiver self.ordem chaves
        if len(raiz.chaves) >= self.ordem:
            nova_raiz = NodaArvoreB(self.ordem, folha=False)
            nova_raiz.filhos.append(raiz)
            self._dividir_filho(nova_raiz, 0, raiz)
            self.raiz = nova_raiz
        self._inserir_nao_cheio(self.raiz, chave, registro)

    def _inserir_nao_cheio(self, no, chave, registro):
        # Insere a chave em um nó que ainda não está cheio.
        i = len(no.chaves) - 1
        # Se o nó for folha, localiza a posição correta para manter a ordem e insere a chave e o registro.
        if no.folha:
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            if i >= 0 and no.chaves[i] == chave:
                no.registros[i] = registro
            else:
                no.chaves.insert(i + 1, chave)
                no.registros.insert(i + 1, registro)
        # Caso não seja um nó folha, encontra o filho correto para inserir. Se esse filho estiver cheio, divide-o antes de continua.
        else:
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            # Se o filho está cheio (número máximo de chaves atingido), divide-o
            if len(no.filhos[i].chaves) >= self.ordem:
                self._dividir_filho(no, i, no.filhos[i])
                if chave > no.chaves[i]:
                    i += 1
            self._inserir_nao_cheio(no.filhos[i], chave, registro)

    def _dividir_filho(self, pai, i, filho):
        #  Divide um nó filho que está cheio, promovendo a chave mediana para o nó pai.
        ordem = self.ordem
        # O índice mediano é calculado para que o nó seja dividido corretamente
        meio = (ordem - 1) // 2  
        novo_no = NodaArvoreB(ordem=self.ordem, folha=filho.folha)
        
        chave_sobe = filho.chaves[meio]
        # O nó novo receberá as chaves à direita da chave mediana
        novo_no.chaves = filho.chaves[meio + 1:]
        filho.chaves = filho.chaves[:meio]
        
        if filho.folha:
            novo_no.registros = filho.registros[meio + 1:]
            filho.registros = filho.registros[:meio]
        else:
            novo_no.filhos = filho.filhos[meio + 1:]
            filho.filhos = filho.filhos[:meio + 1]
        
        pai.chaves.insert(i, chave_sobe)
        pai.filhos.insert(i + 1, novo_no)

    def remover(self, chave, no=None):
        #  Remove uma chave da árvore B, tratando casos em que a chave está em um nó folha ou em um nó interno.
        if isinstance(chave, str) and ',' in chave:
            print(f"Aviso: Operação de remoção mal formatada ignorada -> R {chave}")
            return
        if isinstance(chave, (list, tuple)):
            if len(chave) != 1:
                print(f"Aviso: Operação de remoção mal formatada ignorada -> R {chave}")
                return
            else:
                chave = chave[0]

        #  Verifica se a operação de remoção está bem formatada
        if no is None:
            no = self.raiz

        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1
        
        # Se a chave estiver em um nó folha, é simplesmente removida.
        if i < len(no.chaves) and chave == no.chaves[i]:
            # Se a chave estiver em um nó folha, é simplesmente removida.
            if no.folha:
                no.chaves.pop(i)
                if no.registros:
                    no.registros.pop(i)
            else:
                # Para remoção em nó interno, tenta usar o predecessor ou sucessor,
                # se o filho correspondente possuir chaves a mais do que o mínimo.
                min_keys = (self.ordem + 1) // 2 - 1
                if len(no.filhos[i].chaves) > min_keys:
                    pred_chave, pred_registro, no_pred = self._pegar_predecessor(no.filhos[i])
                    no.chaves[i] = pred_chave
                    if no.registros:
                        no.registros[i] = pred_registro
                    self.remover(pred_chave, no.filhos[i])
                elif len(no.filhos[i + 1].chaves) > min_keys:
                    suc_chave, suc_registro, no_suc = self._pegar_sucessor(no.filhos[i + 1])
                    no.chaves[i] = suc_chave
                    if no.registros:
                        no.registros[i] = suc_registro
                    self.remover(suc_chave, no.filhos[i + 1])
                else:
                    self._mesclar(no, i)
                    self.remover(chave, no.filhos[i])
        # Se a chave estiver em um nó interno, tenta substituí-la pelo predecessor
        # (maior chave à esquerda) ou sucessor (menor chave à direita)
        elif not no.folha:
            self.remover(chave, no.filhos[i])
        # Se a chave não estiver presente em um nó folha, encerra a operação
        else:
            return

        # Após a remoção, se o nó não for a raiz e estiver abaixo do número mínimo de chaves, balanceia
        min_keys = (self.ordem + 1) // 2 - 1
        if no != self.raiz and len(no.chaves) < min_keys:
            self._balancear_depois_remover(no)

        # Se a raiz ficar sem chaves, atualiza a raiz (reduz a altura da árvore)
        if self.raiz and not self.raiz.chaves:
            if self.raiz.filhos:
                self.raiz = self.raiz.filhos[0]
            else:
                self.raiz = None

    def _pegar_sucessor(self, no):
        # Retorna (chave, registro, nó) da menor chave na subárvore
        while not no.folha:
            no = no.filhos[0]
        if no.registros:
            return no.chaves[0], no.registros[0], no
        return no.chaves[0], None, no

    def _pegar_predecessor(self, no):
        # Retorna (chave, registro, nó) da maior chave na subárvore
        # Segue os ponteiros do último filho até chegar a um nó folha.
        while not no.folha:
            no = no.filhos[-1]
        if no.registros:
            return no.chaves[-1], no.registros[-1], no
        return no.chaves[-1], None, no

    def _mesclar(self, no, i):
        # Mescla dois nós irmãos (o filho no índice i e o filho no índice i+1) utilizando a chave separadora do nó pai.
        filho_esq = no.filhos[i]
        filho_dir = no.filhos[i + 1]
        # A chave do nó pai que separa os dois filhos é inserida no filho da esquerda
        filho_esq.chaves.append(no.chaves.pop(i))
        if no.registros:
            no.registros.pop(i)
        filho_esq.chaves.extend(filho_dir.chaves)
        if filho_esq.folha:
            filho_esq.registros.extend(filho_dir.registros)
        else:
            filho_esq.filhos.extend(filho_dir.filhos)
        no.filhos.pop(i + 1)

    def _balancear_depois_remover(self, no):
        #  Realiza o balanceamento de um nó que ficou com menos chaves do que o mínimo permitido após uma remoção.
        min_keys = (self.ordem + 1) // 2 - 1
        if no == self.raiz or len(no.chaves) >= min_keys:
            return

        pai = self._encontrar_no_pai(self.raiz, no)
        if pai is None:
            return

        indice_no = pai.filhos.index(no)

        # Tenta redistribuir com o irmão à esquerda
        if indice_no > 0:
            irmao_esq = pai.filhos[indice_no - 1]
            if len(irmao_esq.chaves) > min_keys:
                no.chaves.insert(0, pai.chaves[indice_no - 1])
                pai.chaves[indice_no - 1] = irmao_esq.chaves.pop(-1)
                if not irmao_esq.folha and irmao_esq.filhos:
                    no.filhos.insert(0, irmao_esq.filhos.pop(-1))
                return

        # Tenta redistribuir com o irmão à direita
        if indice_no < len(pai.filhos) - 1:
            irmao_dir = pai.filhos[indice_no + 1]
            if len(irmao_dir.chaves) > min_keys:
                no.chaves.append(pai.chaves[indice_no])
                pai.chaves[indice_no] = irmao_dir.chaves.pop(0)
                if not irmao_dir.folha and irmao_dir.filhos:
                    no.filhos.append(irmao_dir.filhos.pop(0))
                return

        # Se não for possível redistribuir, mescla com um dos irmãos
        if indice_no > 0:
            self._mesclar(pai, indice_no - 1)
        else:
            self._mesclar(pai, indice_no)
        # O balanceamento pode ser aplicado recursivamente, assegurando a manutenção da propriedade de mínima ocupação em toda a árvore.
        if pai != self.raiz and len(pai.chaves) < min_keys:
            self._balancear_depois_remover(pai)

    def _encontrar_no_pai(self, no, filho):
        # Localiza recursivamente o nó pai de um nó específico.
        if no is None or no.folha:
            return None
        # Percorre os nós a partir da raiz, procurando aquele que possui o nó alvo como filho.
        for f in no.filhos:
            if f == filho:
                return no
            p = self._encontrar_no_pai(f, filho)
            if p:
                return p
        return None

    def percorrer_em_largura(self):
        # Executa uma travessia em largura (BFS) da árvore, retornando a representação dos nós por nível.
        if not self.raiz:
            return []
    
        resultado = []
        fila = [self.raiz]

        # Percorre todos os nós de cada nível.
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
