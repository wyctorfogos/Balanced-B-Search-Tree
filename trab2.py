# Wyctor Fogos da Rocha
# matrícula: 2024230514

import sys
import os
from models.arvore_b import ArvoreB
from models.tad_pilha import TadPilha
from utils.text_processing import ProcessamentoDados
from utils.pos_processing import pos_process_data


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python main.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    entrada, saida = sys.argv[1], sys.argv[2]

    if not os.path.exists(entrada):
        print(f"Erro: O arquivo '{entrada}' não foi encontrado.")
        sys.exit(1)

    processamento = ProcessamentoDados(entrada, saida)
    processamento.ler_dados()

    arvore_b = ArvoreB(processamento.ordem)
    # resultados_busca = []
    resultados_busca = TadPilha()

    for op in processamento.operacoes:
        try:
            op_name = op[0]

            if op_name == 'I':
                chave = int(op[1])
                registro = int(op[2])
                arvore_b.inserir(chave, registro)

            elif op_name == 'R':
                chave = int(op[1])
                arvore_b.remover(chave)

            elif op_name == 'B':
                chave = int(op[1])
                encontrado = arvore_b.buscar(chave)
                resultado = "O REGISTRO ESTA NA ARVORE!" if encontrado else "O REGISTRO NAO ESTA NA ARVORE!"
                resultados_busca.push(resultado)
        except Exception as e:
            print(f"Erro durante o processamento: {e}\n")


    # Ajeitar a saída como esperado 
    estado_arvore = arvore_b.percorrer_em_largura()
    
    # Pré processa os dados com os resuldados em Pilha
    ##  Função usada para desempilhar os dados e salvar 
    saida_pos_processados = pos_process_data(resultado_da_busca = resultados_busca, estado_final_da_arvore=estado_arvore)

    print(f"{saida_pos_processados}\n")
    processamento.salvar_dados(saida_pos_processados)