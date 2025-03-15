from models.ABB import ABB

if __name__ == "__main__":
    # Criando a ABB com raiz 50
    raiz = ABB(50)
    raiz = raiz.insere_recursivo(raiz, 30)
    raiz = raiz.insere_recursivo(raiz, 70)
    raiz = raiz.insere_recursivo(raiz, 20)
    raiz = raiz.insere_recursivo(raiz, 40)
    raiz = raiz.insere_recursivo(raiz, 60)
    raiz = raiz.insere_recursivo(raiz, 80)

    print("🌳 ABB antes da remoção:")
    print(f"Raiz: {raiz}")

    # Removendo uma folha
    raiz = raiz.remover_recursivo(raiz, 20)
    print("✅ Após remover 20 (folha):")
    print(f"Raiz: {raiz}")

    # Removendo um nó com um filho
    raiz = raiz.remover_recursivo(raiz, 30)
    print("✅ Após remover 30 (nó com um filho):")
    print(f"Raiz: {raiz}")

    # Removendo um nó com dois filhos
    raiz = raiz.remover_recursivo(raiz, 50)
    print("✅ Após remover 50 (nó com dois filhos):")
    print(f"Raiz: {raiz}")
