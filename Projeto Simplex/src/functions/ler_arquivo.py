import re

def extrair_termos(expressao):
    expressao = expressao.replace(" ", "")

    termos = re.findall(r'([+-]?\d*\.?\d*)([a-zA-Z])(\d+)', expressao)

    coeficientes = {}

    for coef, var, idx in termos:
        if coef in ["", "+"]:
            coef = 1
        elif coef == "-":
            coef = -1
        else:
            coef = float(coef)

        chave = f"{var}{idx}"
        coeficientes[chave] = coeficientes.get(chave, 0) + coef

    return coeficientes


def parse_funcao_objetivo(linha):
    linha = linha.lower()

    tipo = "max" if "max" in linha else "min"

    # pega tudo depois do =
    expressao = linha.split("=")[1]

    coeficientes = extrair_termos(expressao)

    return tipo, coeficientes


def parse_restricao(linha):
    linha = linha.lower()

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
    b = float(direita.strip())

    coeficientes = extrair_termos(esquerda)

    return coeficientes, op, b


def ordenar_variaveis(todas_vars):

    xs = []
    ss = []
    outras = []

    for v in todas_vars:

        if v[0] == 'x':
            xs.append(v)

        elif v[0] == 's':
            ss.append(v)

        else:
            outras.append(v)

    xs.sort()
    ss.sort()
    outras.sort()

    return xs + ss + outras


def ler_arquivo(entrada):
    with open(entrada, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    # função objetivo
    tipo, c_dict = parse_funcao_objetivo(linhas[0])

    A_dicts = []
    b = []
    operadores = []

    # contador das variáveis de folga
    contador_s = 1
    operadores = []

    # restrições
    for linha in linhas[1:]:
        coef, op, limite = parse_restricao(linha)
        operadores.append(op)
        # normalização
        if op == "<=":
            var_s = f"s{contador_s}"
            coef[var_s] = 1
            op = "="
            contador_s += 1

        elif op == ">=":
            var_s = f"s{contador_s}"
            coef[var_s] = -1
            op = "="
            contador_s += 1

        A_dicts.append(coef)
        b.append(limite)

    # todas variáveis ex: x1/x2
    todas_vars = set(c_dict.keys())
    for d in A_dicts:
        todas_vars.update(d.keys())

    # ordenação correta (x primeiro, depois s)
    variaveis = ordenar_variaveis(todas_vars)

    # vetor c
    c = []

    for var in variaveis:
        c.append(c_dict.get(var, 0))

    # matriz A
    A = []

    for d in A_dicts:

        linha = []

        for var in variaveis:
            linha.append(d.get(var, 0))

        A.append(linha)

    return tipo, variaveis, c, A, b, operadores