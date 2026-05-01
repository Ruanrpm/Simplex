def mult_matriz_vetor(A, b):
    m = len(A)
    n = len(A[0])
    
    if len(b) != n:
        raise ValueError("Dimensões incompatíveis")
    
    resultado = [0 for _ in range(m)]
    
    for i in range(m):
        soma = 0
        for j in range(n):
            soma += A[i][j] * b[j]
        resultado[i] = soma
    
    return resultado