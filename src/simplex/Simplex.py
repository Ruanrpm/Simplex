import numpy as np

class Simplex:
    def __init__(self, A, b, c, base):
        self.A = np.array(A, dtype=float) #Matrix completa
        self.b = np.array(b, dtype=float) #vetor b
        self.c = np.array(b, dtype=float) # custos
        self.base = base # índices das variáveis básicas
        self.n = len(c) #total de variaveis
        self.m = len(b) #numero de restricoes

