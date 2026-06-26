from functions.inversa import inversa_matriz
from functions.laplace import determinante_laplace
from functions.mult_matriz_vetor import mult_matriz_vetor
from functions.transposta import transposta
from functions.mult_vetor_matriz import mult_vetor_matriz
EPS = 1e-9

class Simplex:
    def __init__(self, A, b, c, tipo, ops):
        self.A = A #Matrix completa
        self.operadores = ops
        self.b = b #vetor b
        self.c = c # custos
        self.tipo = tipo
        self.base = []
        self.fase = 2
        
        self.n = len(c) #total de variaveis
        self.m = len(b) #numero de restricoes 


    # *** PASSO I ***

    def calcular_solucao_basica(self):
        self.garantir_base_inicial()

        # Validação da base
        if len(self.base) != self.m:
            raise ValueError("Base inválida: tamanho incorreto!")
        
         # Montar matriz básica       
        
        A, _, _ = self.dados_problema()

        self.B = [[linha[j] for j in self.base] for linha in A]

        if determinante_laplace(self.B) == 0:
            raise ValueError("Matriz básica não é invertível")
        
        self.B_inv = inversa_matriz(self.B)
        self.x_B = mult_matriz_vetor(self.B_inv, self.b)

        _, _, n = self.dados_problema()
        nao_base = [j for j in range(n) if j not in self.base]
        self.x_N = [0] * len(nao_base)


    # *** PASSO II ***
    def calcular_lambda(self):
        if not hasattr(self, "B"):
            raise ValueError("Execute calculo_solucao_basica() primeiro")
        
        B_T = transposta(self.B)
        B_T_inv = inversa_matriz(B_T)

        # Custos básicos
        _, c, _ = self.dados_problema()

        cb = [c[j] for j in self.base]

        # lambda
        self.lambda_ = mult_matriz_vetor(B_T_inv, cb)


    def calcular_custos_relativos(self):
        # *** custos relativos ***
        
        # Custos não básicos
        A, c, n = self.dados_problema()
        nao_base = [j for j in range(n) if j not in self.base]
        cn = [c[j] for j in nao_base]

        # matriz A não básica
        A_N = [[linha[j] for j in nao_base] for linha in A]

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
        A, _, _ = self.dados_problema()

        # pega coluna da variável que entra
        a_k = [linha[k] for linha in A]

        self.y = mult_matriz_vetor(self.B_inv, a_k)
    

    # *** PASSO V ***
    def razao_minima(self):
        if all(y <= EPS for y in self.y):
            return None # Problema ilimitado
            
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
        if l is None:
            return "ILIMITADO"

        self.base[l] = k


    def iteracao(self):
            # atualizar tudo que depende da base
            self.calcular_solucao_basica()
            self.calcular_lambda()

            if self.teste_otimalidade():
                return "Solução na iteração atual é ótima"

            k = self.escolher_variavel()

            status = self.atualizar_base(k)
            if status == "ILIMITADO":
                return "ILIMITADO"

            return "continua"
         


