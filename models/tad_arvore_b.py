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
        """Insere uma chave e seu registro na árvore."""
        # Verifica se a chave já existe e atualiza o registro
        no = self.raiz
        indice = self._encontrar_indice_chave(no, chave)
        
        # Se encontrar a chave, apenas atualiza o registro
        if indice != -1:
            no.registros[indice] = registro
            return
            
        # Caso contrário, insere normalmente
        raiz = self.raiz
        if len(raiz.chaves) == self.ordem - 1:
            nova_raiz = NodaArvoreB(self.ordem, folha=False)
            nova_raiz.filhos.append(raiz)
            self._dividir_filho(nova_raiz, 0, raiz)
            self.raiz = nova_raiz
        self._inserir_nao_cheio(self.raiz, chave, registro)

    def _encontrar_indice_chave(self, no, chave):
        """Encontra o índice da chave em um nó, ou retorna -1 se não encontrar."""
        for i, k in enumerate(no.chaves):
            if k == chave:
                return i
        return -1

    def _dividir_filho(self, pai, i, filho):
        """Divide um filho que está cheio."""
        ordem = self.ordem
        novo_no = NodaArvoreB(ordem, filho.folha)
        meio = (ordem - 1) // 2  # Calcula o índice médio corretamente
        
        # Transfere metade das chaves/registros para o novo nó
        novo_no.chaves = filho.chaves[meio + 1:]
        novo_no.registros = filho.registros[meio + 1:]
        
        # Se não for folha, transfere os filhos correspondentes
        if not filho.folha:
            novo_no.filhos = filho.filhos[meio + 1:]
            filho.filhos = filho.filhos[:meio + 1]
        
        # Promove a chave do meio para o pai
        pai.chaves.insert(i, filho.chaves[meio])
        pai.registros.insert(i, filho.registros[meio])
        pai.filhos.insert(i + 1, novo_no)
        
        # Atualiza o filho original
        filho.chaves = filho.chaves[:meio]
        filho.registros = filho.registros[:meio]

    def _inserir_nao_cheio(self, no, chave, registro):
        """Insere em um nó que não está cheio."""
        i = len(no.chaves) - 1
        
        if no.folha:
            # Insere na posição correta no nó folha
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            no.chaves.insert(i + 1, chave)
            no.registros.insert(i + 1, registro)
        else:
            # Encontra o filho correto para descer
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            
            # Se o filho estiver cheio, divide-o primeiro
            if len(no.filhos[i].chaves) == self.ordem - 1:
                self._dividir_filho(no, i, no.filhos[i])
                if chave > no.chaves[i]:
                    i += 1
            
            # Continua a inserção recursivamente
            self._inserir_nao_cheio(no.filhos[i], chave, registro)

    def remover(self, chave):
        """Remove uma chave da árvore."""
        if not self.raiz:
            return False
            
        resultado = self._remover_chave(self.raiz, chave)
        
        # Se a raiz ficou vazia e tem filhos, ajusta a raiz
        if len(self.raiz.chaves) == 0 and not self.raiz.folha:
            self.raiz = self.raiz.filhos[0]
            
        return resultado

    def _remover_chave(self, no, chave):
        """Remove uma chave de um nó específico ou seus descendentes."""
        minimo = self.ordem // 2
        
        # Encontra a posição da chave no nó
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1
            
        # Caso 1: A chave está neste nó
        if i < len(no.chaves) and no.chaves[i] == chave:
            # Caso 1a: Nó é folha
            if no.folha:
                no.chaves.pop(i)
                no.registros.pop(i)
                return True
                
            # Caso 1b: Nó interno
            else:
                # Caso 1b.1: Predecessor
                if len(no.filhos[i].chaves) >= minimo:
                    # Substitui pela chave predecessor
                    predecessor = self._pegar_predecessor(no.filhos[i])
                    no.chaves[i] = predecessor[0]
                    no.registros[i] = predecessor[1]
                    # Remove o predecessor recursivamente
                    return self._remover_chave(no.filhos[i], predecessor[0])
                    
                # Caso 1b.2: Sucessor
                elif len(no.filhos[i + 1].chaves) >= minimo:
                    # Substitui pela chave sucessor
                    sucessor = self._pegar_sucessor(no.filhos[i + 1])
                    no.chaves[i] = sucessor[0]
                    no.registros[i] = sucessor[1]
                    # Remove o sucessor recursivamente
                    return self._remover_chave(no.filhos[i + 1], sucessor[0])
                    
                # Caso 1b.3: Fusão com filho
                else:
                    self._fundir_nos(no, i)
                    return self._remover_chave(no.filhos[i], chave)
                    
        # Caso 2: A chave não está neste nó
        else:
            # Caso 2a: Chegamos a uma folha sem encontrar a chave
            if no.folha:
                return False
                
            # Flag para indicar se estamos no último filho
            ultimo_filho = (i == len(no.chaves))
            
            # Caso 2b: Garantir que o filho tenha pelo menos minimo chaves
            if len(no.filhos[i].chaves) < minimo:
                self._preencher_filho(no, i)
                
            # Se o último filho se fundiu com o anterior
            if ultimo_filho and i > len(no.chaves):
                return self._remover_chave(no.filhos[i-1], chave)
            else:
                return self._remover_chave(no.filhos[i], chave)
    
    def _pegar_predecessor(self, no):
        """Encontra a maior chave na subárvore esquerda."""
        while not no.folha:
            no = no.filhos[-1]
        return (no.chaves[-1], no.registros[-1])
        
    def _pegar_sucessor(self, no):
        """Encontra a menor chave na subárvore direita."""
        while not no.folha:
            no = no.filhos[0]
        return (no.chaves[0], no.registros[0])
        
    def _fundir_nos(self, no, indice):
        """Funde o filho[indice] com filho[indice+1]."""
        filho = no.filhos[indice]
        irmao = no.filhos[indice + 1]
        
        # Move a chave de separação do nó pai para o filho
        filho.chaves.append(no.chaves[indice])
        filho.registros.append(no.registros[indice])
        
        # Copia todas as chaves do irmão para o filho
        filho.chaves.extend(irmao.chaves)
        filho.registros.extend(irmao.registros)
        
        # Se não for folha, copia os filhos também
        if not filho.folha:
            filho.filhos.extend(irmao.filhos)
            
        # Remove a chave e o filho direito do nó pai
        no.chaves.pop(indice)
        no.registros.pop(indice)
        no.filhos.pop(indice + 1)
        
    def _preencher_filho(self, no, indice):
        """Garante que filho[indice] tenha pelo menos minimo chaves."""
        minimo = self.ordem // 2
        
        # Caso 1: Pegar do irmão esquerdo
        if indice != 0 and len(no.filhos[indice - 1].chaves) >= minimo:
            self._pegar_do_anterior(no, indice)
            
        # Caso 2: Pegar do irmão direito
        elif indice != len(no.chaves) and len(no.filhos[indice + 1].chaves) >= minimo:
            self._pegar_do_proximo(no, indice)
            
        # Caso 3: Fundir com um irmão
        else:
            if indice != len(no.chaves):
                self._fundir_nos(no, indice)
            else:
                self._fundir_nos(no, indice - 1)
                
    def _pegar_do_anterior(self, no, indice):
        """Pega uma chave do irmão anterior e a coloca no filho[indice]."""
        filho = no.filhos[indice]
        irmao = no.filhos[indice - 1]
        
        # Move a chave pai para o início do filho
        filho.chaves.insert(0, no.chaves[indice - 1])
        filho.registros.insert(0, no.registros[indice - 1])
        
        # Move a última chave do irmão para o pai
        no.chaves[indice - 1] = irmao.chaves.pop()
        no.registros[indice - 1] = irmao.registros.pop()
        
        # Se não for folha, move o último filho do irmão para o filho
        if not filho.folha:
            filho.filhos.insert(0, irmao.filhos.pop())
            
    def _pegar_do_proximo(self, no, indice):
        """Pega uma chave do irmão seguinte e a coloca no filho[indice]."""
        filho = no.filhos[indice]
        irmao = no.filhos[indice + 1]
        
        # Move a chave pai para o final do filho
        filho.chaves.append(no.chaves[indice])
        filho.registros.append(no.registros[indice])
        
        # Move a primeira chave do irmão para o pai
        no.chaves[indice] = irmao.chaves.pop(0)
        no.registros[indice] = irmao.registros.pop(0)
        
        # Se não for folha, move o primeiro filho do irmão para o filho
        if not irmao.folha:
            filho.filhos.append(irmao.filhos.pop(0))

    def percorrer_em_largura(self):
        """Percorre a árvore em largura e retorna uma representação em string."""
        if not self.raiz:
            return []
            
        resultado = []
        nivel_atual = [self.raiz]
        
        while nivel_atual:
            texto_nivel = []
            proximo_nivel = []
            
            for no in nivel_atual:
                chaves_str = ""
                for i in range(len(no.chaves)):
                    chaves_str += f"key: {no.chaves[i]}, "
                texto_nivel.append(f"[{chaves_str}]")
                
                # Adiciona filhos não vazios ao próximo nível
                if not no.folha:
                    for filho in no.filhos:
                        if filho:
                            proximo_nivel.append(filho)
            
            resultado.append("".join(texto_nivel))
            nivel_atual = proximo_nivel
            
        return resultado