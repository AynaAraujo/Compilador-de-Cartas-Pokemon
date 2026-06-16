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
