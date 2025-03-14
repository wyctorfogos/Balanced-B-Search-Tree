import os
import sys
from models.text_processing import ProcessamentoDados
# Exemplo de uso
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso correto: python trab2.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    entrada, saida = sys.argv[1], sys.argv[2]

    processamento = ProcessamentoDados(entrada, saida)
    processamento.ler_dados()

    # Demonstração da leitura (para teste inicial):
    print(f"Ordem da árvore: {processamento.ordem}")
    print(f"Número de operações: {processamento.num_operacoes}")
    print("Operações:")
    for op in processamento.operacoes:
        print(op)

    # Exemplo de uso da gravação (substituir pela integração futura)
    processamento.adicionar_resultado_busca(20, True)
    processamento.adicionar_resultado_busca(30, False)

    exemplo_estado_arvore = [
        "[key: 51, key: 75, ]",
        "[key: 20, key: 40, key: 45, ][key: 55, key: 60, key: 62, ][key: 77, ]"
    ]

    processamento.adicionar_estado_final_arvore(exemplo_estado_arvore)
    processamento.salvar_dados()
