# ⚔️ Pokémon TCG DSL & Battle Simulator

Uma Linguagem de Domínio Específico (DSL) desenvolvida em **Python** utilizando a biblioteca **Lark** para automatizar, validar e simular batalhas simplificadas de Pokémon Trading Card Game (TCG).

Este projeto foi desenvolvido como requisito para a disciplina de **Compiladores UPE**.

---

## 🎯 Diretriz do Projeto
> **Originalidade + Utilidade > Complexidade**
> O foco do projeto é o mapeamento estrito do domínio de um jogo de cartas, aplicando conceitos fundamentais de compiladores (Análise Sintática, Árvore de Sintaxe Abstrata e Análise Semântica) em um escopo controlado e de alta utilidade prática.

---

## 📋 Escopo do MVP & Regras do Jogo

Para garantir a estabilidade do compilador e a entrega dentro do prazo, o escopo foi delimitado sob as seguintes regras:
* **Apenas Pokémons Básicos:** Mecânicas de evolução (Stage 1 / Stage 2) são desconsideradas.
* **Arena 1v1:** Não há banco de reservas (*bench*). Cada jogador possui apenas um Pokémon ativo por vez.
* **Abstração de Energias:** Não existem cartas físicas de energia no deck. O motor do jogo incrementa automaticamente `+1 Energia` do tipo correspondente ao Pokémon ativo no início de cada turno.
* **Condição de Vitória:** O jogo termina quando um jogador atinge **3 pontos de nocaute** OU se o oponente não tiver mais cartas de Pokémon válidas na mão para substituir um nocauteado.
* **Cálculo de Dano:** Modificadores de **Fraqueza** (Dano $\times$ 2) e **Resistência** (Dano - 20) são aplicados estritamente com base nos tipos elementares.

---

## 🛠️ Arquitetura do Compilador

O fluxo de execução do script `.pok` segue o pipeline clássico de engenharia de compiladores:

1. **Análise Sintática (Lark):** O arquivo fonte é processado por uma gramática EBNF que valida a estrutura dos comandos.
2. **Transformação (AST):** Os tokens aceitos são convertidos em uma Árvore de Sintaxe Abstrata usando `lark.Transformer`.
3. **Análise Semântica (Python):** O interpretador valida as regras de contexto do jogo antes de executar a ação (Ex: Checar se o Pokémon tem energia suficiente para o ataque escolhido).
4. **Execução/Interpretador:** O estado do jogo é atualizado e renderizado diretamente no terminal.

---

## 💻 Exemplo de Código na DSL (`batalha.pok`)

```text
# --- Inicialização e Definição de Decks ---
DECK Jogador1 [ "Weedle", "Charmander", "Vulpix" ]
DECK Jogador2 [ "Caterpie", "Squirtle", "Pikachu" ]
INICIAR BATALHA

# --- Execução de Turnos ---
TURNO Jogador1: ATACAR 1
TURNO Jogador2: PASSAR
TURNO Jogador1: ATACAR 1
