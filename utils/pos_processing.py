def pos_process_data(resultado_da_busca, estado_final_da_arvore):
    ## Formata os resultados da busca e a estrutura final da árvore B.
    # Saída de texto a ser entregue
    saida_formatada = ""
    
    # Desempilha a pilha
    while (resultado_da_busca.__len__() > 0):
        resultado = resultado_da_busca.top()
        
        # Adiciona o resultado da busca à saída
        saida_formatada += resultado + "\n"
        
        # Tirar o elemento do topo após obtê-lo
        resultado_da_busca.pop()

    # Monta a saída exatamente no formato pedido
    saida_formatada += "-- ARVORE B\n"
    saida_formatada += "\n".join(str(estado) for estado in estado_final_da_arvore)
    
    # Retornando a saída formatada
    return saida_formatada
