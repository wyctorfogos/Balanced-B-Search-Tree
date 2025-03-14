import os
import sys
from utils.text_processing import ProcessamentoDados
from utils.pos_processing import pos_process_data
from models.tad_arvore_b import ArvoreB

if __name__ == '__main__':
    # Verifica se o número correto de argumentos foi passado
    if len(sys.argv) != 3:
        print("Uso correto: python main.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    # Verifica se o arquivo de entrada existe
    if not os.path.exists(entrada):
        print(f"Erro: O arquivo {entrada} não foi encontrado.")
        sys.exit(1)

    # Processa os dados do arquivo de entrada
    processamento = ProcessamentoDados(entrada, saida)
    processamento.ler_dados()

    # Inicializa a árvore B com a ordem especificada
    arvore_b = ArvoreB(processamento.ordem)

    resultados_busca = []

    # Executa as operações especificadas no arquivo de entrada
    for op in processamento.operacoes:
        if op[0] == 'I':  # Inserção
            _, chave, registro = op
            arvore_b.inserir(chave, registro)

        elif op[0] == 'R':  # Remoção
            _, chave = op
            arvore_b.remover(chave)

        elif op[0] == 'B':  # Busca
            _, chave = op
            encontrado = arvore_b.buscar(chave)
            resultado = "O REGISTRO ESTA NA ARVORE!" if encontrado else "O REGISTRO NAO ESTA NA ARVORE!"
            resultados_busca.append(resultado)

    # Obtém a estrutura final da árvore B em largura
    estado_arvore = arvore_b.percorrer_em_largura()

    print(f"Estado da arvore: {estado_arvore}\n")
    print(f"Resultados da busca: {resultados_busca}\n")

    # Ordenar os dados antes de serem salvos
    resultados_busca = pos_process_data(resultado_da_busca=resultados_busca, estado_final_da_arvore=estado_arvore)

    # Resultado dos dados estruturados
    print(f"Resultados: \n{resultados_busca}\n")
    
    # Salva os dados da busca e o estado final da árvore no arquivo de saída
    processamento.salvar_dados(resultados_busca)
