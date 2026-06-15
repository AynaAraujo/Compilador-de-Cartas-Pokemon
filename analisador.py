from lark import Lark, Transformer
import json

# ==========================================
# 1. GRAMÁTICA ATUALIZADA (LARK)
# ==========================================
analisador = Lark(r"""
    ?start: definicao_decks sequencia_rounds
    
    definicao_decks: deck_player1 deck_player2 "INICIAR" "BATALHA"
    deck_player1: "DECK" "Jogador1" "[" string_lista "]"
    deck_player2: "DECK" "Jogador2" "[" string_lista "]"
    string_lista: STRING ("," STRING)*

    sequencia_rounds: round+
    round: "ROUND" INT ":" turno_p1 turno_p2
    
    turno_p1: "TURNO" "Jogador1" ":" acao
    turno_p2: "TURNO" "Jogador2" ":" acao
    
    ?acao: atacar | recuar | energizar | passar
    atacar: "ATACAR" INT
    recuar: "RECUAR" STRING
    energizar: "ENERGIZAR" STRING
    passar: "PASSAR"

    STRING: ESCAPED_STRING
    
    %import common.ESCAPED_STRING
    %import common.INT
    %ignore /[ \t\n\r]+/
    %ignore /#[^\n]*/
""", start='start')


tree = analisador.parse('''
DECK Jogador1 [ "Weedle", "Charmander", "Vulpix", "Pikachu", "Geodude" ]
DECK Jogador2 [ "Caterpie", "Squirtle", "Bulbasaur", "Eevee", "Meowth" ]
INICIAR BATALHA

ROUND 1:
    TURNO Jogador1: ATACAR 1
    TURNO Jogador2: ATACAR 2

ROUND 2:
    TURNO Jogador1: RECUAR "Charmander"
    TURNO Jogador2: ATACAR 1

ROUND 3:
    TURNO Jogador1: ATACAR 1
    TURNO Jogador2: PASSAR
''')

print(tree.pretty())

