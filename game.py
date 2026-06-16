# game.py
class JogoEstado:
    def __init__(self, db_cartas):
        self.db = db_cartas
        self.p1_pontos = 0
        self.p2_pontos = 0
        self.p1_banco = []
        self.p2_banco = []
        self.p1_ativo = None
        self.p2_ativo = None

    def carregar_deck(self, lista_nomes):
        deck_instanciado = []
        for nome in lista_nomes:
            if nome not in self.db:
                raise NameError(f"❌ Erro Semântico: A carta '{nome}' não existe no banco de dados.")
            
            carta_original = self.db[nome]

            deck_instanciado.append({
                "name": carta_original["name"],
                "hp": int(carta_original["hp"]),
                "hp_atual": int(carta_original["hp"]),
                "types": carta_original["types"],
                "attacks": carta_original["attacks"],
                "weaknesses": carta_original.get("weaknesses", []),
                "resistances": carta_original.get("resistances", []),
                "energias_total": 0  # Inicializa o contador numérico simples de marcadores
            })
        return deck_instanciado

    def formatar_pokemon(self, p):
        if not p: return "Nenhum (Nocauteado)"
        
        # Mapeia e formata os ataques exibindo o custo numérico antes de selecionar a ação
        ataques_formatados = []
        for a in p['attacks']:
            custo = a.get('cost', 0)
            ataques_formatados.append(f"{a['name']} [Dano:{a['damage']} | Custo:{custo} eng]")
        txt_ataques = " / ".join(ataques_formatados)
        
        fraqueza = f"{p['weaknesses'][0]['type']} ({p['weaknesses'][0]['value']})" if p['weaknesses'] else "Nenhuma"
        resistencia = f"{p['resistances'][0]['type']} ({p['resistances'][0]['value']})" if p['resistances'] else "Nenhuma"
        
        # Exibe de forma limpa a quantidade acumulada de marcadores de energia
        return f"{p['name']} | HP: {p['hp_atual']}/{p['hp']} | TIPO: {p['types']} | ENERGIAS: {p['energias_total']} | FRAQUEZA: {fraqueza} | RESISTENCIA: {resistencia} \n   └─ ATAQUES DISPONÍVEIS: {txt_ataques}"

    def mostrar_painel(self, jogador_da_vez):
        print("\n" + "="*45 + " STATUS DA ARENA " + "="*45)
        if jogador_da_vez == "Jogador1":
            print(f"P1's: {self.p1_pontos} pontos")
            print(f"P1's Pokémon: {self.formatar_pokemon(self.p1_ativo)}")
            print(f"P2's Pokémon: {self.formatar_pokemon(self.p2_ativo)}")
        else:
            print(f"P2's: {self.p2_pontos} pontos")
            print(f"P2's Pokémon: {self.formatar_pokemon(self.p2_ativo)}")
            print(f"P1's Pokémon: {self.formatar_pokemon(self.p1_ativo)}")
        print("="*105)