def pos_process_data(resultado_da_busca, estado_final_da_arvore):
    """
    Formata os resultados da busca e a estrutura final da árvore B.
    
    :param resultado_da_busca: Lista de strings com resultados da busca na árvore.
    :param estado_final_da_arvore: Lista representando a estrutura da árvore B (pode conter listas aninhadas).
    :return: String formatada com os resultados seguidos da árvore formatada.
    """

    # Garantindo que `resultado_da_busca` seja uma lista de strings válidas
    if not isinstance(resultado_da_busca, list) or not all(isinstance(x, str) for x in resultado_da_busca):
        raise ValueError("resultado_da_busca deve ser uma lista de strings")

    # Se algum elemento dentro de `estado_final_da_arvore` for uma lista, converta-o para string
    estado_final_da_arvore = [str(element) if not isinstance(element, str) else element for element in estado_final_da_arvore]

    # Formatando os resultados da busca
    resultados_formatados = "\n".join(resultado_da_busca) + "\n"

    # Construindo a representação da árvore corretamente
    estrutura_arvore = "-- ARVORE B\n" + "\n".join(estado_final_da_arvore)

    # Retornando a saída formatada
    return resultados_formatados + estrutura_arvore