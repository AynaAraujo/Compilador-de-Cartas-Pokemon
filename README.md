# ⚔️ Pokémon TCG DSL & REPL Battle Simulator

Uma Linguagem de Domínio Específico (DSL) desenvolvida em **Python** utilizando a biblioteca **Lark** para inicialização de estado de ambiente e um motor interpretador interativo de turnos via CLI (Terminal).

Este projeto foi desenvolvido como requisito para a disciplina de **Compiladores UPE**.

---

## 📂 Estrutura de Arquivos do Projeto

```text
Compilador-de-Cartas-Pokemon/
├── data/
│   └── base_cartas_pokemon.json    # Banco de dados estático das cartas Pokémon Básicas
├── analisador.py                  # Gramática EBNF e instanciação do Parser Lark
├── game.py                        # Estrutura de memória de estados e painéis do jogo
├── interpretador.py               # Caminhada recursiva na AST (match/case) e REPL
├── main.py                        # Ponto de entrada (Entrypoint) da aplicação
└── README.md                      # Documentação do repositório

```

---

## 📋 Escopo do MVP & Regras do Jogo

Para garantir a estabilidade do compilador e a entrega dentro do prazo, o escopo foi delimitado sob as seguintes regras:

* **Apenas Pokémons Básicos:** Mecânicas de evolução (Stage 1 / Stage 2) são desconsideradas.
* **Tamanho do Deck:** Cada jogador deve compor seu deck com exatamente **5 cartas de Pokémons** no arquivo de inicialização.
* **Arena 1v1 Dinâmica:** Há um Pokémon ativo por jogador em campo e os demais permanecem no banco de retaguarda. Quando um Pokémon ativo é nocauteado, o jogador é obrigado a promover um substituto, mantendo a posse do seu turno subsequente.
* **Marcadores de Energia Simplificados:** A ação de energizar adiciona `+1 marcador genérico` ao Pokémon ativo, eliminando a seleção manual de tipos de energia para maior fluidez.
* **Validação Semântica de Custo:** O interpretador realiza a checagem em tempo de execução e impede ataques caso o total de energias ligadas ao Pokémon ativo seja menor que o requisito exigido pela carta.
* **Persistência no Recuo:** Os Pokémons preservam intactas todas as suas energias anexadas ao recuarem para o banco.
* **Condição de Vitória:** O jogo termina quando um jogador atinge **3 pontos de nocaute** OU se o oponente não tiver mais cartas no banco para repor o campo.
* **Cálculo de Dano Dinâmico:** Modificadores de **Fraqueza** (Dano bruto modificado via JSON) e **Resistência** são aplicados automaticamente comparando os tipos elementares na Arena.

---

## 🛠️ Arquitetura do Compilador

Este projeto adota uma arquitetura clássica de **Avaliação Dirigida por Sintaxe** usando caminhada explícita e recursiva pela árvore sintática:

1. **Análise Sintática (Lark):** O arquivo fonte `.pok` é processado por uma gramática EBNF que valida unicamente a estrutura de carregamento dos decks.
2. **Interpretador Baseado em Padrões:** A função recursiva `avalie` varre os nós estruturados da árvore de sintaxe abstrata utilizando o recurso de **Structural Pattern Matching (`match tree.data`)** nativo do Python.
3. **Loop de Execução Interativo (REPL):** Após ler o comando `INICIAR BATALHA`, o interpretador inicia a rotina interativa de console via teclado (`input()`), exibindo relatórios polidos e prompts dinâmicos com os dados vitais (`HP` e `Energia`) do jogador ativo da vez.

---

## 💻 Exemplo de Código na DSL (`batalha.pok`)

```text
# --- Inicialização da Mesa com Decks de 5 Cartas ---
DECK Alice [ "Pikachu", "Charmander", "Chansey", "Growlithe", "Ponyta" ]
DECK Bob [ "Squirtle", "Diglett", "Mewtwo", "Bulbasaur", "Caterpie" ]
INICIAR BATALHA
```

A DSL funciona para inicializar dois decks de jogadores e iniciar uma batalha interativa.
Cada deck deve conter exatamente 5 cartas e pode ser declarado em qualquer ordem.
O nome do jogador é livre, contanto que os dois sejam diferentes.

A validação cobre:

* tamanho de deck incorreto
* cartas repetidas no mesmo deck
* cartas não existentes no banco de dados

Arquivos de exemplo para validação:

* `batalha_tamanho_invalido.pok`
* `batalha_repetida.pok`
* `batalha_carta_invalida.pok`

Use qualquer um desses arquivos no lugar de `batalha.pok` para testar os erros de validação diretamente.

---

## 📦 Como Rodar a Aplicação

### Pré-requisitos

* Python 3.10 ou superior
* Biblioteca `lark-parser`

```bash
pip install lark-parser
```

### Execução

Passe o arquivo com a especificação da batalha como argumento por linha de comando:

```bash
python main.py batalha.pok
```
