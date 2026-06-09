import random
import math
import time
import os
import sys
from collections import deque
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

EstadoColeta = Tuple[int, int]
Permutacao = List[int]


class LabirintoColeta:

    def __init__(self, filename: str):
        with open(filename, encoding="utf-8") as f:
            contents = f.read()

        linhas = contents.splitlines()
        self.altura = len(linhas)
        self.largura = max(len(linha) for dynamic_line in linhas for linha in [dynamic_line])

        self.paredes = []
        self.coletas = []
        self.inicio = None
        self.objetivo = None

        for i in range(self.altura):
            linha_grid = []
            for j in range(self.largura):
                char = linhas[i][j] if j < len(linhas[i]) else " "

                if char == "#":
                    linha_grid.append(True)
                elif char in ("A", "S"):
                    self.inicio = (i, j)
                    linha_grid.append(False)
                elif char in ("B", "E"):
                    self.objetivo = (i, j)
                    linha_grid.append(False)
                elif char == "C":
                    self.coletas.append((i, j))
                    linha_grid.append(False)
                else:
                    linha_grid.append(False)
            self.paredes.append(linha_grid)

        if self.inicio is None or self.objetivo is None:
            raise ValueError("O mapa precisa conter o ponto inicial 'A' e o objetivo 'B'.")

        self.matriz_distancias = self._calcular_matriz_distancias()

    def _vizinhos_grid(self, estado):
        linha, coluna = estado
        candidatos = [
            (linha - 1, coluna),
            (linha + 1, coluna),
            (linha, coluna - 1),
            (linha, coluna + 1)
        ]
        return [
            (l, c)
            for l, c in candidatos
            if 0 <= l < self.altura
            and 0 <= c < self.largura
            and not self.paredes[l][c]
        ]

    def _bfs_distancia_total(self, origem):
        fila = deque([origem])
        distancias = {origem: 0}

        while fila:
            atual = fila.popleft()
            for vizinho in self._vizinhos_grid(atual):
                if vizinho not in distancias:
                    distancias[vizinho] = distancias[atual] + 1
                    fila.append(vizinho)
        return distancias

    def _calcular_matriz_distancias(self):
        pontos = [self.inicio] + self.coletas + [self.objetivo]
        matriz = {}
        for ponto in pontos:
            matriz[ponto] = self._bfs_distancia_total(ponto)
        return matriz

    def calcular_custo_rota(self, seq):
        if not seq:
            return self.matriz_distancias[self.inicio].get(self.objetivo, math.inf)

        custo = self.matriz_distancias[self.inicio].get(self.coletas[seq[0]], math.inf)

        for i in range(len(seq) - 1):
            p1 = self.coletas[seq[i]]
            p2 = self.coletas[seq[i + 1]]
            custo += self.matriz_distancias[p1].get(p2, math.inf)

        custo += self.matriz_distancias[self.coletas[seq[-1]]].get(self.objetivo, math.inf)
        return custo

    def gerar_vizinhos(self, seq):
        if len(seq) < 2:
            return []
        vizinhos = []
        n = len(seq)
        for i in range(n):
            for j in range(i + 1, n):
                novo = seq.copy()
                novo[i], novo[j] = novo[j], novo[i]
                vizinhos.append(novo)
        return vizinhos

    def gerar_unico_vizinho_aleatorio(self, seq):
        if len(seq) < 2:
            return seq.copy()
        novo = seq.copy()
        i, j = random.sample(range(len(seq)), 2)
        novo[i], novo[j] = novo[j], novo[i]
        return novo

    def imprimir_rota(self, rota):
        if not rota:
            print("\n➡ ROTA SEGUIDA: A (Início) ➔ B (Objetivo)")
        else:
            passo_a_passo = ["A (Início)"]
            for indice in rota:
                passo_a_passo.append(f"C{indice}")
            passo_a_passo.append("B (Objetivo)")
            print("\n➡ ROTA SEGUIDA: " + " ➔ ".join(passo_a_passo))

        print("+" + "-"*7 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*14 + "+" + "-"*17 + "+")
        print(f"| {'Etapa':<5} | {'Origem':<14} | {'Destino':<14} | {'Custo Trecho':<12} | {'Custo Total':<15} |")
        print("+" + "-"*7 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*14 + "+" + "-"*17 + "+")
        
        if not rota:
            custo = self.matriz_distancias[self.inicio].get(self.objetivo, math.inf)
            print(f"| {'1':<5} | {'A (Início)':<14} | {'B (Objetivo)':<14} | {custo:<12} | {custo:<15} |")
            print("+" + "-"*7 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*14 + "+" + "-"*17 + "+")
            return

        custo_acumulado = 0
        etapa = 1

        p_at = self.inicio
        p_prox = self.coletas[rota[0]]
        custo_trecho = self.matriz_distancias[p_at].get(p_prox, math.inf)
        custo_acumulado += custo_trecho
        print(f"| {etapa:<5} | {'A (Início)':<14} | {f'C{rota[0]}':<14} | {custo_trecho:<12} | {custo_acumulado:<15} |")

        for i in range(len(rota) - 1):
            etapa += 1
            p_at = self.coletas[rota[i]]
            p_prox = self.coletas[rota[i+1]]
            custo_trecho = self.matriz_distancias[p_at].get(p_prox, math.inf)
            custo_acumulado += custo_trecho
            print(f"| {etapa:<5} | {f'C{rota[i]}':<14} | {f'C{rota[i+1]}':<14} | {custo_trecho:<12} | {custo_acumulado:<15} |")

        etapa += 1
        p_at = self.coletas[rota[-1]]
        p_prox = self.objetivo
        custo_trecho = self.matriz_distancias[p_at].get(p_prox, math.inf)
        custo_acumulado += custo_trecho
        print(f"| {etapa:<5} | {f'C{rota[-1]}':<14} | {'B (Objetivo)':<14} | {custo_trecho:<12} | {custo_acumulado:<15} |")
        
        print("+" + "-"*7 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*14 + "+" + "-"*17 + "+")

    def hill_climbing(self):
        if len(self.coletas) == 0:
            custo = self.calcular_custo_rota([])
            return [], custo, [custo]

        atual = list(range(len(self.coletas)))
        random.shuffle(atual)
        custo_atual = self.calcular_custo_rota(atual)
        historico = [custo_atual]

        while True:
            vizinhos = self.gerar_vizinhos(atual)
            if not vizinhos:
                break

            melhor_vizinho = min(vizinhos, key=self.calcular_custo_rota)
            custo_vizinho = self.calcular_custo_rota(melhor_vizinho)

            if custo_vizinho >= custo_atual:
                break

            atual = melhor_vizinho
            custo_atual = custo_vizinho
            historico.append(custo_atual)

        return atual, custo_atual, historico

    def simulated_annealing(self, t_inicial=150.0, alfa=0.98, max_iter=1500):
        if len(self.coletas) < 2:
            atual = list(range(len(self.coletas)))
            custo = self.calcular_custo_rota(atual)
            return atual, custo, [custo]

        atual = list(range(len(self.coletas)))
        random.shuffle(atual)
        custo_atual = self.calcular_custo_rota(atual)

        melhor = atual.copy()
        melhor_custo = custo_atual
        temperatura = t_inicial
        historico = [custo_atual]

        for _ in range(max_iter):
            if temperatura < 0.001:
                break

            vizinho = self.gerar_unico_vizinho_aleatorio(atual)
            custo_vizinho = self.calcular_custo_rota(vizinho)
            delta = custo_vizinho - custo_atual

            if delta < 0 or random.random() < math.exp(-delta / temperatura):
                atual = vizinho
                custo_atual = custo_vizinho

                if custo_atual < melhor_custo:
                    melhor = vizinho.copy()
                    melhor_custo = custo_atual

            historico.append(custo_atual)
            temperatura *= alfa

        return melhor, melhor_custo, historico

