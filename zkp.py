import random
import time
import matplotlib.pyplot as plt

# Contagem de operações
operations = {
    "permutacao": 0,
    "inversao": 0,
    "composicao": 0,
    "verificacao": 0
}

# Tempo de operações
op_times = {
    "permutacao": [],
    "inversao": [],
    "composicao": [],
}

memory = []

# Grafos representados por matriz de adjacência
G1 = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]

# Isomorfismo secreto
# Conhecido apenas pelo provador
phi = [2, 0, 1]

# Função de permutação
def permute_graph(G, perm):
    inicio = time.perf_counter()
    n = len(G)
    H = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            H[perm[i]][perm[j]] = G[i][j]

    op_times["permutacao"].append(time.perf_counter() - inicio)
    operations["permutacao"] += 1
    return H


def inverse_perm(p):
    inicio = time.perf_counter()
    inv = [0] * len(p)
    for i, v in enumerate(p):
        inv[v] = i
    op_times["inversao"].append(time.perf_counter() - inicio)
    operations["inversao"] += 1
    return inv


def compose(p1, p2):
    inicio = time.perf_counter()
    r = [p1[p2[i]] for i in range(len(p1))]

    op_times["composicao"].append(time.perf_counter() - inicio)
    operations["composicao"] += 1
    return r

def run(num_Rounds):
    accept = False

    G2 = permute_graph(G1, phi)
    print("G2:")
    print(G2)
    n = len(G1)

    for r in range(num_Rounds):
        # Prover
        pi = list(range(n))
        random.shuffle(pi)

        H = permute_graph(G1, pi)

        # Verifier
        # Geração do desafio. Verifier escolhe aleatoriamente entre 0 e 1
        b = random.randint(0, 1)

        # Prover responde
        if b == 0:
            sigma = inverse_perm(pi)
            target = G1
        else:
            sigma = compose(inverse_perm(phi), inverse_perm(pi))
            target = G2

        # Verificação
        test = permute_graph(H, sigma)
        accept = (test == target)
        operations["verificacao"] += 1

        # memória teórica:
        # G1 + G2 + H + pi + sigma
        memory.append(3*n*n + 2*n)
        print(f"Rodada {r+1}: desafio={b}, aceito={accept}")
    return accept

# Tempo medio por etapa
def timePerStep():
    time_med = {}

    for key in op_times:
        time_med[key] = sum(op_times[key]) / len(op_times[key])

    plt.figure(figsize=(8,5))

    plt.bar(time_med.keys(), [v*1000 for v in time_med.values()])

    plt.ylabel("Tempo médio (ms)")
    plt.title("Tempo médio por etapa do protocolo")
    plt.tight_layout()

    plt.savefig("tempo_etapas.png")

# Numero de operacoes em cada etapa
def numberOperations():
    plt.figure(figsize=(8,5))

    plt.bar(operations.keys(), operations.values())

    plt.ylabel("Quantidade")
    plt.title("Número de operações executadas")

    plt.tight_layout()

    plt.savefig("num_operacoes.png")

# Memoria
def memoryUsage(rounds):
    plt.figure(figsize=(8,5))

    plt.plot(range(1, rounds+1), memory)

    plt.xlabel("Rodadas")
    plt.ylabel("Elementos armazenados")
    plt.title("Custo espacial")

    plt.tight_layout()

    plt.savefig("memoria.png")

    
# Iniciando o protocolo

rounds = 80

inicio = time.perf_counter()
run(rounds)
fim = time.perf_counter()

total_time = (fim - inicio)*1000
print(f"Tempo total: {total_time}")

# Gerando graficos
timePerStep()
numberOperations()
memoryUsage(rounds)

print("Arquivos gerados:")
print("tempo_etapas.png")
print("num_operacoes.png")
print("memoria.png")
