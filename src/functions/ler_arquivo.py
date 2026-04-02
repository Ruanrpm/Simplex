import re

def parse_funcao_objetivo(linha):
    linha = linha.lower().replace(" ", "")
    
    tipo = "max" if "max" in linha else "min"
    
    # Pega tudo depois do =
    expressao = linha.split("=")[1]

    termos = re.findall(r'([+-]?\d*\.?\d*)x(\d+)', expressao)

    coeficientes = {} 

    for coef, var in termos:
        if coef in ["", "+"]:
            coef = 1
        elif coef == "-":
            coef = -1
        else:
            coef = float(coef)

        coeficientes[int(var)] = coef

    return tipo, coeficientes


def parse_restricao(linha):
    linha = linha.replace(" ", "")
    
    # Identifica operador
    if "<=" in linha:
        partes = linha.split("<=")
        op = "<="
    elif ">=" in linha:
        partes = linha.split(">=")
        op = ">="
    else:
        partes = linha.split("=")
        op = "="

    esquerda, direita = partes
    b = float(direita)

    termos = re.findall(r'([+-]?\d*\.?\d*)x(\d+)', esquerda)

    coeficientes = {}

    for coef, var in termos:
        if coef in ["", "+"]:
            coef = 1
        elif coef == "-":
            coef = -1
        else:
            coef = float(coef)

        coeficientes[int(var)] = coef

    return coeficientes, op, b


def ler_arquivo(entrada):
    with open(entrada, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    tipo, c_dict = parse_funcao_objetivo(linhas[0])

    restricoes = []
    A_dicts = []
    b = []
    operadores = []

    for linha in linhas[1:]:
        coef, op, limite = parse_restricao(linha)
        A_dicts.append(coef)
        operadores.append(op)
        b.append(limite)

    # Descobrir número de variáveis
    todas_vars = set(c_dict.keys())
    for d in A_dicts:
        todas_vars.update(d.keys())

    n = max(todas_vars)

    # Converter para vetor/matriz
    c = [c_dict.get(i, 0) for i in range(1, n+1)]

    A = []
    for d in A_dicts:
        A.append([d.get(i, 0) for i in range(1, n+1)])

    return tipo, c, A, b, operadores