import random

ACE = 150
DECK_SIZE = 52


class Shoe:

    def __init__(self, num_decks=6, max_cut_percentage=0.3, min_cut_percentage=0.1) -> None:
        self._max_cut_percentage = max_cut_percentage
        self._min_cut_percentage = min_cut_percentage
        self._num_decks = num_decks
        self._pos_current_card = 0
        self._cut_card_seen = False
        self._raw_count = 0
        
        self._cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4 * num_decks
        self.shuffle()
        self._pos_cut_card = None
        self._set_cut_card_position()
        print(self._pos_cut_card)

    def _set_cut_card_position(self):
        self._pos_cut_card = self._num_decks * DECK_SIZE - int(self._num_decks * DECK_SIZE * 
                                 random.uniform(self._min_cut_percentage, self._max_cut_percentage))


    def shuffle(self):
        random.shuffle(self._cards)
        self._cut_card_seen = False
        self._set_cut_card_position()
        self._raw_count = 0
        self._pos_current_card = 0

    def draw(self) -> int:
        card = self._cards[self._pos_current_card]
        self._pos_current_card += 1

        self._cut_card_seen = self._pos_current_card > self._pos_cut_card 
        #print(self._pos_current_card, self._pos_cut_card)

        self._raw_count += (card < 7) - (card > 9)

        return card
    
    ## get and set methods
    def get_num_decks(self):
        return self._num_decks
    
    def get_pos_cut_card(self):
        return self._pos_cut_card
    
    def get_pos_current_card(self):
        return self._pos_current_card
    
    def get_cut_card_seen(self):
        return self._cut_card_seen

    def get_raw_count(self):
        return self._raw_count
    
    def get_true_count(self):
        return round(self._raw_count / (len(self._cards) - self._pos_current_card + 1))
    



