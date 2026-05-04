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

        self.B_inv = inversa(self.B)

        # Solução básica - vetores B\N
        self.x_B = mult_matriz_vetor(self.B_inv, self.b)

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
        A_N = [[linha[j] for j in nao_base] for linha in self.A]

        # lista lbdT*AN
        if not hasattr(self, "lambda_"):
            raise ValueError("Execute calcular_lambda primeiro")
        
        lambda_T_A_N = mult_vetor_matriz(self.lambda_, A_N)

        if len(cn) != len(lambda_T_A_N):
            raise ValueError("Erro de dimensão nos custos reduzidos")
        
        custos_reduzidos = [
            cn[i] - lambda_T_A_N[i]
            for i in range(len(cn))
        ]

        return custos_reduzidos, nao_base


    def escolher_variavel(self):
        custos_reduzidos, nao_base = self.calcular_custos_relativos()

        # derterminação da variavel a entrar na base
        k = custos_reduzidos.index(min(custos_reduzidos))
        variavel_escolhida = nao_base[k]

        return variavel_escolhida
    

    # # *** PASSO III ***
    def teste_otimalidade(self):
        custos_reduzidos, _ = self.calcular_custos_relativos()

        for i in range(len(custos_reduzidos)):
            if custos_reduzidos[i] < 0:
                return False
            
        return True
    

    # *** PASSO IV ***
    def calcular_direcao(self, k):
        # pega coluna da variável que entra
        a_k = [linha[k] for linha in self.A]

        self.y = mult_matriz_vetor(self.B_inv, a_k)
    

    # *** PASSO V ***
    def razao_minima(self):
        if all(y <= 0 for y in self.y):
            raise ValueError("O problema não tem solução ótima finita f(x) -> 'inf'")            
            
        # determinação da variavel a sair da base
        valores = [
            self.x_B[i] / self.y[i] if self.y[i] > 0 else float('inf')
            for i in range(len(self.y))
        ]
        # Indice da base que sai
        return valores.index(min(valores))

    
    # *** PASSO VI ***
    def atualizar_base(self):
        k = self.escolher_variavel()

        self.calcular_direcao(k)

        l = self.razao_minima()

        self.base[l] = k



    def iteracao(self):
            # atualizar tudo que depende da base
            self.calcular_solucao_basica()
            self.calcular_lambda()

            if self.teste_otimalidade():
                return "Solução na iteração atual é ótima"

            self.atualizar_base()
            
            return "continua"
    
    def resolver(self):
        while True:
            status = self.iteracao()

            if status == "Solução na iteração atual é ótima":
                return self.x_B, self.base