def transposta(M):
    linhas = len(M)
    colunas = len(M[0])
    
    T = [[0 for _ in range(linhas)] for _ in range(colunas)]
    
    for i in range(linhas):
        for j in range(colunas):
            T[j][i] = M[i][j]
    
    return T