def generar_mapa_aleatorio_dinamico(filename: str, num_coletas: int = 7, altura: int = 14, largura: int = 35):
    random.seed(time.time_ns())
    while True:
        grid = [["#" for _ in range(largura)] for _ in range(altura)]
        for i in range(1, altura - 1):
            for j in range(1, largura - 1):
                if random.random() > 0.28: 
                    grid[i][j] = " "
        for j in range(1, largura - 1):
            grid[1][j] = " "
            grid[grid_alt := altura - 2][j] = " "
        for i in range(1, altura - 1):
            grid[i][1] = " "
            grid[i][largura - 2] = " "

        livres = [(i, j) for i in range(1, altura - 1) for j in range(1, largura - 1) if grid[i][j] == " "]
        total_pontos = 2 + num_coletas
        if len(livres) < total_pontos: continue

        posicoes = random.sample(livres, total_pontos)
        p_inicio, p_objetivo = posicoes[0], posicoes[1]
        coletas_pos = posicoes[2:]

        grid[p_inicio[0]][p_inicio[1]] = "A"
        grid[p_objetivo[0]][p_objetivo[1]] = "B"
        for cx in coletas_pos: grid[cx[0]][cx[1]] = "C"

        fila = deque([p_inicio])
        visitados = {p_inicio}
        while fila:
            al, ac = fila.popleft()
            for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nl, nc = al + dl, ac + dc
                if 0 <= nl < altura and 0 <= nc < largura and grid[nl][nc] != "#":
                    if (nl, nc) not in visitados:
                        visitados.add((nl, nc))
                        fila.append((nl, nc))

        if all(p in visitados for p in [p_objetivo] + coletas_pos):
            with open(filename, "w", encoding="utf-8") as f:
                for linha in grid: f.write("".join(linha) + "\n")
            print(f"\n[+] Novo mapa salvo com sucesso em: '{filename}'")
            break

