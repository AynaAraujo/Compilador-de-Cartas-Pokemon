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
                "energias_total": 0
            })
        return deck_instanciado

    def formatar_pokemon(self, p):
        if not p: return "NENHUM POKÉMON EM CAMPO (NOCAUTEADO)"
        
        # Mapeamento e estruturação visual dos ataques
        ataques_formatados = []
        for a in p['attacks']:
            custo = a.get('cost', 0)
            ataques_formatados.append(f"• {a['name']} [Dano: {a['damage']} | Custo: {custo} eng]")
        txt_ataques = "   ".join(ataques_formatados)
        
        fraqueza = f"{p['weaknesses'][0]['type']} ({p['weaknesses'][0]['value']})" if p['weaknesses'] else "Nenhuma"
        resistencia = f"{p['resistances'][0]['type']} ({p['resistances'][0]['value']})" if p['resistances'] else "Nenhuma"
        
        # Quebra de linha adicionada no retorno para distanciar e organizar os ataques visualmente
        return (
            f"🟢 {p['name']}\n"
            f"   [ HP: {p['hp_atual']}/{p['hp']}  |  TIPO: {p['types']}  |  ENERGIAS LIGADAS: {p['energias_total']} ]\n"
            f"   [ FRAQUEZA: {fraqueza}  |  RESISTÊNCIA: {resistencia} ]\n"
            f"   └─ ATAQUES: {txt_ataques}"
        )

    def mostrar_painel(self, jogador_da_vez):
        print("\n" + "🐾 " * 15 + " STATUS DA ARENA DE BATALHA " + "🐾 " * 15 + "\n")
        
        if jogador_da_vez == "Jogador1":
            print(f"🏆 PLACAR JOGADOR 1: {self.p1_pontos} ponto(s)")
            print(f"⭐ MEU CAMPO (P1):\n{self.formatar_pokemon(self.p1_ativo)}")
            print("\n" + "   " * 35 + "\n") # Espaçamento maior entre P1 e P2
            print(f"💥 ADVERSÁRIO (P2):\n{self.formatar_pokemon(self.p2_ativo)}")
        else:
            print(f"🏆 PLACAR JOGADOR 2: {self.p2_pontos} ponto(s)")
            print(f"⭐ MEU CAMPO (P2):\n{self.formatar_pokemon(self.p2_ativo)}")
            print("\n" + "   " * 35 + "\n") # Espaçamento maior entre P2 e P1
            print(f"💥 ADVERSÁRIO (P1):\n{self.formatar_pokemon(self.p1_ativo)}")
            
        print("\n" + "═"*108)