from lark import *


# ==========================================
# 2. MEMÓRIA E MOTOR DO JOGO
# ==========================================
class JogoEstado:
    def __init__(self, db_cartas):
        self.db = db_cartas
        self.p1_pontos = 0
        self.p2_pontos = 0
        self.p1_mao = []
        self.p2_mao = []
        self.p1_ativo = None
        self.p2_ativo = None

    def carregar_deck(self, lista_nomes):
        deck_instanciado = []
        for nome in lista_nomes:
            if nome not in self.db:
                raise NameError(f"❌ Erro Semântico: A carta '{nome}' não existe no banco de dados.")
            
            carta_original = self.db[nome]
            
            # Validação semântica de escopo (Apenas Pokémons Básicos)
            if "Basic" not in carta_original.get("subtypes", []):
                raise TypeError(f"❌ Erro Semântico: A carta '{nome}' é {carta_original['subtypes'][0]}. Apenas Pokémons Básicos são permitidos!")

            deck_instanciado.append({
                "name": carta_original["name"],
                "hp": int(carta_original["hp"]),
                "hp_atual": int(carta_original["hp"]),
                "types": carta_original["types"],
                "attacks": carta_original["attacks"],
                "weaknesses": carta_original.get("weaknesses", []),
                "resistances": carta_original.get("resistances", []),
                "energias": {}
            })
        return deck_instanciado

    def formatar_pokemon(self, p):
        if not p: return "Nenhum"
        lista_eng = [f"{qtd} {tipo}" for tipo, qtd in p['energias'].items()]
        txt_energia = ", ".join(lista_eng) if lista_eng else "Nenhuma"
        ataques = ", ".join([f"{i+1}-{a['name']}(Dano:{a['damage']})" for i, a in enumerate(p['attacks'])])
        fraqueza = p['weaknesses'][0]['type'] if p['weaknesses'] else "Nenhuma"
        resistencia = p['resistances'][0]['type'] if p['resistances'] else "Nenhuma"
        return f"{p['name']} | HP: {p['hp_atual']}/{p['hp']} | Tipo: {p['types'][0]} | Ataques: [{ataques}] | Fraqueza: {fraqueza} | Resistência: {resistencia} | Energias: [{txt_energia}]"

    def mostrar_painel(self, jogador_da_vez):
        print("-" * 95)
        if jogador_da_vez == "Jogador1":
            print(f"👉 TURNO JOGADOR 1 (Placar: {self.p1_pontos} pontos)")
            print(f"P1's Pokémon: {self.formatar_pokemon(self.p1_ativo)}")
            print(f"P2's Pokémon: {self.formatar_pokemon(self.p2_ativo)}")
        else:
            print(f"👉 TURNO JOGADOR 2 (Placar: {self.p2_pontos} pontos)")
            print(f"P2's Pokémon: {self.formatar_pokemon(self.p2_ativo)}")
            print(f"P1's Pokémon: {self.formatar_pokemon(self.p1_ativo)}")
        print("-" * 95)


# ==========================================
# 3. INTERPRETADOR RECURSIVO (MATCH/CASE)
# ==========================================
def avalie(tree, estado: JogoEstado):
    # Se chegarmos em um nó terminal que não é uma Tree do Lark, interrompemos
    if not isinstance(tree, Tree):
        return tree

    match tree.data:
        case "start":
            # Avalia a definição dos decks e depois a sequência de rounds
            avalie(tree.children[0], estado)
            avalie(tree.children[1], estado)

        case "definicao_decks":
            # Avalia o nó do deck 1 e deck 2 para preencher as listas de strings
            nomes_p1 = avalie(tree.children[0], estado)
            nomes_p2 = avalie(tree.children[1], estado)
            
            estado.p1_mao = estado.carregar_deck(nomes_p1)
            estado.p2_mao = estado.carregar_deck(nomes_p2)

            estado.p1_ativo = estado.p1_mao.pop(0)
            estado.p2_ativo = estado.p2_mao.pop(0)
            print("\n=== ROUND 0: Decks Carregados e Validados (Match Tree Ativo) ===")

        case "deck_player1" | "deck_player2":
            # Delega para o filho 'string_lista' retornar a lista de strings limpa
            return avalie(tree.children[0], estado)

        case "string_lista":
            # Limpa as aspas de cada Token de string na lista
            return [str(filho).replace('"', '') for filho in tree.children]

        case "sequencia_rounds":
            for node_round in tree.children:
                avalie(node_round, estado)

        case "round":
            num_round = str(tree.children[0])
            print(f"\n================================== ROUND {num_round} ==================================")
            # Executa o turno P1, depois o turno P2 sequencialmente
            avalie(tree.children[1], estado)
            avalie(tree.children[2], estado)

        case "turno_p1":
            estado.mostrar_painel("Jogador1")
            # O filho imediato de turno_p1 é o nó da ação (atacar, recuar, energizar, passar)
            acao_node = tree.children[0]
            executar_acao_motor(estado.p1_ativo, estado.p2_ativo, "Jogador1", acao_node, estado)

        case "turno_p2":
            estado.mostrar_painel("Jogador2")
            acao_node = tree.children[0]
            executar_acao_motor(estado.p2_ativo, estado.p1_ativo, "Jogador2", acao_node, estado)


