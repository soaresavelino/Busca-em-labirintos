from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Set
from collections import deque
import heapq
import itertools
import math
import time
import numpy as np  
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Estado = Tuple[int, int]

@dataclass
class No:
    estado: Estado
    pai: Optional['No'] = None
    acao: Optional[str] = None
    g: float = 0.0

@dataclass
class ResultadoBusca:
    algoritmo: str
    encontrado: bool
    caminho: List[Estado]
    acoes: List[str]
    nos_explorados: int
    nos_expandidos: int
    estados_explorados: List[Estado]
    custo_caminho: Optional[float] = None
    tempo_execucao: float = 0.0
    tamanho_max_fronteira: int = 0

    @property
    def tamanho_caminho(self) -> Optional[int]:
        return len(self.acoes) if self.encontrado else None

class LabirintoBusca:
    def __init__(self, filename: str):
        with open(filename, encoding='utf-8') as f:
            contents = f.read()

        self.mapa_original = [list(linha) for linha in contents.splitlines()]
        contents = contents.replace('S', 'A').replace('E', 'B')

        linhas = contents.splitlines()
        self.altura = len(linhas)
        self.largura = max(len(linha) for linha in linhas) if linhas else 0
        self.paredes = []
        
        # Inicialização explícita para evitar o AttributeError
        self.inicio = None
        self.objetivo = None

        for i in range(self.altura):
            row = []
            for j in range(self.largura):
                char = linhas[i][j] if j < len(linhas[i]) else ' '
                
                if char == 'A':
                    self.inicio = (i, j)
                    row.append(False)
                elif char == 'B':
                    self.objetivo = (i, j)
                    row.append(False)
                # Correção: 'T' e ' ' são caminhos livres (False = não é parede)
                elif char == ' ' or char == 'T': 
                    row.append(False)
                else:
                    row.append(True) # Parede
            self.paredes.append(row)

        # Validação obrigatória após o processamento
        if self.inicio is None or self.objetivo is None:
            raise ValueError(f"Mapa inválido em {filename}: 'A' ou 'B' não encontrados.")

    def vizinhos(self, estado: Estado):
        linha, coluna = estado
        candidatos = [
            ('cima',     (linha - 1, coluna)),
            ('baixo',    (linha + 1, coluna)),
            ('esquerda', (linha, coluna - 1)),
            ('direita',  (linha, coluna + 1)),
        ]
        resultado = []
        for acao, (l, c) in candidatos:
            if 0 <= l < self.altura and 0 <= c < self.largura and not self.paredes[l][c]:
                terreno = self.mapa_original[l][c]
                custo = 5.0 if terreno == 'T' else 1.0
                resultado.append((acao, (l, c), custo))
        return resultado


    
    def h(self, estado: Estado) -> float:
        return abs(estado[0] - self.objetivo[0]) + abs(estado[1] - self.objetivo[1])

    @staticmethod
    def reconstruir(no: No):
        estados, acoes = [], []
        atual = no
        while atual.pai is not None:
            estados.append(atual.estado)
            acoes.append(atual.acao)
            atual = atual.pai
        estados.reverse()
        acoes.reverse()
        return estados, acoes
    
    

    def busca_largura(self) -> ResultadoBusca: 
        start_time = time.time()
        inicio = No(self.inicio)
        fronteira = deque([inicio])
        em_fronteira = {self.inicio}
        explorados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []
        nos_explorados = 0
        nos_expandidos = 0
        max_len_fronteira = 0

        while fronteira:
            max_len_fronteira = max(max_len_fronteira, len(fronteira))
            no = fronteira.popleft()
            em_fronteira.remove(no.estado)
            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.objetivo:
                caminho, acoes = self.reconstruir(no)
                return ResultadoBusca(
                    'Busca em Largura (BFS)', True, caminho, acoes,
                    nos_explorados, nos_expandidos, ordem_explorados,
                    custo_caminho=no.g,
                    tempo_execucao=time.time() - start_time,
                    tamanho_max_fronteira=max_len_fronteira
                )

            explorados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.vizinhos(no.estado):
                if estado not in explorados and estado not in em_fronteira:
                    filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                    fronteira.append(filho)
                    em_fronteira.add(estado)

        return ResultadoBusca(
            'Busca em Largura (BFS)', False, [], [], nos_explorados, nos_expandidos,
            ordem_explorados, custo_caminho=None,
            tempo_execucao=time.time() - start_time,
            tamanho_max_fronteira=max_len_fronteira
        )

    def busca_profundidade(self) -> ResultadoBusca:
        start_time = time.time()
        inicio = No(self.inicio)
        fronteira = [inicio]
        em_fronteira = {self.inicio}
        explorados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []
        nos_explorados = 0
        nos_expandidos = 0
        max_len_fronteira = 0

        while fronteira:
            max_len_fronteira = max(max_len_fronteira, len(fronteira))
            no = fronteira.pop()
            em_fronteira.remove(no.estado)
            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.objetivo:
                caminho, acoes = self.reconstruir(no)
                return ResultadoBusca(
                    'Busca em Profundidade (DFS)', True, caminho, acoes,
                    nos_explorados, nos_expandidos, ordem_explorados,
                    custo_caminho=no.g,
                    tempo_execucao=time.time() - start_time,
                    tamanho_max_fronteira=max_len_fronteira
                )

            explorados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in reversed(self.vizinhos(no.estado)):
                if estado not in explorados and estado not in em_fronteira:
                    filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                    fronteira.append(filho)
                    em_fronteira.add(estado)

        return ResultadoBusca(
            'Busca em Profundidade (DFS)', False, [], [], nos_explorados, nos_expandidos,
            ordem_explorados, custo_caminho=None,
            tempo_execucao=time.time() - start_time,
            tamanho_max_fronteira=max_len_fronteira
        )

    def busca_prioridade(self, nome: str, funcao_prioridade) -> ResultadoBusca:
        start_time = time.time()
        contador = itertools.count()
        inicio = No(self.inicio, g=0.0)
        fronteira = []
        heapq.heappush(fronteira, (funcao_prioridade(inicio), next(contador), inicio))
        melhor_g: Dict[Estado, float] = {self.inicio: 0.0}
        fechados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []
        nos_explorados = 0
        nos_expandidos = 0
        max_len_fronteira = 0

        while fronteira:
            max_len_fronteira = max(max_len_fronteira, len(fronteira))
            _, _, no = heapq.heappop(fronteira)

            if no.estado in fechados:
                continue

            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.objetivo:
                caminho, acoes = self.reconstruir(no)
                return ResultadoBusca(
                    nome, True, caminho, acoes,
                    nos_explorados, nos_expandidos, ordem_explorados,
                    custo_caminho=no.g,
                    tempo_execucao=time.time() - start_time,
                    tamanho_max_fronteira=max_len_fronteira
                )

            fechados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.vizinhos(no.estado):
                novo_g = no.g + custo
                if estado in fechados:
                    continue
                if novo_g < melhor_g.get(estado, math.inf):
                    filho = No(estado=estado, pai=no, acao=acao, g=novo_g)
                    melhor_g[estado] = novo_g
                    heapq.heappush(fronteira, (funcao_prioridade(filho), next(contador), filho))

        return ResultadoBusca(
            nome, False, [], [], nos_explorados, nos_expandidos,
            ordem_explorados, custo_caminho=None,
            tempo_execucao=time.time() - start_time,
            tamanho_max_fronteira=max_len_fronteira
        )

    def busca_custo_uniforme(self) -> ResultadoBusca:
        return self.busca_prioridade('Busca de Custo Uniforme (UCS)', lambda no: no.g)

    def busca_gulosa(self) -> ResultadoBusca:
        return self.busca_prioridade('Busca Gulosa (Greedy)', lambda no: self.h(no.estado))

    def busca_astar(self) -> ResultadoBusca:
        return self.busca_prioridade('Busca A*', lambda no: no.g + self.h(no.estado))
    
    def animar_busca(self, resultado: ResultadoBusca):
        if not resultado.encontrado:
            print("Caminho não encontrado, não há o que animar.")
            return

        fig, ax = plt.subplots()
        
        # Cria a matriz do labirinto (0=Livre, 1=Parede)
        grid = np.array(self.paredes, dtype=int)
        img = ax.imshow(grid, cmap='binary')

        caminho = resultado.caminho
        
        # Elemento visual do agente
        agente, = ax.plot([], [], 'ro', markersize=5, label='Agente')

        def init():
            ax.plot(self.inicio[1], self.inicio[0], 'go', label='Início')
            ax.plot(self.objetivo[1], self.objetivo[0], 'bo', label='Objetivo')
            return agente,

        def update(frame):
            pos = caminho[frame]
            agente.set_data([pos[1]], [pos[0]])
            return agente,

        ani = animation.FuncAnimation(fig, update, frames=len(caminho), 
                                      init_func=init, blit=True, interval=100)
        
        plt.title(f"Visualização: {resultado.algoritmo}")
        plt.legend()
        plt.show()
    
    def renderizar(self, caminho_final, visitados):
        print("\n--- Visualização do Labirinto (Terminal) ---")

        mapa_vis = [linha[:] for linha in self.mapa_original]
        print("Legenda: . = Visitados | * = Caminho Final | # = Parede\n")
        
        # Cria a matriz de exibição a partir do mapa original
        
        mapa_vis = [linha[:] for linha in self.mapa_original]

        # 1. Marca os nós visitados (sem sobrescrever A ou B)
        if visitados:
            for (l, c) in visitados:
                if 0 <= l < len(mapa_vis) and 0 <= c < len(mapa_vis[0]):
                    if mapa_vis[l][c] not in ['A', 'B']:
                        mapa_vis[l][c] = '.'

        # 2. Marca o caminho final (sem sobrescrever A ou B)
        if caminho_final:
            for (l, c) in caminho_final:
                if 0 <= l < len(mapa_vis) and 0 <= c < len(mapa_vis[0]):
                    if mapa_vis[l][c] not in ['A', 'B']:
                        mapa_vis[l][c] = '*'

        # 3. Imprime linha por linha
        for linha in mapa_vis:
            print("".join(linha))
        print("\n-------------------------------------------")