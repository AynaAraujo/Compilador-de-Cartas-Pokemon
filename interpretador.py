# interpretador.py
import re
from lark import Tree
from game import JogoEstado

# =========================================================================
# FUNCTIONS EXECUTADAS PELO INTERPRETADOR INTERATIVO (REPL)
# =========================================================================

def executar_round_zero(estado: JogoEstado):
    print("\n=========================================================================================")
    print("                                       ROUND 0")
    print("=========================================================================================")
    print("Mãos/Bancos carregados com sucesso do arquivo JSON!")
    print(f"Banco do Jogador 1: {', '.join([p['name'] for p in estado.p1_banco])}")
    print(f"Banco do Jogador 2: {', '.join([p['name'] for p in estado.p2_banco])}")
    
    estado.p1_ativo = estado.p1_banco.pop(0)
    estado.p2_ativo = estado.p2_banco.pop(0)
    print("\nPokémons iniciais enviados para o campo!")


def escolher_novo_ativo_obrigatorio(nome_jogador, meu_banco, estado: JogoEstado):
    if not meu_banco:
        return False
    print(f"Opções disponíveis no banco: {', '.join([p['name'] for p in meu_banco])}")
    
    escolha = input(f"Digite o nome do Pokémon para entrar em campo ativo: ").strip()
    p_novo = next((p for p in meu_banco if p['name'].lower() == escolha.lower()), None)
    if not p_novo:
        p_novo = meu_banco.pop(0)
        print(f"⚠️ Opção inválida. O sistema promoveu automaticamente o primeiro do banco: {p_novo['name']}")
    else:
        meu_banco.remove(p_novo)
        
    if nome_jogador == "Jogador1":
        estado.p1_ativo = p_novo
    else:
        estado.p2_ativo = p_novo
    print(f"📥 {p_novo['name']} entrou em campo como o novo Pokémon ativo de {nome_jogador}!")
    return True


def verificar_e_repor_ativos_obrigatorios(estado: JogoEstado):
    if estado.p1_ativo is None:
        print("\n💥 Jogador 1 precisa substituir seu Pokémon nocauteado!")
        if not escolher_novo_ativo_obrigatorio("Jogador1", estado.p1_banco, estado):
            print("\n💀 Jogador 1 não tem mais Pokémons no banco para substituir!")
            return False

    if estado.p2_ativo is None:
        print("\n💥 Jogador 2 precisa substituir seu Pokémon nocauteado!")
        if not escolher_novo_ativo_obrigatorio("Jogador2", estado.p2_banco, estado):
            print("\n💀 Jogador 2 não tem mais Pokémons no banco para substituir!")
            return False
            
    return True


