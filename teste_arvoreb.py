from models.arvore_b import ArvoreB

if __name__ == "__main__":
    arvore = ArvoreB(ordem=4)

    for chave in [10, 20, 5, 6, 12, 30, 7, 17]:
        arvore.inserir(chave)

    print("🌳 Antes da remoção:")
    print("\n".join(arvore.percorrer_em_largura()))

    arvore.remover(6)
    arvore.remover(17)

    print("\n🗑️ Após remoção das chaves 6 e 17:")
    print("\n".join(arvore.percorrer_em_largura()))
