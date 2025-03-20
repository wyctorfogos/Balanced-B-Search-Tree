# Wyctor Fogos da Rocha
# matrícula: 2024230514

from .no_arvore_b import NodaArvoreB

class ArvoreB:
    def __init__(self, ordem):
        self.ordem = ordem
        self.raiz = NodaArvoreB(ordem)

    def buscar(self, chave, no=None):
        if no is None:
            no = self.raiz
        i = 0
        while ((i < len(no.chaves)) and (chave > no.chaves[i])):
            i += 1

        # Encontrando a chave desejada
        if i < len(no.chaves) and chave == no.chaves[i]:
            return True  

        # Senão encontrar a chave
        if no.folha:
            return False 

        return self.buscar(chave, no.filhos[i])

    def inserir(self, chave, registro):
        raiz = self.raiz
        if len(raiz.chaves) == self.ordem - 1:
            nova_raiz = NodaArvoreB(self.ordem, folha=False)
            nova_raiz.filhos.append(raiz)
            self._dividir_filho(nova_raiz, 0, raiz)
            self.raiz = nova_raiz
        self._inserir_nao_cheio(self.raiz, chave, registro)

    def _inserir_nao_cheio(self, no, chave, registro):
        i = len(no.chaves) - 1
        if no.folha:
            # Encontrar a posição correta para inserção
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            if i >= 0 and no.chaves[i] == chave:
                no.registros[i] = registro  # Atualiza registro (não insere nova chave)
            else:
                no.chaves.insert(i + 1, chave)
                no.registros.insert(i + 1, registro)
        else:
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            if len(no.filhos[i].chaves) == self.ordem - 1:
                self._dividir_filho(no, i, no.filhos[i])
                if chave > no.chaves[i]:
                    i += 1
            self._inserir_nao_cheio(no.filhos[i], chave, registro)


    def _dividir_filho(self, pai, i, filho):
        ordem = self.ordem
        meio = (ordem // 2) - 1 # (ordem-1)//2 #(ordem // 2) - 1 

        novo_no = NodaArvoreB(ordem=self.ordem, folha=filho.folha)

        chave_sobe = filho.chaves[meio]

        novo_no.chaves = filho.chaves[meio+1:]
        filho.chaves = filho.chaves[:meio]

        if filho.folha:
            novo_no.registros = filho.registros[meio+1:]
            filho.registros = filho.registros[:meio+1]
        else:
            novo_no.filhos = filho.filhos[meio+1:]
            filho.filhos = filho.filhos[:meio+1]

        pai.chaves.insert(i, chave_sobe)
        pai.filhos.insert(i + 1, novo_no)

    def remover(self, chave, no=None):
        if no is None:
            no = self.raiz

        i = 0
        while ((i < len(no.chaves)) and (chave > no.chaves[i])):
            i += 1

        if i < len(no.chaves) and chave == no.chaves[i]:
            # Chave encontrada  
            if no.folha:
                no.chaves.pop(i)
                if no.registros:
                    # Removemos apenas se houver registros
                    no.registros.pop(i)  
            else:
                sucessor_chave, sucessor_registro = self._pegar_sucessor(no.filhos[i+1])
                no.chaves[i] = sucessor_chave  
                # Substitui a chave removida pelo sucessor
                if sucessor_registro is not None:
                    if i < len(no.registros):  
                        # Apenas se houver registro
                        no.registros[i] = sucessor_registro 
                    else:
                        # Caso contrário, adicionamos
                        no.registros.append(sucessor_registro)  
                # Remove o sucessor do nó folha
                self.remover(sucessor_chave, no.filhos[i+1])  
        elif not no.folha:
            self.remover(chave, no.filhos[i])

        ## Verifica se precisa balancear
        # Como foi especificado no trabalho, pra se manter a árvore balanceada é verificado a quantidade de chaves pra cada nó
        # É preciso verificar a quantidade de chaves por Nós de um ramo após a remoção de um Nó
        if (len(no.chaves) < (self.ordem // 2)-1) or (len(no.chaves)> (self.ordem-1)):
            self._balancear_depois_remover(no)

        # Se a raiz ficou vazia, ajustamos a raiz
        if self.raiz and not self.raiz.chaves and self.raiz.filhos:
            self.raiz = self.raiz.filhos[0]


    def _balancear_depois_remover(self, no):
        if no == self.raiz or len(no.chaves) >= (self.ordem - 1) // 2:
            return  # Nenhuma ação necessária

        pai = self._encontrar_pai(self.raiz, no)
        if pai is None:
            return

        indice_no = pai.filhos.index(no)

        # Redistribuir com irmão esquerdo se possível
        if indice_no > 0:
            irmao_esq = pai.filhos[indice_no - 1]
            if len(irmao_esq.chaves) > (self.ordem - 1) // 2:
                no.chaves.insert(0, pai.chaves[indice_no - 1])
                pai.chaves[indice_no - 1] = irmao_esq.chaves.pop(-1)
                if not irmao_esq.folha:
                    no.filhos.insert(0, irmao_esq.filhos.pop(-1))
                return

        # Redistribuir com irmão direito se possível
        if indice_no < len(pai.filhos) - 1:
            irmao_dir = pai.filhos[indice_no + 1]
            if len(irmao_dir.chaves) > (self.ordem - 1) // 2:
                no.chaves.append(pai.chaves[indice_no])
                pai.chaves[indice_no] = irmao_dir.chaves.pop(0)
                if not irmao_dir.folha:
                    no.filhos.append(irmao_dir.filhos.pop(0))
                return

        # Se não foi possível redistribuir, faz a fusão
        if indice_no > 0:
            irmao_esq = pai.filhos[indice_no - 1]
            irmao_esq.chaves.append(pai.chaves.pop(indice_no - 1))
            irmao_esq.chaves.extend(no.chaves)
            if not no.folha:
                irmao_esq.filhos.extend(no.filhos)
            pai.filhos.pop(indice_no)
        else:
            irmao_dir = pai.filhos[indice_no + 1]
            no.chaves.append(pai.chaves.pop(indice_no))
            no.chaves.extend(irmao_dir.chaves)
            if not irmao_dir.folha:
                no.filhos.extend(irmao_dir.filhos)
            pai.filhos.pop(indice_no + 1)

        # Verifica recursivamente se o pai precisa balancear após fusão
        if len(pai.chaves) < (self.ordem - 1) // 2 and pai != self.raiz:
            self._balancear_depois_remover(pai)

        ## Atualiza a raiz caso fique vazia
        #if self.raiz and not self.raiz.chaves and self.raiz.filhos:
        #    self.raiz = self.raiz.filhos[0]

    def _pegar_sucessor(self, no):
        """ Retorna a chave e registro do menor valor da subárvore direita """
        while not no.folha:
            no = no.filhos[0]  # O menor valor está no filho mais à esquerda

        # Verifica se há registros antes de acessar
        if no.registros:
            return no.chaves[0], no.registros[0]
        return no.chaves[0], None  # Retorna None se não houver registro associado


    def _encontrar_pai(self, no, filho):
        if no is None or no.folha:
            return None
        for i, f in enumerate(no.filhos):
            if f == filho:
                return no
            p = self._encontrar_pai(f, filho)
            if p:
                return p
        return None

    def percorrer_em_largura(self):
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
    
