from functions.ler_arquivo import ler_arquivo
from simplex.Simplex import Simplex

tipo, variaveis, c, A, b, ops = ler_arquivo("entrada.txt")
tipo_original = tipo

simplex = Simplex(A, b, c, tipo, ops)
simplex.preprocessar()
# simplex.construir_fase1()

solucao, base_final, z = simplex.resolver()
print("operadores originais:", ops)


if tipo_original == "max" and z != 0:
    z = -z

print("Solução:", solucao)
print("Z:", z)
print("Base final:", base_final)

print("\nTipo:", tipo_original)
print("variaveis:", variaveis)
print("c:", simplex.c)
print("A:", simplex.A)
print("b:", simplex.b)
print("ops:", ops)





# print("A_fase1:")
# for linha in simplex.A_fase1:
#     print(linha)

# print("\nbase:", simplex.base)
# print("nbase:", simplex.nbase)
# print("artificial_mask:", simplex.artificial_mask)
# print("c_fase1:", simplex.c_fase1)