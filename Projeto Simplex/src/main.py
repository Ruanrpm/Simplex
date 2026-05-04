from functions.ler_arquivo import ler_arquivo
from simplex.Simplex import Simplex
import random

tipo, c, A, b, ops = ler_arquivo("entrada.txt")

base = random.sample(range(len(c)), len(b))

simplex = Simplex(A, b, c, base)

solucao, base_final = simplex.resolver()

print("Solução:", solucao)
print("Base final:", base_final)

print("\nTipo:", tipo)
print("c:", c)
print("A:", A)
print("b:", b)
print("ops:", ops)