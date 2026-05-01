from functions import inversa, laplace, mult_matriz_vetor, transposta, mult_vetor_matriz

class Simplex:
    def __init__(self, A, b, c, base):
        self.A = A #Matrix completa
        self.b = b #vetor b
        self.c = c # custos
        self.base = base # índices das variáveis básicas
        
        self.n = len(c) #total de variaveis
        self.m = len(b) #numero de restricoes


    

    # *** PASSO I ***
    def calcular_solucao_basica(self):
        # Validação da base
        if len(self.base) != self.m:
            raise ValueError("Base inválida: tamanho incorreto!")
        
         # Montar matriz básica       
        self.B = [[linha[j] for j in self.base] for linha in self.A]

        if laplace(self.B) == 0:
            raise ValueError("Matriz básica tem determinante 0. Não é invertível!")

        B_inv = inversa(self.B)

        # Solução básica - vetores B\N
        self.x_B = mult_matriz_vetor(B_inv, self.b)

        nao_base = [j for j in range(self.n) if j not in self.base]
        self.x_N = [0] * len(nao_base)


    # *** PASSO II ***
    def calcular_lambda(self):
        if not hasattr(self, "B"):
            raise ValueError("Execute calculo_solucao_basica() primeiro")
        
        B_T = transposta(self.B)
        B_T_inv = inversa(B_T)

        # Custos básicos
        cb = [self.c[j] for j in self.base]

        # lambda
        self.lambda_ = mult_matriz_vetor(B_T_inv, cb)


    def calcular_custos_relativos(self):
        # *** custos relativos ***
        
        # Custos não básicos
        nao_base = [j for j in range(self.n) if j not in self.base]
        cn = [self.c[j] for j in nao_base]

        # matriz A não básica
        self.A_N = [[linha[j] for j in nao_base] for linha in self.A]

        # lista lbdT*AN
        if not hasattr(self, "lambda_"):
            raise ValueError("Execute calcular_lambda primeiro")
        
        lambda_T_A_N = mult_vetor_matriz(self.lambda_, self.A_N)

        if len(cn) != len(lambda_T_A_N):
            raise ValueError("Erro de dimensão nos custos reduzidos")
        
        custos_reduzidos = [
            cn[i] - lambda_T_A_N[i]
            for i in range(len(cn))
        ]

        return custos_reduzidos, nao_base


    def escolher_variavel(self):
        custos_reduzidos, nao_base = self.calcular_custos_relativos()

        # *** derterminação da variavel a entrar na base
        k = custos_reduzidos.index(min(custos_reduzidos))
        variavel_escolhida = nao_base[k]

        return variavel_escolhida
    

    # # *** PASSO III ***