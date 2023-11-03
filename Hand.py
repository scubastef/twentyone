

class PlayerHand:

    def __init__(self, initial_bet: float) -> None:
        self._card1 = None
        self._card2 = None

        self._num_cards = 0
        self._num_soft_aces = 0
        self._hand_sum = 0


        self._initial_bet = initial_bet
    
    def soft_ace_exits(self):
        return self._num_soft_aces > 0

    def get_card1(self):
        return self._card1
    
    def set_card1(self, card : int):
        self._num_cards += 1
        self._card1 = card
    
    def get_card2(self):
        return self._card2
    
    def set_card2(self, card : int):
        self._num_cards += 1
        self._card2 = card

    def get_initial_bet(self):
        return self._initial_bet

    def set_initial_bet(self, amount : int):
        self._initial_bet = amount
    
    def adjust_initial_bet(self, amount : float):
        self._initial_bet += amount
    
    def is_blackjack(self) -> bool:
        return self._card1 + self._card2 == 21
    
    def update_hand(self, new_card : int):
        self._num_cards += 1
        self._num_soft_aces += (new_card == 11)
        self._hand_sum += new_card

        while self._hand_sum > 21 and self._num_soft_aces > 0:
            self._hand_sum -= 10
            self._num_soft_aces -= 1

    def get_hand_sum(self):
        return self._hand_sum
    
    def is_initial(self):
        return self._num_cards == 2
    
    def is_busted(self):
        return self._hand_sum > 21 and self._num_soft_aces==0

    def set_initial_cards(self, card1 : int, card2 : int):
        self._card1 = card1
        self._card2 = card2

    def is_aces_pair(self):
        return self._card1 + self._card2 == 22
    
    def is_pair(self):
        assert self._card1 is not None or self._card2 is not None, 'cards cant be None'
        return (self._card1 == self._card2) and self._num_cards == 2
    
    def initalize_cards(self, card1 : int, card2 : int):
        self._card1 = card1
        self._card2 = card2
        self._num_cards = 2
        self._hand_sum = card1 + card2
        self._num_soft_aces = (card1==11 + card2==11)

    def manually_convert_one_hard_to_soft(self):
        '''FOR EXTREMLY RARE CASES'''
        while self._hand_sum > 21 and self._num_soft_aces > 0:
            self._hand_sum -= 10
            self._num_soft_aces -= 1








class DealerHand:

    def __init__(self, up_card : int, down_card : int) -> None:
        self._up_card = up_card
        self._down_card = down_card

        self._is_up_card_ace = up_card == 11
        self._is_sum_twentyone = (up_card + down_card) == 21

        self._num_soft_aces = up_card == 11 + down_card == 11
        self._hand_sum = up_card + down_card

    def get_is_up_card_ace(self):
        return self._is_up_card_ace
    
    def get_is_up_card_ten(self):
        return self._up_card == 10
    
    def get_is_sum_twentyone(self):
        return self._is_sum_twentyone
    
    def get_upcard(self):
        return self._up_card
    
    def update_hand(self, card : int):
        self._num_soft_aces += (card == 11)
        self._hand_sum += card

        while self._hand_sum > 21 and self._num_soft_aces > 0:
            self._hand_sum -= 10
            self._num_soft_aces -= 1
    
    def exists_soft_ace(self):
        return self._num_soft_aces > 0

    def get_hand_sum(self):
        return self._hand_sum
    
    def get_num_soft_aces(self):
        return self._num_soft_aces


    