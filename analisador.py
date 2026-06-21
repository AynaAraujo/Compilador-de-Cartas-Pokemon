# analisador.py
from lark import Lark

analisador_pokemon = Lark(r"""
    ?start: definicao_decks
    
    definicao_decks: deck_def+ "INICIAR" "BATALHA"
    deck_def: "DECK" PLAYER "[" string_lista "]"
    string_lista: STRING ("," STRING)*

    PLAYER: /[A-Za-z][A-Za-z0-9_]*/
    STRING: ESCAPED_STRING
    
    %import common.ESCAPED_STRING
    %ignore /[ \t\n\r]+/
    %ignore /#[^\n]*/
""", start='start')