import csv
import os
from labirinto import LabirintoBusca
from busca_local import executar_busca_local

from busca_online import (
    ler_mapa_online,
    bfs_offline,
    AgenteOnlineDFS,
    desenhar_trajetoria,
    salvar_csv_online
)


ARQUIVOS = [
    ('Labirinto 1  Pequeno  (21x21)', 'mapas/maze1.txt'),
    ('Labirinto 2  Medio    (41x41)', 'mapas/maze2.txt'),
    ('Labirinto 3  Grande   (61x61)', 'mapas/maze3.txt'),
]


def executar_semana1():
    todos_resultados = []
    
    # 1. PROCESSAMENTO
    for nome, arquivo in ARQUIVOS:
        lab = LabirintoBusca(arquivo)
        resultados = [
            lab.busca_largura(),
            lab.busca_profundidade(),
            lab.busca_custo_uniforme(),
            lab.busca_gulosa(),
            lab.busca_astar(),
        ]
        
        for r in resultados:
            todos_resultados.append({
                'Labirinto': nome.strip(),
                'Algoritmo': r.algoritmo,
                'Sucesso': 'Sim' if r.encontrado else 'Não',
                'Custo': str(r.custo_caminho) if r.encontrado else '–',
                'Passos': str(r.tamanho_caminho) if r.encontrado else '–',
                'Explorados': r.nos_explorados,
                'Expandidos': r.nos_expandidos,
                'Tempo(ms)': f'{r.tempo_execucao * 1000:.3f}',
                'Fronteira': r.tamanho_max_fronteira,
                'lab_obj': lab,
                'resultado_obj': r
            })

    # 2. EXPORTAÇÃO PARA CSV (Adicionado aqui)
    os.makedirs('resultados', exist_ok=True)
    caminho_csv = 'resultados/resultadosclassica.csv'
    campos = ['Labirinto', 'Algoritmo', 'Sucesso', 'Custo', 'Passos', 'Explorados', 'Expandidos', 'Tempo(ms)', 'Fronteira']
    
    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for r in todos_resultados:
            # Salvamos apenas os campos definidos, excluindo os objetos (lab_obj/resultado_obj)
            writer.writerow({k: r[k] for k in campos})
    print(f'\n[*] Resultados salvos em: {caminho_csv}')

    # 3. MENU DE EXIBIÇÃO
    while True:
        print("\n--- MENU DE RESULTADOS SEMANA 1 ---")
        print("1 - Ver Tabela Comparativa Completa")
        print("2 - Ver Animação de um Algoritmo")
        print("3 - Ver Visualização Visual (Mapa/Nós)")
        print("0 - Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            # fmt: 
            # Labirinto(20), Algoritmo(25), Suc(4), Custo(6), Passos(6), Expl(6), Exp(6), Tempo(10), Front(6)
            fmt = "{:<20} | {:<25} | {:<4} | {:>6} | {:>6} | {:>6} | {:>6} | {:>10} | {:>6}"
            
            # Cabeçalho
            header = fmt.format("Labirinto", "Algoritmo", "Sucesso", "Custo", "Passos", "Explorados", "Expandidos", "Tempo(ms)", "Fronteira")
            print("\n" + header)
            print("-" * len(header))
            
            # Dados
            for r in todos_resultados:
                print(fmt.format(
                    r['Labirinto'][:20],
                    r['Algoritmo'][:25], # Garante que o texto não ultrapasse
                    r['Sucesso'][:3],
                    r['Custo'],
                    r['Passos'],
                    r['Explorados'],
                    r['Expandidos'],
                    r['Tempo(ms)'],
                    r['Fronteira']
                ))
        
        elif escolha == '2':
            print("\nEscolha o número do experimento para animar:")
            fmt_menu = "{:<2} - {:<20} | {:<30}"
            for i, r in enumerate(todos_resultados):
                print(fmt_menu.format(i, r['Labirinto'][:20], r['Algoritmo']))
            
            try:
                idx = int(input("Número: "))
                item = todos_resultados[idx]
                if item['resultado_obj'].encontrado:
                    item['lab_obj'].animar_busca(item['resultado_obj'])
                else:
                    print("Caminho não encontrado!")
            except (ValueError, IndexError):
                print("Opção inválida.")

        elif escolha == '3':
            print("\nEscolha o número do experimento para visualizar:")
            fmt_menu = "{:<2} - {:<20} | {:<30}"
            for i, r in enumerate(todos_resultados):
                print(fmt_menu.format(i, r['Labirinto'][:20], r['Algoritmo']))
            
            try:
                idx = int(input("Número: "))
                item = todos_resultados[idx]
                
                # Chamada corrigida: passando a lista de estados e não o contador
                item['lab_obj'].renderizar(
                    item['resultado_obj'].caminho, 
                    item['resultado_obj'].estados_explorados
                )
            except (ValueError, IndexError, AttributeError) as e:
                print(f"Erro ao visualizar: {e}")
        
        elif escolha == '0':
            break
def executar_semana2():
    print()
    print('=' * 105)
    print('SEMANA 2 – BUSCA LOCAL COM PONTOS DE COLETA')
    print('=' * 105)

    executar_busca_local()

    print()
    print('Semana 2 finalizada.')
    print('=' * 105)

def executar_semana3():
    print()
    print('=' * 105)
    print('SEMANA 3 – BUSCA ONLINE NO LABIRINTO DESCONHECIDO')
    print('=' * 105)

    mapa, inicio, objetivo = ler_mapa_online('mapas/mapa_online.txt')

    agente = AgenteOnlineDFS(mapa, inicio, objetivo)

    resultado_online = agente.executar(mostrar_passos=False)

    caminho_otimo = bfs_offline(mapa, inicio, objetivo)
    custo_offline = len(caminho_otimo) - 1 if caminho_otimo else None

    if custo_offline and custo_offline > 0:
        razao = resultado_online['custo_real'] / custo_offline
    else:
        razao = None

    print()
    print('========== RESULTADOS DA BUSCA ONLINE ==========')
    print('Sucesso:', 'Sim' if resultado_online['sucesso'] else 'Não')
    print('Movimentos:', resultado_online['movimentos'])
    print('Custo real percorrido:', resultado_online['custo_real'])
    print('Células reveladas:', resultado_online['celulas_reveladas'])
    print('Células revisitadas:', resultado_online['celulas_revisitadas'])
    print('Replanejamentos:', resultado_online['replanejamentos'])
    print(f"Tempo(ms): {resultado_online['tempo'] * 1000:.3f}")
    print('Custo ótimo offline:', custo_offline)

    if razao is not None:
        print(f'Razão online/offline: {razao:.3f}')
    else:
        print('Razão online/offline: não calculada')

    print()
    print('========== TRAJETÓRIA ONLINE NO MAPA REAL ==========')
    print(desenhar_trajetoria(mapa, resultado_online['trajetoria']))

    salvar_csv_online(resultado_online, custo_offline, razao)

    print()
    print('Resultado da Semana 3 salvo em: resultados/resultado_online.csv')
    print('=' * 105)


if __name__ == '__main__':
    
    executar_semana1()
    executar_semana2()
    executar_semana3()
   