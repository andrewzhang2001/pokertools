import random

class Deck:

    def __init__(self):
        self.undealt_cards = []
        self.dealt_cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                self.undealt_cards.append(Card(rank, suit))
        
    def contains_card(self, card: str) -> bool:
        rank = card[0]
        suit = card[1]
        if rank not in Card.ranks or suit not in Card.suits:
            return False
        temp_card = Card(rank, suit)
        return temp_card in self.undealt_cards

        

    def deal(self, num_cards: int) -> list:
        """Randomly deal a certain number of cards. Returns a list of cards dealt"""
        assert num_cards <= len(self.undealt_cards)
        returned_cards = []
        for _ in range(num_cards):
            random_index = random.randint(0, len(self.undealt_cards) - 1)
            temp_card = self.undealt_cards[random_index]
            self.undealt_cards[random_index] = self.undealt_cards[-1]
            self.undealt_cards[-1] = temp_card
            dealt_card = self.undealt_cards.pop()
            returned_cards.append(dealt_card)
            self.dealt_cards.append(dealt_card)
    
    
    def undeal(self, num_cards: int) -> None:
        """Undeals the most recently dealt cards of the deck."""
        assert num_cards <= len(self.dealt_cards)
        for _ in range(num_cards):
            self.undealt_cards.append(self.dealt_cards.pop())

    def deal_flop(self, flop_string: str) -> bool:
        flop_cards = flop_string.split()
        if len(flop_cards) == 1:
            assert len(flop_cards[0] == 6)
            flop_cards = [flop_cards[0][:2], flop_cards[0][2:4], flop_cards[0][4:6]]
        else:
            assert len(flop_cards) == 3
        for card in flop_cards:
            if not self.contains_card(card):
                return False
        



class Card:

    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    suits = ['c', 'd', 'h', 's']
    suits_symbol_map = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}

    def __init__(self, rank:str, suit:str):
        assert rank in Card.ranks and suit in Card.suits
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.rank + self.suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __ne__(self, other):
        return not self.__eq__(other)

c = Card('8','s')
print(c)

d = Deck()
print(d.undealt_cards)
print(d.dealt_cards)
d.deal(10)
print(d.dealt_cards)
print(d.undealt_cards)
d.undeal(5)
print(d.dealt_cards)
print(d.undealt_cards)
d.undeal(5)
print(d.dealt_cards)
print(d.undealt_cards)
# Should AssertionError
d.undeal(5)
print(d.dealt_cards)
print(d.undealt_cards)