# ==========================================
# 4. MOTOR DE EXECUÇÃO DE AÇÕES
# ==========================================
def executar_acao_motor(meu_pkmn, oponente_pkmn, jogador, acao_node, estado: JogoEstado):
    match acao_node.data:
        case "passar":
            print(f"-> {jogador} decidiu passar o turno.")

        case "energizar":
            tipo_energia = str(acao_node.children[0]).replace('"', '')
            meu_pkmn["energias"][tipo_energia] = meu_pkmn["energias"].get(tipo_energia, 0) + 1
            print(f"⚡ {jogador} colocou 1 energia de tipo '{tipo_energia}' em {meu_pkmn['name']}.")
            print(f"Status Atualizado -> {estado.formatar_pokemon(meu_pkmn)}")

        case "recuar":
            target = str(acao_node.children[0]).replace('"', '')
            mao_atual = estado.p1_mao if jogador == "Jogador1" else estado.p2_mao
            
            p_novo = next((p for p in mao_atual if p['name'] == target), None)
            if not p_novo:
                raise ValueError(f"❌ Erro Semântico: {target} não está na mão do {jogador} para poder entrar em campo!")

            mao_atual.remove(p_novo)
            if jogador == "Jogador1":
                mao_atual.append(estado.p1_ativo)
                estado.p1_ativo = p_novo
            else:
                mao_atual.append(estado.p2_ativo)
                estado.p2_ativo = p_novo
            print(f"🔄 Recuo efetuado! {target} agora é o Pokémon ativo de {jogador}.")

        case "atacar":
            idx = int(acao_node.children[0]) - 1
            ataque = meu_pkmn['attacks'][idx]
            dano_base = int(ataque['damage']) if ataque['damage'] else 0
            
            # Modificadores de Dano (Fraqueza e Resistência)
            multiplicador = 2 if oponente_pkmn['weaknesses'] and oponente_pkmn['weaknesses'][0]['type'] == meu_pkmn['types'][0] else 1
            reducao = int(oponente_pkmn['resistances'][0]['value'].replace('-', '')) if oponente_pkmn['resistances'] and oponente_pkmn['resistances'][0]['type'] == meu_pkmn['types'][0] else 0
            
            dano_final = max(0, (dano_base * multiplicador) - reducao)
            oponente_pkmn['hp_atual'] = max(0, oponente_pkmn['hp_atual'] - dano_final)
            
            print(f"💥 {meu_pkmn['name']} usou {ataque['name']} causando {dano_final} de dano!")
            print(f"Status Oponente -> {estado.formatar_pokemon(oponente_pkmn)}")

            # Verificação de Nocaute
            if oponente_pkmn['hp_atual'] <= 0:
                print(f"💀 {oponente_pkmn['name']} foi nocauteado!")
                if jogador == "Jogador1":
                    estado.p1_pontos += 1
                    if estado.p2_mao: estado.p2_ativo = estado.p2_mao.pop(0)
                else:
                    estado.p2_pontos += 1
                    if estado.p1_mao: estado.p1_ativo = estado.p1_mao.pop(0)

