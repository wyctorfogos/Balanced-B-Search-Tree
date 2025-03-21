# Wyctor Fogos da Rocha
# matrícula: 2024230514

from models.arvore_b import ArvoreB

if __name__ == "__main__":
    arvore = ArvoreB(4)
    for chave in [10, 20, 5, 6, 12, 30, 7, 17]:
        arvore.inserir(chave)

    print("Árvore B em largura antes da remoção:")
    print("\n".join(arvore.percorrer_em_largura()))

    print("\nBusca por 12:", arvore.buscar(12))
    print("Busca por 40:", arvore.buscar(40))

    arvore.remover(12)
    arvore.remover(5)

    print("\nÁrvore B em largura após remover 12 e 5:")
    print("\n".join(arvore.percorrer_em_largura()))
