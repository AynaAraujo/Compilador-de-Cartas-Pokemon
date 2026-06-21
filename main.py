# main.py
import json
import sys
from analisador import analisador_pokemon
from game import DeckError, JogoEstado
from interpretador import avalie

def rodar_simulador(caminho_script_pok):
    # 1. Carrega a base de dados de cartas local
    try:
        with open("data/base_cartas_pokemon.json", "r", encoding="utf-8") as f:
            dados_json = json.load(f)
    except FileNotFoundError:
        print("❌ Erro: O arquivo 'data/base_cartas_pokemon.json' não foi encontrado.")
        return
    
    # Filtra e indexa o banco de dados pelo nome do Pokémon para busca rápida O(1)
    # Filtra e indexa o banco de dados removendo espaços extras ocultos nas chaves
    db_cartas = {c["name"].strip(): c for c in dados_json}

    # 2. Lê o arquivo de script da DSL contendo a batalha
    try:
        with open(caminho_script_pok, "r", encoding="utf-8") as f:
            script_batalha = f.read()
    except FileNotFoundError:
        print(f"❌ Erro: O script '{caminho_script_pok}' não foi encontrado.")
        return

    print(f"🔍 Carregando script: {caminho_script_pok}...")

    try:
        # 3. Análise Sintática: Lark gera a Árvore de Sintaxe Abstrata (AST)
        arvore_ast = analisador_pokemon.parse(script_batalha)
        
        # 4. Inicializa a memória/estado do jogo passando o banco de dados carregado
        estado_partida = JogoEstado(db_cartas)
        
        # 5. Execução: Dispara o interpretador recursivo baseado em match/case
        avalie(arvore_ast, estado_partida)
        
        print("\n🏆 Simulação concluída com sucesso!")

    except (TypeError, ValueError, DeckError) as erro_semantico:
        # Captura as exceções de regras de negócio tratadas pelo interpretador
        print(f"\n{erro_semantico}")
        print("🚫 Execução abortada pelo Analisador Semântico.")
        
    except Exception as erro_generico:
        # Captura eventuais erros de sintaxe do Lark ou falhas inesperadas
        print(f"\n❌ Erro de Execução/Sintaxe: {erro_generico}")


if __name__ == "__main__":
    # Permite passar o script .pok via linha de comando (Ex: python main.py batalha.pok)
    # Se não passar nada, ele tenta rodar um padrão 'batalha.pok'
    arquivo_teste = sys.argv[1] if len(sys.argv) > 1 else "batalha.pok"
    rodar_simulador(arquivo_teste)