import random

# Grafos representados por matriz de adjacência
G1 = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]

# Isomorfismo secreto
phi = [2, 0, 1]


def permute_graph(G, perm):
    n = len(G)

    H = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            H[perm[i]][perm[j]] = G[i][j]

    return H


def inverse_perm(p):
    inv = [0] * len(p)

    for i, v in enumerate(p):
        inv[v] = i

    return inv


def compose(p1, p2):
    return [p1[p2[i]] for i in range(len(p1))]


G2 = permute_graph(G1, phi)

print("G2:")
print(G2)

rodadas = 10

for r in range(rodadas):

    # Peggy
    pi = list(range(len(G1)))
    random.shuffle(pi)

    H = permute_graph(G1, pi)

    # Victor
    b = random.randint(0, 1)

    # Peggy responde
    if b == 0:
        sigma = inverse_perm(pi)
        alvo = G1
    else:
        sigma = compose(inverse_perm(phi), inverse_perm(pi))
        alvo = G2

    # Verificação
    teste = permute_graph(H, sigma)

    aceito = (teste == alvo)

    print(f"Rodada {r+1}: desafio={b}, aceito={aceito}")
