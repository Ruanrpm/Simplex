def inversa_matriz(A):
    n = len(A)
    
    # Criar matriz aumentada [A | I]
    M = [linha[:] + [0]*n for linha in A]
    
    for i in range(n):
        M[i][n + i] = 1  # identidade
    
    # Gauss-Jordan com pivotamento
    for i in range(n):
        
        #  Pivotamento (trocar linha se pivô for 0)
        if M[i][i] == 0:
            for k in range(i + 1, n):
                if M[k][i] != 0:
                    M[i], M[k] = M[k], M[i]
                    break
            else:
                raise ValueError("Matriz não é invertível")
        
        pivô = M[i][i]
        
        # Normalizar linha
        for j in range(2*n):
            M[i][j] /= pivô
        
        # Zerar outras linhas
        for k in range(n):
            if k != i:
                fator = M[k][i]
                for j in range(2*n):
                    M[k][j] -= fator * M[i][j]
    
    # Extrair inversa
    inversa = [linha[n:] for linha in M]
    
    return inversa