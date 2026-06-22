from functions.ler_arquivo import ler_arquivo
from simplex.Simplex import Simplex
import random

tipo, variaveis, c, A, b, ops = ler_arquivo("entrada.txt")

simplex = Simplex(A, b, c, tipo)

solucao, base_final, z = simplex.resolver()

print("Solução:", solucao)
print("Z:", z)
print("Base final:", base_final)

print("\nTipo:", tipo)
print("c:", c)
print("variaveis:", variaveis)
print("A:", A)
print("b:", b)
print("ops:", ops)