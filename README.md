
## Trabalho de Inteligência Artificial - Jogo do Pacman
Este repositório contém o código do projeto de Inteligência Artificial aplicado ao jogo Pacman. O projeto é um trabalho desenvolvido pela Universidade de Berkeley e tem como objetivo a implementação de diferentes algoritmos de IA para controlar o comportamento do Pacman.

## Algoritmos Implementados
# Agente Reflexivo:

Este agente toma decisões com base em regras simples que avaliam o estado atual do jogo.
Avalia ações possíveis e escolhe aquela que resulta na melhor pontuação imediata.
# Minimax:

Um algoritmo de decisão que busca minimizar a perda máxima possível (minimizar o dano do pior cenário).
É utilizado para tomar decisões otimizadas em cenários de jogos adversariais.
# Poda Alpha-Beta:

Uma otimização do algoritmo Minimax que reduz o número de nós avaliados na árvore de decisão.
Melhora a eficiência ao eliminar ramos que não precisam ser explorados porque não podem influenciar a decisão final.
# Expectimax:

Uma variação do Minimax que considera a expectativa de utilidade das ações, útil para jogos com elementos de incerteza.
Calcula o valor esperado das ações, ao invés de assumir que o oponente sempre joga para minimizar o ganho.
