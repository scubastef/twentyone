from enum import Enum
from Shoe import Shoe
from Hand import DealerHand, PlayerHand
from Strategy import PlayerStrategy
from Enums import DealerStrategy, Action

class Player:


    def __init__(self, strategy : PlayerStrategy, bankroll : int) -> None:
        self._strategy = strategy
        self._initial_hand = None
        self._active_hands = []
        self._bankroll = bankroll
        self._activity_status = True
        self._num_splits = 0

    def get_activity_status(self):
        return self._activity_status

    def get_active_hands(self) -> list[PlayerHand]:
        return self._active_hands

    def add_active_hand(self, hand : PlayerHand):
        self._active_hands.append(hand)

    def get_action(self, player_hand : PlayerHand, dealer_hand : DealerHand):
        if player_hand.is_busted(): 
            return Action.STAND
        
        player_sum, dealer_card = player_hand.get_hand_sum(), dealer_hand.get_upcard()
        print(player_sum, dealer_card)

        can_split = self._num_splits < 4 and player_hand.is_pair() #TODO: get rid of magic number
        initial = player_hand.is_initial()


        ###### an extremly rare case ######
        if player_hand.is_aces_pair() and ~can_split: 
            player_hand.manually_convert_one_hard_to_soft()
        ###### an extremly rare case ######

        if can_split: 
            action = self._strategy.get_pair_splitting_table().loc[player_sum, dealer_card]
        elif player_hand.soft_ace_exits() and initial:
            action = self._strategy.get_soft_totals_init_table().loc[player_sum, dealer_card]
        elif player_hand.soft_ace_exits() and not initial:
            action = self._strategy.get_soft_totals_post_table().loc[player_sum, dealer_card]
        else:
            action = self._strategy.get_hard_totals_table().loc[player_sum, dealer_card]
        
        return action

    def set_hand(self, hand : PlayerHand):
        self._hand = hand

    def set_hand_cards(self, card1 : int, card2 : int):
        assert self._hand is not None, 'HAND IS NONE!!!!!!!'
        self._hand.set_card1(card1)
        self._hand.set_card2(card2)
    
    def get_hand(self):
        return self._initial_hand

    def adjust_bankroll(self, amount : float):
        self._bankroll += amount

    def take_insurance(self):
        None #TODO:

    def set_activity_status(self, status : bool):
        self._activity_status = status

    def get_num_splits(self):
        return self._num_splits
    
    def increment_num_splits(self):
        self._num_splits += 1

    def get_bankroll(self):
        return self._bankroll
    
    def reset_hands(self):
        self._initial_hand = None
        self._active_hands = []
        self._activity_status = True
        self._num_splits = 0

    def place_bet(self):
        assert self._initial_hand is None, 'Can only place a bet before the dealer deals the cards'
        self._initial_hand = PlayerHand(5) # TODO: use a startegy
        self._bankroll -= 5 # TODO make sure to update

    def initialize_initial_hand_cards(self, card1 : int, card2 : int):
        assert self._hand is not None, 'Can only assign cards after a bet has been made'
        self._initial_hand.set_initial_cards(card1, card2)
        
        

class Dealer:
    def __init__(self, dealer_strategy : DealerStrategy) -> None:
        self._hand = None 
        self._strategy = dealer_strategy

    def get_dealer_strategy(self):
        return self._strategy

    def get_hand(self):
        return self._hand
    
    def set_hand(self, up_card : int, down_card : int):
        self._hand = DealerHand(up_card, down_card)

    def upcard_is_ace(self):
        return self._hand.get_is_up_card_ace()
    
    def upcard_is_ten(self):
        return self._hand.get_is_up_card_ten()
    
    def sum_is_twentyone(self):
        return self._hand.get_is_sum_twentyone()
    
    def is_busted(self):
        return self._hand.get_hand_sum()  > 21