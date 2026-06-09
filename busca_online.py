from collections import deque
import time
import csv
import os


MOVIMENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def ler_mapa_online(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.read().splitlines()

    largura = max(len(linha) for linha in linhas)

    mapa = []
    inicio = None
    objetivo = None

    for i, linha in enumerate(linhas):
        linha_mapa = []

        for j in range(largura):
            if j < len(linha):
                caractere = linha[j]
            else:
                caractere = " "

            linha_mapa.append(caractere)

            if caractere == "A":
                inicio = (i, j)
            elif caractere == "B":
                objetivo = (i, j)

        mapa.append(linha_mapa)

    if inicio is None or objetivo is None:
        raise ValueError("O mapa precisa conter A e B.")

    return mapa, inicio, objetivo


def dentro_do_mapa(mapa, posicao):
    linha, coluna = posicao
    return 0 <= linha < len(mapa) and 0 <= coluna < len(mapa[0])


def eh_livre(mapa, posicao):
    linha, coluna = posicao
    return mapa[linha][coluna] != "#"


def vizinhos_reais(mapa, posicao):
    linha, coluna = posicao
    lista = []

    for dl, dc in MOVIMENTOS:
        nova = (linha + dl, coluna + dc)

        if dentro_do_mapa(mapa, nova) and eh_livre(mapa, nova):
            lista.append(nova)

    return lista


def bfs_offline(mapa, inicio, objetivo):
    """
    Calcula o menor caminho usando o mapa completo.
    Isso será usado só para comparar com a busca online.
    """
    fila = deque([inicio])
    visitados = {inicio}
    pais = {}

    while fila:
        atual = fila.popleft()

        if atual == objetivo:
            break

        for vizinho in vizinhos_reais(mapa, atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pais[vizinho] = atual
                fila.append(vizinho)

    if objetivo not in pais and objetivo != inicio:
        return []

    caminho = []
    atual = objetivo

    while atual != inicio:
        caminho.append(atual)
        atual = pais[atual]

    caminho.append(inicio)
    caminho.reverse()

    return caminho


class AgenteOnlineDFS:
    def __init__(self, mapa_real, inicio, objetivo, raio=1):
        self.mapa_real = mapa_real
        self.inicio = inicio
        self.objetivo = objetivo
        self.raio = raio

        self.altura = len(mapa_real)
        self.largura = len(mapa_real[0])

        self.posicao_atual = inicio

        self.mapa_interno = [
            ["?" for _ in range(self.largura)]
            for _ in range(self.altura)
        ]

        self.mapa_interno[inicio[0]][inicio[1]] = "A"

        self.visitados = set()
        self.trajetoria = [inicio]
        self.pilha_retorno = []

        self.movimentos = 0
        self.celulas_reveladas = set()
        self.celulas_revisitadas = 0
        self.replanejamentos = 0

    def perceber(self):
        """
        O agente percebe apenas as células próximas.
        Com raio 1, ele percebe cima, baixo, esquerda, direita e a célula atual.
        """
        linha, coluna = self.posicao_atual

        posicoes_percebidas = [(linha, coluna)]

        for dl, dc in MOVIMENTOS:
            nova = (linha + dl, coluna + dc)
            posicoes_percebidas.append(nova)

        for posicao in posicoes_percebidas:
            if dentro_do_mapa(self.mapa_real, posicao):
                l, c = posicao
                self.mapa_interno[l][c] = self.mapa_real[l][c]
                self.celulas_reveladas.add(posicao)

    def vizinhos_livres_conhecidos(self, posicao):
        """
        Retorna apenas vizinhos que o agente já sabe que são livres.
        Ele não anda para célula desconhecida diretamente.
        """
        linha, coluna = posicao
        lista = []

        for dl, dc in MOVIMENTOS:
            nova = (linha + dl, coluna + dc)

            if dentro_do_mapa(self.mapa_interno, nova):
                l, c = nova

                if self.mapa_interno[l][c] != "#" and self.mapa_interno[l][c] != "?":
                    lista.append(nova)

        return lista

    def escolher_proxima_posicao(self):
        """
        Estratégia Online DFS:
        - tenta ir para um vizinho livre ainda não visitado;
        - se não existir, volta pelo caminho anterior.
        """
        self.visitados.add(self.posicao_atual)

        for vizinho in self.vizinhos_livres_conhecidos(self.posicao_atual):
            if vizinho not in self.visitados:
                self.pilha_retorno.append(self.posicao_atual)
                return vizinho

        if self.pilha_retorno:
            return self.pilha_retorno.pop()

        return None

    def executar(self, limite_passos=1000, mostrar_passos=False):
        tempo_inicio = time.time()

        while self.posicao_atual != self.objetivo and self.movimentos < limite_passos:
            self.perceber()
            self.replanejamentos += 1

            proxima = self.escolher_proxima_posicao()

            if proxima is None:
                break

            if proxima in self.trajetoria:
                self.celulas_revisitadas += 1

            self.posicao_atual = proxima
            self.trajetoria.append(proxima)
            self.movimentos += 1

            if mostrar_passos:
                self.imprimir_mapa_interno()

        self.perceber()

        tempo_total = time.time() - tempo_inicio

        return {
            "sucesso": self.posicao_atual == self.objetivo,
            "movimentos": self.movimentos,
            "custo_real": self.movimentos,
            "celulas_reveladas": len(self.celulas_reveladas),
            "celulas_revisitadas": self.celulas_revisitadas,
            "replanejamentos": self.replanejamentos,
            "tempo": tempo_total,
            "trajetoria": self.trajetoria,
            "mapa_interno": self.mapa_interno,
            "visitados": self.visitados
        }

    def imprimir_mapa_interno(self):
        print("\nMapa interno do agente:")

        copia = [linha.copy() for linha in self.mapa_interno]
        l, c = self.posicao_atual
        copia[l][c] = "X"

        for linha in copia:
            print("".join(linha))


def desenhar_trajetoria(mapa_real, trajetoria):
    """
    Mostra o mapa real com o caminho percorrido pelo agente.
    """
    mapa_saida = [linha.copy() for linha in mapa_real]

    for posicao in trajetoria:
        l, c = posicao

        if mapa_saida[l][c] not in ["A", "B"]:
            mapa_saida[l][c] = "."

    return "\n".join("".join(linha) for linha in mapa_saida)


def salvar_csv_online(resultado, custo_offline, razao, caminho="resultados/resultado_online.csv"):
    os.makedirs("resultados", exist_ok=True)

    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)

        escritor.writerow([
            "sucesso",
            "movimentos",
            "custo_real",
            "celulas_reveladas",
            "celulas_revisitadas",
            "replanejamentos",
            "tempo",
            "custo_otimo_offline",
            "razao_online_offline"
        ])

        escritor.writerow([
            resultado["sucesso"],
            resultado["movimentos"],
            resultado["custo_real"],
            resultado["celulas_reveladas"],
            resultado["celulas_revisitadas"],
            resultado["replanejamentos"],
            resultado["tempo"],
            custo_offline,
            razao
        ])