def executar_busca_local():
    os.makedirs("graficos", exist_ok=True)
    os.makedirs("mapas", exist_ok=True)

    arquivos_mapas = sorted([f for f in os.listdir("mapas") if f.endswith(".txt")])
    
    print("\n=== SELEÇÃO DE MAPA PARA BUSCA LOCAL (SEMANA 2) ===")
    print("0 - [GERAR E SALVAR NOVO MAPA ALEATÓRIO]")
    for idx, mapa in enumerate(arquivos_mapas, start=1):
        print(f"{idx} - mapas/{mapa}")
    
    try:
        escolha = int(input("\nEscolha uma opção ou o número do mapa: "))
        if escolha == 0:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"mapas/mapa_aleatorio_{timestamp}.txt"
            generar_mapa_aleatorio_dinamico(nome_arquivo, num_coletas=7)
        else:
            nome_arquivo = os.path.join("mapas", arquivos_mapas[escolha - 1])
    except (ValueError, IndexError):
        print("[!] Opção inválida. Usando o primeiro mapa disponível por segurança.")
        if arquivos_mapas:
            nome_arquivo = os.path.join("mapas", arquivos_mapas[0])
        else:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"mapas/mapa_aleatorio_{timestamp}.txt"
            generar_mapa_aleatorio_dinamico(nome_arquivo, num_coletas=7)

    print(f"\n[*] Executando algoritmos no cenário: '{nome_arquivo}'")
    
    try:
        lab = LabirintoColeta(nome_arquivo)
    except Exception as e:
        print(f"[!] Erro ao ler ou processar o mapa selecionado: {e}")
        return

    print(f"[*] Coletas encontradas no arquivo: {len(lab.coletas)}")
    print(f"[*] Início: {lab.inicio} | Objetivo: {lab.objetivo}")

    # HILL CLIMANBG
    inicio = time.time()
    rota_hc, custo_hc, hist_hc = lab.hill_climbing()
    tempo_hc = time.time() - inicio

    print("\n" + "=" * 50 + "\nHILL CLIMBING\n" + "=" * 50)
    lab.imprimir_rota(rota_hc)
    print(f"Tempo de execução: {tempo_hc:.4f}s")

    # SIMULATED ANNEALING
    inicio = time.time()
    rota_sa, custo_sa, hist_sa = lab.simulated_annealing()
    tempo_sa = time.time() - inicio

    print("\n" + "=" * 50 + "\nSIMULATED ANNEALING\n" + "=" * 50)
    lab.imprimir_rota(rota_sa)
    print(f"Tempo de execução: {tempo_sa:.4f}s")

    #ANÁLISE COMPARATIVA
    print("\n" + "=" * 50 + "\nANÁLISE\n" + "=" * 50)
    if custo_sa < custo_hc:
        print(f"Simulated Annealing foi MELHOR (Custo {custo_sa} contra {custo_hc} do HC).")
    elif custo_hc < custo_sa:
        print(f"Hill-Climbing foi MELHOR (Custo {custo_hc} contra {custo_sa} do SA).")
    else:
        print(f"Empate técnico! Ambos acharam o mesmo custo final de {custo_hc}.")

    #GERAÇÃO DOS GRÁFICOS
    if custo_hc != math.inf and custo_sa != math.inf and len(lab.coletas) >= 2:
        plt.figure(figsize=(12, 6))
        plt.plot(hist_hc, label=f"HC ({custo_hc})", linewidth=2, marker="o", markevery=max(1, len(hist_hc)//5))
        plt.plot(hist_sa, label=f"SA ({custo_sa})", linewidth=1.5)
        plt.title(f"Convergência dos Algoritmos ({len(lab.coletas)} Coletas)")
        plt.xlabel("Iterações")
        plt.ylabel("Custo da Solução")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("graficos/convergencia_coletas_semana2.png", dpi=300)
        plt.close()

        plt.figure(figsize=(8, 5))
        plt.bar(["Hill-Climbing", "Simulated Annealing"], [custo_hc, custo_sa], color=['crimson', 'dodgerblue'])
        plt.title("Comparação dos Custos Finais")
        plt.ylabel("Distância Total")
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig("graficos/comparacao_custos.png", dpi=300)
        plt.close()
        print("\n[+] Gráficos salvos com sucesso na pasta 'graficos/'.")


if __name__ == "__main__":
    executar_busca_local()