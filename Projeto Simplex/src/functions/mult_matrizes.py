def mult_matrizes(A, B):
    m = len(A)
    n = len(A[0])
    n2 = len(B)
    p = len(B[0])

    if n != n2:
        raise ValueError("Erro: Multiplicação invalida")
    
    C = [[0 for j in range(p)] for i in range(m)]

    for linhas in range(m):
        for colunas in range(p):
            soma = 0
            for k in range(n):
                soma += (A[linhas][k] * B[k][colunas])
            
            C[linhas][colunas] = soma
    
    return C