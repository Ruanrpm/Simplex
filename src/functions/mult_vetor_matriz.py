def mult_vetor_matriz(v, M):
    m = len(M)       # linhas
    n = len(M[0])    # colunas
    
    if len(v) != m:
        raise ValueError("Dimensões incompatíveis")
    
    resultado = [0 for _ in range(n)]
    
    for j in range(n):
        soma = 0
        for i in range(m):
            soma += v[i] * M[i][j]
        resultado[j] = soma
    
    return resultado