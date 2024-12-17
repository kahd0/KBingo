import random
import json
from utils.database import saveCards, getLastCardNumber, isCardUnique
from utils.logging import logInfo, logError

class GenerateCardsController:
    def __init__(self, bingo_id, num_cartelas):
        self.bingo_id = bingo_id
        self.num_cartelas = num_cartelas



    def generateCards(self):
        """Gera cartelas únicas, verificando no banco."""
        cards = set()
        last_card, last_lote = getLastCardNumber(self.bingo_id)

        new_lote = last_lote + 1 if last_lote else 1
        new_card_number = last_card + 1 if last_card else 1

        while len(cards) < self.num_cartelas:
            card = self.generateSingleCard()
            if tuple(card) not in cards and isCardUnique(self.bingo_id, card):  # Correção aqui
                cards.add(tuple(card))
                yield {
                    "numero_cartela": f"{new_card_number:04d}-{new_lote:02d}",
                    "numeros": json.dumps(card),
                    "lote": new_lote
                }
                new_card_number += 1


    def generateSingleCard(self):
        """Gera uma única cartela 5x5 respeitando os intervalos."""
        card = []
        intervals = [(0, 19), (20, 39), (40, 59), (60, 79), (80, 99)]
        for interval in intervals:
            column = random.sample(range(interval[0], interval[1] + 1), 5)
            card.extend(column)
        return card

    def saveGeneratedCards(self):
        """Salva as cartelas geradas no banco de dados."""
        try:
            generated_cards = list(self.generateCards())
            saveCards(self.bingo_id, generated_cards)
            logInfo(f"{len(generated_cards)} cartelas geradas com sucesso.")
            return generated_cards
        except Exception as e:
            logError(f"Erro ao gerar cartelas: {e}")
            return []
