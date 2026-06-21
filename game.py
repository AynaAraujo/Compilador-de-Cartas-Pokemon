# game.py
from collections import Counter

class DeckError(Exception):
    pass

class DeckSizeError(DeckError):
    pass

class DuplicateCardError(DeckError):
    pass

class InvalidCardError(DeckError):
    pass


class JogoEstado:
    def __init__(self, db_cartas):
        self.db = db_cartas
        self.p1_name = "Jogador1"
        self.p2_name = "Jogador2"
        self.p1_pontos = 0
        self.p2_pontos = 0
        self.p1_banco = []
        self.p2_banco = []
        self.p1_ativo = None
        self.p2_ativo = None

    def carregar_deck(self, lista_nomes):
        if len(lista_nomes) != 5:
            raise DeckSizeError(
                f"❌ Erro Semântico: Cada deck deve conter exatamente 5 cartas. Foram encontradas {len(lista_nomes)} carta(s)."
            )

        repetidas = [nome for nome, count in Counter(lista_nomes).items() if count > 1]
        if repetidas:
            raise DuplicateCardError(
                f"❌ Erro Semântico: O deck contém cartas repetidas: {', '.join(repetidas)}."
            )

        deck_instanciado = []
        for nome in lista_nomes:
            nome = nome.strip()
            if nome not in self.db:
                cartas_validas = ", ".join(sorted(self.db))
                raise InvalidCardError(
                    f"❌ Erro Semântico: A carta '{nome}' não existe no banco de dados."
                    f" Cartas válidas: {cartas_validas}"
                )

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
        if not p:
            return "NENHUM POKÉMON EM CAMPO (NOCAUTEADO)"

        ataques_formatados = []
        for a in p['attacks']:
            custo = a.get('cost', 0)
            ataques_formatados.append(f"• {a['name']} [Dano: {a['damage']} | Custo: {custo} eng]")
        txt_ataques = "   ".join(ataques_formatados)

        fraqueza = f"{p['weaknesses'][0]['type']} ({p['weaknesses'][0]['value']})" if p['weaknesses'] else "Nenhuma"
        resistencia = f"{p['resistances'][0]['type']} ({p['resistances'][0]['value']})" if p['resistances'] else "Nenhuma"

        return (
            f"🟢 {p['name']}\n"
            f"   [ HP: {p['hp_atual']}/{p['hp']}  |  TIPO: {p['types']}  |  ENERGIAS LIGADAS: {p['energias_total']} ]\n"
            f"   [ FRAQUEZA: {fraqueza}  |  RESISTÊNCIA: {resistencia} ]\n"
            f"   └─ ATAQUES: {txt_ataques}"
        )

    def mostrar_painel(self, jogador_da_vez):
        print("\n" + "🐾 " * 15 + " STATUS DA ARENA DE BATALHA " + "🐾 " * 15 + "\n")

        if jogador_da_vez == self.p1_name:
            print(f"🏆 PLACAR {self.p1_name}: {self.p1_pontos} ponto(s)")
            print(f"⭐ MEU CAMPO ({self.p1_name}):\n{self.formatar_pokemon(self.p1_ativo)}")
            print("\n" + "   " * 35 + "\n")
            print(f"💥 ADVERSÁRIO ({self.p2_name}):\n{self.formatar_pokemon(self.p2_ativo)}")
        else:
            print(f"🏆 PLACAR {self.p2_name}: {self.p2_pontos} ponto(s)")
            print(f"⭐ MEU CAMPO ({self.p2_name}):\n{self.formatar_pokemon(self.p2_ativo)}")
            print("\n" + "   " * 35 + "\n")
            print(f"💥 ADVERSÁRIO ({self.p1_name}):\n{self.formatar_pokemon(self.p1_ativo)}")

        print("\n" + "═"*108)