import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def carregar_dados():
    # Mude de 'resultados/resultados.csv' para 'resultados/resultadosclassica.csv'
    return pd.read_csv('resultados/resultadosclassica.csv')

def plotar_barra(metrica):
    df = carregar_dados()
    mapas = df['Labirinto'].unique()
    algoritmos = df['Algoritmo'].unique()
    
    x = np.arange(len(algoritmos))
    width = 0.25
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plota uma barra para cada mapa
    for i, mapa in enumerate(mapas):
        valores = df[df['Labirinto'] == mapa][metrica].values
        offset = (i - 1) * width # Centraliza as barras
        rects = ax.bar(x + offset, valores, width, label=mapa)
        ax.bar_label(rects, padding=3, fontsize=8)

    ax.set_ylabel(metrica)
    ax.set_title(f'Desempenho: {metrica} por Algoritmo')
    ax.set_xticks(x)
    ax.set_xticklabels(algoritmos)
    ax.legend()
    plt.tight_layout()
    plt.show()

def plotar_escalabilidade():
    df = carregar_dados()
    algoritmos = df['Algoritmo'].unique()
    mapas = df['Labirinto'].unique()
    
    plt.figure(figsize=(10, 6))
    for alg in algoritmos:
        valores = df[df['Algoritmo'] == alg]['Expandidos'].values
        plt.plot(mapas, valores, marker='o', label=alg, linewidth=2)
    
    plt.title('Escalabilidade: Nós Expandidos por Mapa')
    plt.ylabel('Nós Expandidos')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    while True:
        print("\n--- MENU DE GRÁFICOS (DINÂMICO) ---")
        print("1 - Nós Expandidos (Barras)")
        print("2 - Tempo(ms) (Barras)")
        print("3 - Passos (Barras)")
        print("4 - Escalabilidade (Linhas)")
        print("0 - Sair")
        
        opcao = input("Escolha: ")
        if opcao == '1': plotar_barra('Expandidos')
        elif opcao == '2': plotar_barra('Tempo(ms)')
        elif opcao == '3': plotar_barra('Passos')
        elif opcao == '4': plotar_escalabilidade()
        elif opcao == '0': break
        import matplotlib.pyplot as plt
import numpy as np

def gerar_grafico_comparativo():
   
    algoritmos = ['BFS', 'DFS', 'UCS', 'Gulosa', 'A*']
  
    custos_custo1 = [8.0, 14.0, 8.0, 8.0, 8.0]    
    custos_custo5 = [10.0, 14.0, 8.0, 8.0, 8.0]   

    x = np.arange(len(algoritmos))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - largura/2, custos_custo1, largura, label='Cenário Custo 1.0')
    rects2 = ax.bar(x + largura/2, custos_custo5, largura, label='Cenário Custo 5.0')

    ax.set_ylabel('Custo Total do Caminho')
    ax.set_title('Comparativo: Impacto do Custo de Terreno nos Algoritmos')
    ax.set_xticks(x)
    ax.set_xticklabels(algoritmos)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    plt.tight_layout()
    plt.show()

# Chame esta função após ter rodado seus testes nos dois mapas
gerar_grafico_comparativo()