def determinante_laplace(A):
    n = len(A)
    
    # 🔹 Verificação básica
    if any(len(linha) != n for linha in A):
        raise ValueError("A matriz deve ser quadrada")
    
    # 🔹 Casos base
    if n == 1:
        return A[0][0]
    
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    
    # 🔹 Escolher melhor linha (menos zeros)
    melhor_linha = min(range(n), key=lambda i: sum(1 for x in A[i] if x != 0))
    
    det = 0
    
    for j in range(n):
        elemento = A[melhor_linha][j]
        
        if elemento == 0:
            continue  # 🔹 otimização importante
        
        # 🔹 Criar submatriz (menor)
        submatriz = []
        for i in range(n):
            if i != melhor_linha:
                nova_linha = []
                for k in range(n):
                    if k != j:
                        nova_linha.append(A[i][k])
                submatriz.append(nova_linha)
        
        # 🔹 Sinal de Laplace
        sinal = (-1) ** (melhor_linha + j)
        
        det += sinal * elemento * determinante_laplace(submatriz)
    
    return det