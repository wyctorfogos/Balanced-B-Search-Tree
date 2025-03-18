import sys
import os
from models.arvore_b import ArvoreB
from utils.text_processing import ProcessamentoDados

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
    resultados_busca = []

    for op in processamento.operacoes:
        try:
            op_name = op[0]

            if op_name == 'I':
                chave = int(op[1])
                registro = int(op[2])
                arvore_b.inserir(chave, registro)

            elif op_name == 'R':
                # Usa apenas o primeiro token após 'R' como chave, mesmo que haja tokens extras.
                chave = int(op[1])
                arvore_b.remover(chave)

            elif op_name == 'B':
                chave = int(op[1])
                encontrado = arvore_b.buscar(chave)
                resultado = "O REGISTRO ESTA NA ARVORE!" if encontrado else "O REGISTRO NAO ESTA NA ARVORE!"
                resultados_busca.append(resultado)
        except Exception as e:
            print(f"Erro durante o processamento: {e}\n")


    # Ajeitar a saída como esperado 
    estado_arvore = arvore_b.percorrer_em_largura()

    # Monta a saída exatamente no formato pedido
    saida_formatada = "\n".join(resultados_busca)
    saida_formatada += "\n-- ARVORE B\n"
    saida_formatada += "\n".join(estado_arvore)

    print(f"{saida_formatada}\n")
    processamento.salvar_dados(saida_formatada)