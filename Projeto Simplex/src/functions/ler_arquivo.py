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
    # separa por tipo
    xs = sorted(
        [v for v in todas_vars if v.startswith('x')],
        key=lambda v: int(v[1:])
    )

    ss = sorted(
        [v for v in todas_vars if v.startswith('s')],
        key=lambda v: int(v[1:])
    )

    # outras variáveis (caso existam futuramente)
    outras = sorted(
        [v for v in todas_vars if not (v.startswith('x') or v.startswith('s'))]
    )

    return xs + ss + outras


def ler_arquivo(entrada):
    with open(entrada, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    # função objetivo
    tipo, c_dict = parse_funcao_objetivo(linhas[0])

    A_dicts = []
    b = []
    operadores = []

    # restrições
    for linha in linhas[1:]:
        coef, op, limite = parse_restricao(linha)
        A_dicts.append(coef)
        operadores.append(op)
        b.append(limite)

    # todas variáveis
    todas_vars = set(c_dict.keys())
    for d in A_dicts:
        todas_vars.update(d.keys())

    # ordenação correta (x primeiro, depois s)
    variaveis = ordenar_variaveis(todas_vars)

    # vetor c
    c = [c_dict.get(var, 0) for var in variaveis]

    # matriz A
    A = []
    for d in A_dicts:
        A.append([d.get(var, 0) for var in variaveis])

    return tipo, variaveis, c, A, b, operadores