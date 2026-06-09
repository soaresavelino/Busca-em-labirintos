# Uso de Inteligência Artificial no Trabalho

Durante o desenvolvimento deste trabalho, foram utilizadas ferramentas de Inteligência Artificial como apoio para organização das ideias, revisão do código e correção de erros.
A IA foi utilizada como ferramenta de auxílio ao aprendizado, principalmente para tirar dúvidas, revisar trechos do código, entender melhor os algoritmos implementados e organizar as métricas exigidas no trabalho. O uso da IA não substituiu o entendimento do grupo, pois as sugestões foram analisadas, testadas e adaptadas antes de serem utilizadas.

## 1. Ferramentas utilizadas

Foram utilizadas as seguintes ferramentas de Inteligência Artificial:

- Gemini, para apoio na estruturação inicial da Semana 1 e Semana 2, principalmente na parte de busca clássica, organização da classe do labirinto, renderização e métricas;
- ChatGPT, para apoio na estruturação inicial da Semana 3, explicação dos algoritmos, apoio nas partes de busca clássica, busca local e busca online.

## 2. Principais prompts utilizados

Alguns dos principais prompts utilizados foram:

- “Como posso estruturar uma classe LabirintoBusca em Python para representar um ambiente discreto usando matrizes?”
- “Meu código está dando erro AttributeError ao tentar acessar mapa_original na função de visualização. Como posso corrigir a estrutura do **init** e do método renderizar?”
- “Quais métricas são essenciais para comparar algoritmos de busca BFS, DFS, UCS e A\* em um ambiente acadêmico?”
- “Como posso otimizar o método de renderização via terminal para que ele seja mais eficiente e não repita código?”
- “Explicar a diferença entre busca clássica, busca local e busca online.”
- “Explique como funciona a busca online em um labirinto desconhecido.”

## 3. Trechos de código sugeridos por IA

A IA auxiliou com sugestões relacionadas à organização e revisão de partes do código, principalmente em: organização da classe responsável pelo labirinto, implementação do método de renderização no terminal, uso de uma função auxiliar interna para marcar visitados e caminho, sugestão de uso de `@dataclass` para facilitar o armazenamento das métricas, centralização da execução dos algoritmos para evitar repetição de código e explicação da lógica dos algoritmos.

## 4. Sugestões rejeitadas

Algumas sugestões da IA não foram utilizadas, pois não se encaixavam na proposta do trabalho. Entre as sugestões rejeitadas, estão: uso de bibliotecas externas mais complexas para visualização, criação de uma interface gráfica elaborada, implementação de algoritmos extras que não eram obrigatórios e geração de animações mais complexas.

## 5. Erros cometidos pela IA

Durante o uso da IA, alguns erros ou sugestões imprecisas apareceram, como:

- em uma das iterações, a IA sugeriu passar `nos_explorados`, que era um contador inteiro, para a função de renderização, o que gerou o erro `TypeError: 'int' object is not iterable`;
- a correção foi feita manualmente pelo grupo, identificando que a função esperava uma lista de coordenadas, chamada `estados_explorados`, e não apenas um número inteiro;

## 6. Como o grupo validou a solução

A validação do projeto foi feita por meio de testes com os mapas disponíveis na pasta `mapas`.
Foram verificados:

- Testes unitários manuais: Rodamos os algoritmos em labirintos de teste (Pequeno,
  Médio e Grande) e comparamos a saída do terminal com o esperado.
- Depuração: Verificamos se o custo de caminho e o número de nós expandidos
  faziam sentido lógico (ex: BFS expandindo mais nós que A\*).
- Conferência da Rubrica: Validamos se o método de renderização atendia aos 3
  primeiros requisitos da seção "8. Visualização Obrigatória".
- se BFS, DFS, UCS, Busca Gulosa e A\* executavam corretamente;
- se a visualização no terminal representava corretamente o mapa, o caminho e os estados visitados;
- se Hill-Climbing e Simulated Annealing geravam custos e curvas de convergência;

## 7. Modificações feitas pelo grupo

As sugestões da IA foram adaptadas ao projeto. O grupo realizou modificações como: ajustes na estrutura da classe do labirinto, correção do erro envolvendo `nos_explorados` e `estados_explorados`, revisão da lógica dos algoritmos, revisão das métricas e validação manual dos resultados gerados.

O grupo também escolheu representar os nós expandidos e visitados pelo mesmo caractere na visualização, para manter a clareza visual. Essa escolha foi feita considerando que, na busca clássica, todo nó expandido também pode ser considerado visitado.

## 8. Uso da IA em cada parte do trabalho

### Busca clássica

Na busca clássica, a IA auxiliou na estruturação da classe do labirinto e na revisão dos algoritmos BFS, DFS, UCS, Busca Gulosa e A\*. Também ajudou na organização das métricas exigidas no trabalho, como custo do caminho, quantidade de nós explorados, nós expandidos, tempo de execução e tamanho máximo da fronteira.

### Busca local

Na busca local, a IA ajudou a compreender a representação da solução como uma ordem de visitação dos pontos de coleta. Também auxiliou na explicação dos métodos Hill-Climbing e Simulated Annealing, além da análise dos custos encontrados e da curva de convergência.

### Busca online

Na busca online, a IA auxiliou na explicação do comportamento do agente em um ambiente desconhecido. O agente percebe o ambiente aos poucos, atualiza seu mapa interno e toma decisões com base nas informações disponíveis naquele momento.

## 9. Conclusão sobre o uso da IA

O uso de Inteligência Artificial contribuiu para desenvolvimento do código e corrigir erros. No entanto, o entendimento dos algoritmos, os testes, as adaptações e a validação dos resultados foram realizados pelo grupo.