#==================
# IMPLEMENTAÇÃO INICIAL DA FAZE I
#==================    

    def preprocessar(self):
        """
        Normaliza o problema para forma padrão do simplex.
        """

        #  MAX -> MIN
        if self.tipo == "max":
            self.c = [-ci for ci in self.c]
            self.tipo = "min"

        #  Garantir b_i >= 0
        for i in range(len(self.b)):
            if self.b[i] < 0:
                self.b[i] *= -1
                # multiplica linha inteira por -1
                self.A[i] = [-aij for aij in self.A[i]]

                # Quando multiplica por -1, o sinal da restricao tambem vira.
                if self.operadores[i] == "<=":
                    self.operadores[i] = ">="
                elif self.operadores[i] == ">=":
                    self.operadores[i] = "<="
    
    def construir_fase1(self):
        """
        Constrói o problema auxiliar da Fase I.
        """
        self.fase = 1

        A = self.A
        b = self.b 
        operadores = self.operadores

        m = len(A)
        n = len(A[0])

        self.A_fase1 = []
        self.base = []
        self.nbase = list(range(n))
        self.artificiais_add = []

        indice_artificial = n

        # calculo do número de restrições >= ou =
        num_artificiais = 0
        for op in operadores:
            if op in [">=", "="]:
                num_artificiais += 1

        # verifica qual caso será utilizado
        casoA = False
        if num_artificiais > 1:
            casoA = True
            num_artificiais = m
            

        # Controi a matriz da fase I & monta base inicial
        for i in range(m):
            linha = A[i].copy()

            # por padrão indica que a restrição atual não possui artificial
            self.artificiais_add.append(False)

            # Todas a linhas recebem espaço para as artificiais
            linha.extend([0] * num_artificiais)

            # caso precise de artificial:
            if casoA or operadores[i] in [">=", "="]:
                pos = indice_artificial

                linha[pos] = 1  

                self.base.append(pos)
                self.artificiais_add[i] = True

                indice_artificial += 1

            else:
                # coloca as variaveis de folga na base, caso não precise de artificial
                
                # Cria uma matriz temporária, como se a linha atual já tivesse sido adicionada.
                var_folga = self.encontrar_coluna_base(self.A, i)
                if var_folga is None:
                    return "INFACTIVEL"
                self.base.append(var_folga)

            self.A_fase1.append(linha)

        # vetor c da fase I
        total_vars = len(self.A_fase1[0])
        self.c_fase1 = [0] * total_vars

        if casoA:
            # Coloca artificiais em todas as retrições
            for i in range(m):
                self.c_fase1[n + i] = 1
        else:
            # coloca artificiais apenas nas != <=
            for i in range(m):
                if self.artificiais_add[i]:
                    self.c_fase1[n + sum(self.artificiais_add[:i])] = 1

    # Usado para encontrar a coluna identidade da restrição
    def encontrar_coluna_base(self, A, linha):
        # Procura uma coluna que seja idenidade
        for j in range(len(A[0])):

            if A[linha][j] != 1:
                continue

            identidade = True

            # percorre todas as linhas da matriz
            for i in range(len(A)):
                if i == linha:
                    esperado = 1 
                else:
                    esperado = 0

                # Ve se tem valor esperado
                if A[i][j] != esperado:
                    identidade = False
                    break

            if identidade:
                return j

        return None

    def garantir_base_inicial(self):
        if self.base or self.fase == 1:
            return

        for i in range(self.m):
            var_folga = self.encontrar_coluna_base(self.A, i)
            if var_folga is None:
                raise ValueError("Base inicial nao encontrada. Use Fase I.")
            self.base.append(var_folga)
    
    # Para não ter que verificar a todo momento se é fase I ou II
    def dados_problema(self):
        # Retorna a matriz A, vetor de custos c e número de variáveis da fase atual.

        if self.fase == 1:
            return self.A_fase1, self.c_fase1, len(self.A_fase1[0])
        else:
            return self.A, self.c, self.n

    def resolver(self):
        while True:

            status = self.iteracao()

            if status == "Solução na iteração atual é ótima":

                # Se estiver na Fase I
                if self.fase == 1:

                    self.primeira_artificial = self.n

                    # Pega o valor e o indice do vetor b
                    for i, coluna in enumerate(self.base):

                        if coluna >= self.primeira_artificial and self.x_B[i] > EPS:
                            return "INFACTIVEL", self.base, None

                    self.remover_artificiais_base()
                    # Se fase I OK, então
                    self.fase = 2

                    # RESET COMPLETO DO ESTADO PARA FASE II
                    self.calcular_solucao_basica()
                    self.calcular_lambda()
                    continue


                # Fase II 
                _, c, n = self.dados_problema()

                x = [0] * n
                # Coloca o valor da variavel basica no vetor de solução
                for i, b_i in enumerate(self.base):
                    x[b_i] = self.x_B[i]

                z = sum(c[i] * x[i] for i in range(n))

                return x, self.base, z

            if status == "ILIMITADO":

                _, _, n = self.dados_problema()

                x = [0] * n

                return "ILIMITADO", self.base, 0.0

    def remover_artificiais_base(self):

        for i, coluna_base in enumerate(self.base):
            if abs(self.x_B[i]) > EPS:
                continue

            if coluna_base < self.primeira_artificial:
                continue

            encontrou = False

            for j in range(self.primeira_artificial):

                if j in self.base:
                    continue

                if abs(self.A_fase1[i][j]) > EPS:

                    self.base[i] = j
                    encontrou = True
                    break

            
            if not encontrou:
                # Remove a linha da matriz
                self.A_fase1.pop(i)

                # Remove o termo independente correspondente
                self.b.pop(i)

                # Remove a variável da base
                self.base.pop(i)

                # Atualiza o número de restrições
                self.m -= 1

                print(f"Restrição {i} removida por redundância.")

                break

    def precisa_fase1(self):
        for op in self.operadores:
            if op == ">=" or op == ">" or op == "=":
                return True

        return False
