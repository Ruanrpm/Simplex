from functions.ler_arquivo import ler_arquivo
from simplex.Simplex import Simplex

tipo, variaveis, c, A, b, ops = ler_arquivo("entrada.txt")
simplex = Simplex(A, b, c, tipo, ops)

simplex.preprocessar()

try:
    if simplex.precisa_fase1():
        status_fase1 = simplex.construir_fase1()

        if status_fase1 == "INFACTIVEL":
            print("Problema infactivel")
            exit()

    solucao, base_final, z = simplex.resolver()

except ValueError as erro:
    # Se o simplex percebeu inviabilidade em algum ponto, mostramos mensagem simples.
    if str(erro) == "INFACTIVEL":
        print("Problema infactivel")
        exit()

    raise erro

if solucao == "INFACTIVEL":
    print("Problema infactivel")
    exit()

# ajuste se for max original
if tipo == "max" and z is not None:
    z = -z

if z == -0.0:
    z = 0.0

print("\nSolucao:", solucao)
print("Z:", z)
print("Base final:", base_final)

print("\nvariaveis:", variaveis)
print("c:", simplex.c)
print("A:", simplex.A)
print("b:", simplex.b)
print("ops:", ops)
