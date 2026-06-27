# PokéLang — DSL para Batalhas de Cartas Pokémon

> Projeto da disciplina de **Compiladores — UPE**

---

## Equipe

Ayna Mariah

Giulia Buonafina

Maria Luana Rodrigues

---

## Motivação e Descrição Informal da Linguagem

Configurar uma partida do Pokémon TCG exige definir decks, validar regras, gerenciar energia, calcular danos com fraquezas e resistências — tudo manualmente. **PokéLang** é uma DSL (Linguagem de Domínio Específico) criada para automatizar exatamente essa tarefa: com um arquivo de texto simples `.pok`, o usuário declara os dois decks e dispara uma batalha interativa completa no terminal, com todas as regras aplicadas automaticamente pelo interpretador.

A linguagem resolve um problema concreto e bem delimitado: **eliminar o trabalho tedioso de configuração e arbitragem de partidas do Pokémon TCG**, servindo como árbitro digital que garante a consistência semântica do jogo (cartas válidas, tamanho correto de deck, custo de energia, cálculo de dano, condição de vitória).

### O que a linguagem faz

- Declara dois decks de jogadores com cartas nomeadas
- Valida léxica, sintática e semanticamente o script antes de iniciar
- Inicializa a arena de batalha automaticamente
- Executa um **REPL interativo por turnos**: cada jogador escolhe sua ação (atacar, recuar, energizar ou passar) via teclado
- Aplica modificadores de fraqueza e resistência conforme os dados de cada carta
- Detecta nocautes, promove substituições obrigatórias e declara o vencedor ao atingir 3 pontos

---

## Arquitetura do Compilador

O projeto segue a **estrutura clássica de um compilador**, com fases bem definidas:

```
Arquivo .pok  →  [Análise Léxica + Sintática]  →  AST  →  [Interpretador]  →  REPL Interativo
                        (Lark / EBNF)             (Lark Tree)   (match/case recursivo)
```

### Fases implementadas

**1. Análise Léxica e Sintática — `analisador.py`**

A gramática é definida formalmente em **EBNF** usando a biblioteca **Lark**. O Lark gera automaticamente o analisador léxico (tokens `PLAYER`, `STRING`, palavras-chave) e o analisador sintático (parser LL), produzindo a Árvore de Sintaxe Abstrata (AST).

```
definicao_decks: deck_def+ "INICIAR" "BATALHA"
deck_def:        "DECK" PLAYER "[" string_lista "]"
string_lista:    STRING ("," STRING)*
```

**2. Geração de AST**

O Lark constrói uma `Tree` estruturada com nós `definicao_decks`, `deck_def` e `string_lista`. Nenhuma AST manual é necessária — a árvore é gerada automaticamente pela gramática.

**3. Interpretador Orientado à Sintaxe — `interpretador.py`**

A função recursiva `avalie(tree, estado)` percorre a AST usando **Structural Pattern Matching** (`match tree.data`), executando a semântica de cada nó. Este é o padrão clássico de **Tradução Dirigida por Sintaxe**.

**4. Análise Semântica — `game.py`**

Regras de negócio verificadas em tempo de execução:
- Exatamente 5 cartas por deck (`DeckSizeError`)
- Sem cartas repetidas no mesmo deck (`DuplicateCardError`)
- Todas as cartas devem existir no banco de dados (`InvalidCardError`)
- Exatamente 2 declarações de `DECK` com nomes distintos

**5. Motor de Execução / REPL — `interpretador.py` + `game.py`**

Após a validação da AST, o interpretador inicia o loop interativo de turnos: exibe o painel de batalha, lê a ação do jogador e aplica os efeitos no estado do jogo.

---

## Estrutura de Arquivos

```
Compilador-de-Cartas-Pokemon/
├── data/
│   └── base_cartas_pokemon.json       # Banco de dados das cartas Pokémon Básicas
├── analisador.py                      # Gramática EBNF e instanciação do Parser Lark
├── game.py                            # Estado do jogo, erros semânticos e painel
├── interpretador.py                   # Caminhada recursiva na AST + REPL interativo
├── main.py                            # Ponto de entrada da aplicação
├── batalha.pok                        # Exemplo: batalha válida
├── batalha_carta_invalida.pok         # Exemplo: erro semântico — carta inexistente
├── batalha_repetida.pok               # Exemplo: erro semântico — carta repetida no deck
├── batalha_tamanho_invalido.pok       # Exemplo: erro semântico — deck com tamanho errado
└── README.md
```

---

## Como Executar

### Pré-requisitos

- **Python 3.10 ou superior** (necessário para o `match/case`)
- Biblioteca **Lark**

```bash
pip install lark-parser
```

### Executando uma batalha

```bash
python main.py batalha.pok
```

