# analisador.py
from lark import Lark

analisador_pokemon = Lark(r"""
    ?start: definicao_decks
    
    definicao_decks: deck_player1 deck_player2 "INICIAR" "BATALHA"
    deck_player1: "DECK" "Jogador1" "[" string_lista "]"
    deck_player2: "DECK" "Jogador2" "[" string_lista "]"
    string_lista: STRING ("," STRING)*

    STRING: ESCAPED_STRING
    
    %import common.ESCAPED_STRING
    %ignore /[ \t\n\r]+/
    %ignore /#[^\n]*/
""", start='start')