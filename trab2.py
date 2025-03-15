import sys
from utils.text_processing import ProcessamentoDados
from utils.pos_processing import pos_process_data
from models.arvore_b import ArvoreB

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso correto: python main.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    processamento = ProcessamentoDados(entrada, saida)
    processamento.ler_dados()

    print(f"Dados pré-processados: {processamento.operacoes}")

    arvore_b = ArvoreB(processamento.ordem)
    resultados_busca = []

    for op in processamento.operacoes:
        if op[0] == 'I':
            _, chave, registro = op
            arvore_b.inserir(chave)
        elif op[0] == 'R':
            _, chave = op
            arvore_b.remover(chave)
        elif op[0] == 'B':
            _, chave = op
            encontrado = arvore_b.buscar(chave)
            resultados_busca.append(
                "O REGISTRO ESTA NA ARVORE!" if encontrado else "O REGISTRO NAO ESTA NA ARVORE!"
            )

    estado_arvore = arvore_b.percorrer_em_largura()

    resultado_final = "\n".join(resultados_busca)
    resultado_final += "\n-- ARVORE B\n"
    resultado_final += "\n".join(
        ["".join(f"[key: {chave}, " for chave in no.chaves) + "]" for no in arvore_b.raiz.filhos]
    )


    print(f"\n✅ Resultados finais:\n{resultado_final}")

    processamento.salvar_dados(resultado_final)