O programa irá:
1. Carregar o banco de dados de cartas (`data/base_cartas_pokemon.json`)
2. Ler e analisar o script `.pok`
3. Validar léxico, sintático e semanticamente
4. Iniciar a batalha interativa no terminal

> Se nenhum arquivo for passado, o programa tenta executar `batalha.pok` por padrão.

### Criando sua própria batalha

Você pode criar um arquivo `.pok` personalizado com os jogadores e cartas que quiser. Basta seguir a sintaxe da linguagem:

```
DECK NomeJogador1 [ "Carta1", "Carta2", "Carta3", "Carta4", "Carta5" ]
DECK NomeJogador2 [ "Carta1", "Carta2", "Carta3", "Carta4", "Carta5" ]
INICIAR BATALHA
```

Salve o arquivo com a extensão `.pok` e passe-o como argumento:

```bash
python main.py minha_batalha.pok
```

> Os nomes das cartas devem existir no banco de dados (`data/base_cartas_pokemon.json`). Consulte esse arquivo para ver todas as cartas disponíveis.

---

## Exemplos de Programas

### Batalha válida — `batalha.pok`

```
# --- Inicialização da Mesa com Decks de 5 Cartas ---
DECK Bob   [ "Squirtle", "Diglett", "Mewtwo", "Bulbasaur", "Caterpie" ]
DECK Alice [ "Pikachu", "Charmander", "Chansey", "Growlithe", "Ponyta" ]
INICIAR BATALHA
```

**Saída esperada (início):**

```
🔍 Carregando script: batalha.pok...

=========================================================================================
                                       ROUND 0
=========================================================================================
Mãos/Bancos carregados com sucesso do arquivo JSON!
Banco do Bob: Squirtle, Diglett, Mewtwo, Bulbasaur, Caterpie
Banco do Alice: Pikachu, Charmander, Chansey, Growlithe, Ponyta

Pokémons iniciais enviados para o campo!
```

A partir daí, a batalha ocorre interativamente. A cada turno, o jogador da vez escolhe:

```
🤔 Bob [Squirtle | HP:70 | Energias:0], qual ação deseja realizar?
1 - ATACAR
2 - RECUAR
3 - ENERGIZAR (+1 Marcador de Energia)
4 - PASSAR
Digite o número da ação:
```

---

### Exemplo: Deck com tamanho incorreto — `batalha_tamanho_invalido.pok`

```
# Deck 1 com tamanho incorreto (4 cartas)
DECK Alice [ "Pikachu", "Charmander", "Chansey", "Growlithe" ]
DECK Bob   [ "Squirtle", "Diglett", "Mewtwo", "Bulbasaur", "Caterpie" ]
INICIAR BATALHA
```

**Saída:**

```
❌ Erro Semântico: Cada deck deve conter exatamente 5 cartas. Foram encontradas 4 carta(s).
🚫 Execução abortada pelo Analisador Semântico.
```

---

### Exemplo: Carta repetida no deck — `batalha_repetida.pok`

```
# Deck 2 com cartas repetidas
DECK Alice [ "Pikachu", "Charmander", "Chansey", "Growlithe", "Ponyta" ]
DECK Bob   [ "Squirtle", "Diglett", "Mewtwo", "Diglett", "Caterpie" ]
INICIAR BATALHA
```

**Saída:**

```
❌ Erro Semântico: O deck contém cartas repetidas: Diglett.
🚫 Execução abortada pelo Analisador Semântico.
```

---

### Exemplo: Carta inexistente no banco — `batalha_carta_invalida.pok`

```
# Carta inválida no deck
DECK Alice [ "Pikachu", "Charmander", "Chansey", "Growlithe", "Ponyta" ]
DECK Bob   [ "Squirtle", "Diglett", "Mewtwo", "Bulbasaur", "CartaInvalida" ]
INICIAR BATALHA
```

**Saída:**

```
❌ Erro Semântico: A carta 'CartaInvalida' não existe no banco de dados. Cartas válidas: Bulbasaur, Caterpie, ...
🚫 Execução abortada pelo Analisador Semântico.
```

---

## Regras do Jogo (Escopo do MVP)

| Regra | Detalhe |
|-------|---------|
| Tamanho do Deck | Exatamente **5 cartas** por jogador |
| Pokémons aceitos | Apenas **Pokémons Básicos** (sem evolução) |
| Arena | 1 Pokémon ativo + banco de retaguarda por jogador |
| Energia | `+1 marcador genérico` por ação de energizar |
| Custo de ataque | Verificado em tempo de execução |
| Persistência no recuo | Energias anexadas são preservadas |
| Condição de vitória | **3 nocautes** ou oponente sem Pokémons disponíveis |
| Dano | Fraqueza e Resistência aplicadas automaticamente via tipo elemental |
