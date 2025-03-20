# Wyctor Fogos da Rocha
# matrícula: 2024230514

import sys

class ProcessamentoDados:
    def __init__(self, arquivo_entrada, arquivo_saida):
        self.arquivo_entrada = arquivo_entrada
        self.arquivo_saida = arquivo_saida
        self.ordem = None
        self.num_operacoes = None
        self.operacoes = []
        self.resultados = []

    def ler_dados(self):
        try:
            with open(self.arquivo_entrada, 'r') as arquivo:
                linhas = [linha.strip() for linha in arquivo if linha.strip()]

                self.ordem = int(linhas[0])
                self.num_operacoes = int(linhas[1])

                for linha in linhas[2:]:
                    tipo_operacao = linha[0]
                    conteudo = linha[1:].strip()

                    if tipo_operacao == 'I':
                        chave, registro = map(int, conteudo.split(','))
                        self.operacoes.append(('I', chave, registro))

                    elif tipo_operacao == 'R':
                        # Divide o conteúdo e remove espaços extras
                        elementos = [elem.strip() for elem in conteudo.split(',')]
                        
                        if len(elementos) >= 2:
                            print(f"Aviso: Operação de remoção mal formatada ignorada -> {linha}")
                            continue  # Ignora a operação mal formatada
                        else:
                            chave = int(elementos[0])  # Usa o único valor presente
                            self.operacoes.append(('R', chave))

                    elif tipo_operacao == 'B':
                        chave = int(conteudo)
                        self.operacoes.append(('B', chave))

        except FileNotFoundError:
            print(f"Erro: arquivo '{self.arquivo_entrada}' não encontrado.")
            sys.exit(1)
        except Exception as e:
            print(f"Erro durante leitura do arquivo: {e}")
            sys.exit(1)


    def adicionar_resultado_busca(self, chave, encontrado):
        if encontrado:
            self.resultados.append("O REGISTRO ESTA NA ARVORE!")
        else:
            self.resultados.append("O REGISTRO NAO ESTA NA ARVORE!")

    def adicionar_estado_final_arvore(self, estado_arvore):
        self.resultados.append("\n-- ARVORE B")
        self.resultados.extend(estado_arvore)

    def salvar_dados(self, resultados_pos_processados):
        try:
            with open(self.arquivo_saida, 'w') as arquivo:
                arquivo.write(resultados_pos_processados)
        except Exception as e:
            print(f"Erro durante escrita do arquivo: {e}")
            sys.exit(1)