def gerenciar_input_turno(nome_jogador, meu_pkmn, oponente_pkmn, meu_banco, estado: JogoEstado):
    print(f"\n🤔 {nome_jogador} [{meu_pkmn['name']} | HP:{meu_pkmn['hp_atual']} | Energias:{meu_pkmn['energias_total']}], qual ação deseja realizar?")
    print("1 - ATACAR")
    print("2 - RECUAR")
    print("3 - ENERGIZAR (+1 Marcador de Energia)")
    print("4 - PASSAR")
    
    escolha = input("Digite o número da ação: ").strip()
    
    match escolha:
        case "4":
            print(f"-> {nome_jogador} decidiu passar o turno.")
            
        case "3":
            meu_pkmn["energias_total"] += 1
            print(f"⚡ {nome_jogador} colocou 1 energia em {meu_pkmn['name']}.")
            print(f"Status Atualizado -> HP: {meu_pkmn['hp_atual']} | Energias: {meu_pkmn['energias_total']}")
            
        case "2":
            if not meu_banco:
                print("❌ Você não tem Pokémons disponíveis no banco para recuar! Turno perdido.")
                return
            print(f"Pokémons disponíveis no seu banco: {', '.join([p['name'] for p in meu_banco])}")
            target = input("Digite o nome do Pokémon que sairá do banco: ").strip()
            
            p_novo = next((p for p in meu_banco if p['name'].lower() == target.lower()), None)
            if not p_novo:
                print("❌ Pokémon inválido ou não encontrado no banco! Turno perdido.")
                return
                
            meu_banco.remove(p_novo)
            meu_banco.append(meu_pkmn)
            if nome_jogador == "Jogador1":
                estado.p1_ativo = p_novo
            else:
                estado.p2_ativo = p_novo
            print(f"🔄 Recuo efetuado com sucesso! {p_novo['name']} entrou em campo.")
            
        case "1":
            print(f"\nSeleção de Ataque para {meu_pkmn['name']}:")
            for i, a in enumerate(meu_pkmn['attacks']):
                print(f"{i+1} - {a['name']} (Dano Base: {a['damage']} | Requisito: {a.get('cost', 0)} energia(s))")
                
            try:
                idx_input = int(input("Digite o número do ataque desejado: ")) - 1
                if idx_input < 0 or idx_input >= len(meu_pkmn['attacks']):
                    print("❌ Opção de ataque inexistente! Turno perdido.")
                    return
            except ValueError:
                print("❌ Entrada inválida! Turno perdido.")
                return
                
            ataque = meu_pkmn['attacks'][idx_input]
            
            custo_requerido = int(ataque.get("cost", 0))
            if meu_pkmn["energias_total"] < custo_requerido:
                print(f"❌ Erro Semântico: {meu_pkmn['name']} tentou usar '{ataque['name']}' (Requer: {custo_requerido}), mas possui apenas {meu_pkmn['energias_total']} marcador(es)!")
                print("Turno perdido devido à falha de recursos.")
                return
            
            dano_limpo = re.sub(r'\D', '', ataque['damage'])
            dano_base = int(dano_limpo) if dano_limpo else 0

            multiplicador = 1
            if oponente_pkmn['weaknesses'] and oponente_pkmn['weaknesses'][0]['type'] == meu_pkmn['types']:
                val_weak = oponente_pkmn['weaknesses'][0]['value']
                if "x2" in val_weak or "×2" in val_weak: multiplicador = 2
                elif "+20" in val_weak: dano_base += 20

            reducao = 0
            if oponente_pkmn['resistances'] and oponente_pkmn['resistances'][0]['type'] == meu_pkmn['types']:
                reducao = abs(int(oponente_pkmn['resistances'][0]['value']))

            dano_final = max(0, (dano_base * multiplicador) - reducao)
            oponente_pkmn['hp_atual'] = max(0, oponente_pkmn['hp_atual'] - dano_final)
            
            print(f"\n💥 {meu_pkmn['name']} usou {ataque['name']}!")
            print(f"👉 Causou {dano_final} de dano real em {oponente_pkmn['name']}.")

            if oponente_pkmn['hp_atual'] <= 0:
                print(f"💀 {oponente_pkmn['name']} foi nocauteado!")
                if nome_jogador == "Jogador1":
                    estado.p1_pontos += 1
                    estado.p2_ativo = None
                else:
                    estado.p2_pontos += 1
                    estado.p1_ativo = None
        case _:
            print("❌ Comando inválido selecionado! Turno perdido.")


def loop_principal_batalha(estado: JogoEstado):
    num_round = 1
    while estado.p1_pontos < 3 and estado.p2_pontos < 3:
        print(f"\n=========================================================================================")
        print(f"                                       ROUND {num_round}")
        print(f"=========================================================================================")
        
        if not verificar_e_repor_ativos_obrigatorios(estado):
            break

        estado.mostrar_painel("Jogador1")
        gerenciar_input_turno("Jogador1", estado.p1_ativo, estado.p2_ativo, estado.p1_banco, estado)

        if estado.p1_pontos >= 3: 
            break

        print("\n" + "." * 105 + "\n")

        if not verificar_e_repor_ativos_obrigatorios(estado):
            break

        estado.mostrar_painel("Jogador2")
        gerenciar_input_turno("Jogador2", estado.p2_ativo, estado.p1_ativo, estado.p2_banco, estado)
                
        num_round += 1

    print("\n=========================================================================================")
    print("                                      FIM DE JOGO!")
    print("=========================================================================================")
    if estado.p1_pontos >= 3 or not estado.p2_banco and estado.p2_ativo is None:
        print("🏆 PARABÉNS! JOGADOR 1 É O VENCEDOR DA PARTIDA!")
    elif estado.p2_pontos >= 3 or not estado.p1_banco and estado.p1_ativo is None:
        print("🏆 PARABÉNS! JOGADOR 2 É O VENCEDOR DA PARTIDA!")


# ==========================================
# 4. FUNÇÃO PRINCIPAL DE ENTRADA DO INTERPRETADOR
# ==========================================
def avalie(tree, estado: JogoEstado):
    if not isinstance(tree, Tree):
        return tree

    match tree.data:
        case "start":
            avalie(tree.children[0], estado)

        case "definicao_decks":
            nomes_p1 = avalie(tree.children[0], estado)
            nomes_p2 = avalie(tree.children[1], estado)
            
            estado.p1_banco = estado.carregar_deck(nomes_p1)
            estado.p2_banco = estado.carregar_deck(nomes_p2)

            executar_round_zero(estado)
            loop_principal_batalha(estado)

        case "deck_player1" | "deck_player2":
            return avalie(tree.children[0], estado)

        case "string_lista":
            nomes_limpos = []
            for child in tree.children:
                itens = child.children if isinstance(child, Tree) else [child]
                for item in itens:
                    texto = str(item)
                    texto = texto.strip().strip('"').strip("'").strip('“').strip('”')
                    if texto:
                        nomes_limpos.append(texto)
            return nomes_limpos