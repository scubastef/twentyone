from Player import Player, Dealer
from Shoe import Shoe
from Hand import PlayerHand, DealerHand


class Table:

    def __init__(self, players_list : list[Player], dealer : Dealer, shoe : Shoe, table_min : int, table_max : int) -> None:
        self._shoe = shoe
        self._players_list = players_list
        self._dealer = dealer

        self._insurance_rate = 0.5

    def get_shoe(self):
        return self._shoe
    
    def get_num_players(self):
        return len(self._players_list)

    def get_dealer(self):
        return self._dealer
        
    def get_player_list(self):
        return self._players_list
    
    def get_insurance_rate(self):
        return self._insurance_rate
    
        