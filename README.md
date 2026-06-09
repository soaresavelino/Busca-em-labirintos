# Trabalho Prático – Agente Inteligente em Labirinto

Este projeto foi desenvolvido para a disciplina de Inteligência Artificial e tem como objetivo implementar um agente inteligente capaz de atuar em labirintos discretos, utilizando três abordagens diferentes de busca:

1. Busca clássica em labirinto conhecido;
2. Busca local com pontos de coleta obrigatórios;
3. Busca online em labirinto desconhecido.

O ambiente é representado por uma matriz, em que cada caractere indica um tipo de célula do labirinto.

## Legenda dos mapas

| Símbolo | Significado                        |
| ------- | ---------------------------------- |
| `A`     | Posição inicial do agente          |
| `B`     | Objetivo final                     |
| `C`     | Ponto de coleta obrigatório        |
| `#`     | Parede ou obstáculo                |
| espaço  | Caminho livre                      |
| `?`     | Célula desconhecida no modo online |

## Estrutura do projeto

```txt
Busca-em-labirintos-main/
│
├── main.py
├── labirinto.py
├── busca_local.py
├── busca_online.py
├── README.md
├── uso_ia.md
│
├── mapas/
│   ├── maze1.txt
│   ├── maze2.txt
│   ├── maze3.txt
│   └── mapa_online.txt
│
├── resultados/
└── graficos/
```

Parte 1 - Busca Clássica

Na primeira parte, o agente conhece todo o mapa desde o início e deve encontrar um caminho da posição inicial A até o objetivo B.
Foram implementados os seguintes algoritmos: Busca em Largura, Busca em Profundidade, Busca de Custo Uniforme, Busca Gulosa, A\*.
Para cada algoritmo, são coletadas as seguintes métricas: sucesso ou falha, custo do caminho, tamanho do caminho, número de nós explorados, número de nós expandidos, tempo de execução e tamanho máximo da fronteira.
Os resultados são exibidos no terminal e salvos no arquivo: resultados.csv

Parte 2 – Busca Local com Pontos de Coleta

Na segunda parte, o labirinto possui pontos de coleta obrigatórios indicados por C. O agente deve sair de A, visitar todos os pontos de coleta e terminar em B.
A solução é representada por uma ordem de visitação dos pontos de coleta.
Foram implementados os seguintes algoritmos: Hill-Climbing e Simulated Annealing.
A vizinhança utilizada consiste na troca de posição entre dois pontos de coleta dentro da rota.
O custo da solução é calculado pela soma das menores distâncias entre os pontos da rota:

A → C1 → C2 → ... → Ck → B

A busca local gera gráficos de desempenho:
convergencia_coletas_semana2.png
comparacao_custos.png

Parte 3 – Busca Online

Na terceira parte, o agente não conhece o mapa completo desde o início. O mapa real é utilizado apenas pelo simulador. O agente mantém um mapa interno inicialmente desconhecido, preenchido com ?.
A cada passo, o agente executa o ciclo:
perceber → atualizar mapa interno → planejar → agir
A estratégia utilizada foi Online DFS.
O agente percebe as células vizinhas, atualiza seu mapa interno e escolhe um caminho ainda não visitado. Quando não há vizinhos livres não visitados, ele retorna pelo caminho anterior.

Foram coletadas as seguintes métricas: sucesso ou falha, número total de movimentos, custo real percorrido,número de células reveladas, comparação com o caminho ótimo offline, razão online/offline.

Os resultados da busca online são salvos em:
resultados/resultado_online.csv

Como executar o projeto: Primeiro, instale a biblioteca necessária para os gráficos: pip install matplotlib
Depois, execute: python main.py
