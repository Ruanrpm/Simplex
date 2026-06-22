from functions.inversa import inversa_matriz
from functions.laplace import determinante_laplace
from functions.mult_matriz_vetor import mult_matriz_vetor
from functions.transposta import transposta
from functions.mult_vetor_matriz import mult_vetor_matriz
EPS = 1e-9

class Simplex:
    def __init__(self, A, b, c, tipo):
        self.A = A #Matrix completa
        self.b = b #vetor b
        self.c = c # custos
        self.tipo = tipo
        self.base = []
        
        self.n = len(c) #total de variaveis
        self.m = len(b) #numero de restricoes 

        self.encontrar_base_inicial()


    # *** PASSO I ***
    def encontrar_base_inicial(self):
        base = []

        for j in range(self.n):
            coluna = [self.A[i][j] for i in range(self.m)]

            pos_um = []

            for i, valor in enumerate(coluna):

                if abs(valor - 1) < EPS:
                    pos_um.append(i)

                elif abs(valor) > EPS:
                    break

            else:
                if len(pos_um) == 1:
                    base.append(j)

        if len(base) != self.m:
            raise ValueError(
                "Nenhuma base identidade encontrada."
            )

        self.base = base


    def calcular_solucao_basica(self):
        # Validação da base
        if len(self.base) != self.m:
            raise ValueError("Base inválida: tamanho incorreto!")
        
         # Montar matriz básica       
        self.B = [[linha[j] for j in self.base] for linha in self.A]

        if determinante_laplace(self.B) == 0:
            raise ValueError("Matriz básica não é invertível")
        
        self.B_inv = inversa_matriz(self.B)
        self.x_B = mult_matriz_vetor(self.B_inv, self.b)

        nao_base = [j for j in range(self.n) if j not in self.base]
        self.x_N = [0] * len(nao_base)


    # *** PASSO II ***
    def calcular_lambda(self):
        if not hasattr(self, "B"):
            raise ValueError("Execute calculo_solucao_basica() primeiro")
        
        B_T = transposta(self.B)
        B_T_inv = inversa_matriz(B_T)

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
            lambda_T_A_N[i] - cn[i]
            for i in range(len(cn))
        ]

        return custos_reduzidos, nao_base


    def escolher_variavel(self):
        custos_reduzidos, nao_base = self.calcular_custos_relativos()

        # derterminação da variavel a entrar na base
        if self.tipo == "max":
            # escolhe o mais negativo
            menor_valor = min(custos_reduzidos)
            k = custos_reduzidos.index(menor_valor)
        else:
            # escolhe o mais positivo
            maior_valor = max(custos_reduzidos)
            k = custos_reduzidos.index(maior_valor)

        return nao_base[k]
    

    # # *** PASSO III ***
    def teste_otimalidade(self):
        custos_reduzidos, _ = self.calcular_custos_relativos()

        if self.tipo == "max":
            return all(c >= -EPS for c in custos_reduzidos)
        else:
            return all(c <= EPS for c in custos_reduzidos)
    

    # *** PASSO IV ***
    def calcular_direcao(self, k):
        # pega coluna da variável que entra
        a_k = [linha[k] for linha in self.A]

        self.y = mult_matriz_vetor(self.B_inv, a_k)
    

    # *** PASSO V ***
    def razao_minima(self):
        if all(y <= EPS for y in self.y):
            raise ValueError("O problema não tem solução ótima finita f(x) -> 'inf'")            
            
        # determinação da variavel a sair da base
        valores = [
            self.x_B[i] / self.y[i] if self.y[i] > 0 else float('inf')
            for i in range(len(self.y))
        ]
        # Indice da base que sai
        return valores.index(min(valores))

    
    # *** PASSO VI ***
    def atualizar_base(self, k):
        self.calcular_direcao(k)

        l = self.razao_minima()

        self.base[l] = k


    def iteracao(self):
            # atualizar tudo que depende da base
            self.calcular_solucao_basica()
            self.calcular_lambda()

            if self.teste_otimalidade():
                return "Solução na iteração atual é ótima"

            k = self.escolher_variavel()
            self.atualizar_base(k)

            return "continua"


    def resolver(self):
        while True:
            status = self.iteracao()

            if status == "Solução na iteração atual é ótima":
                x = [0]*self.n
                for i, bi in enumerate(self.base):
                    x[bi] = self.x_B[i]
                z = sum(self.c[i] * x[i] for i in range(self.n))
                return x, self.base, z