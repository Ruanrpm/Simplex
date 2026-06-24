from functions.ler_arquivo import ler_arquivo
# from functions.ler_arquivo import preprocessar
from simplex.Simplex import Simplex

tipo, variaveis, c, A, b, ops = ler_arquivo("entrada.txt")
tipo_original = tipo
# tipo, c, A, b = preprocessar(tipo, c, A, b)

simplex = Simplex(A, b, c, tipo, ops)
simplex.preprocessar()
simplex.construir_fase1()

# solucao, base_final, z = simplex.resolver()
print("operadores originais:", ops)

print("A_fase1:")
for linha in simplex.A_fase1:
    print(linha)

print("\nbase:", simplex.base)
print("nbase:", simplex.nbase)
print("artificial_mask:", simplex.artificial_mask)
print("c_fase1:", simplex.c_fase1)

# if tipo_original == "max":
#     z = -z

# print("Solução:", solucao)
# print("Z:", z)
# print("Base final:", base_final)

# print("\nTipo:", tipo_original)
# print("variaveis:", variaveis)
# print("c:", simplex.c)
# print("A:", simplex.A)
# print("b:", simplex.b)
# print("ops:", ops)