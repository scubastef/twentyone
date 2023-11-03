from Table import Table
from Player import Player, Dealer
from Enums import Action, DealerStrategy
from Shoe import Shoe
from Strategy import PlayerStrategy
from Hand import PlayerHand, DealerHand

class Game:

    def __init__(self, table : Table) -> None:
        self._table = table
        self._players = table.get_player_list()
        self._dealer = table.get_dealer()
        self._shoe = table.get_shoe()


    
    def _initial_deal(self):

        temp = [self._shoe.draw() for _ in range((len(self._players) + 1) * 2)]

        for i, player in enumerate(self._players):
            player.get_hand().initalize_cards(temp[i], temp[i + len(self._players)])

        dealer.set_hand(temp[-1], temp[-2])


    def _player_playout(self, player : Player, hand : PlayerHand) :
        
        # get the action
        action = player.get_action(hand, self._dealer.get_hand())

        if action==Action.SPLIT:
            player.increment_num_splits()

            if hand.is_aces_pair():
                hand1 = PlayerHand(hand.get_initial_bet())
                hand1.set_initial_cards(hand.get_card1(), self._shoe.draw())
                player.adjust_bankroll(-hand.get_initial_bet())

                hand2 = PlayerHand(hand.get_initial_bet())
                hand2.set_initial_cards(hand.get_card2(), self._shoe.draw())
                player.adjust_bankroll(-hand.get_initial_bet())

                player.add_active_hand(hand1)
                player.add_active_hand(hand2)
                return

            hand1 = PlayerHand(hand.get_initial_bet())
            player.adjust_bankroll(-hand1.get_initial_bet())
            hand1.initalize_cards(hand.get_card1(), self._shoe.draw())
            self._player_playout(player, hand1)

            hand2 = PlayerHand(hand.get_initial_bet())
            player.adjust_bankroll(-hand2.get_initial_bet())
            hand2.initalize_cards(hand.get_card2(), self._shoe.draw())
            self._player_playout(player, hand2)

        if action == Action.DD:
            hand.adjust_initial_bet(hand.get_initial_bet())
            player.adjust_bankroll(-hand.get_initial_bet())
            hand.update_hand(self._shoe.draw())
            player.add_active_hand(hand)
            return
        
        if action == Action.HIT :
            hand.update_hand(self._shoe.draw())
            self._player_playout(player, hand)

        if action == Action.STAND :
            player.add_active_hand(hand)
            return
        



    def _dealer_playout(self):

        if self._dealer.get_dealer_strategy() == DealerStrategy.HS17:

            while self._dealer.get_hand().get_hand_sum() <= 17:
                if not self._dealer.get_hand().exists_soft_ace() and self._dealer.get_hand().get_hand_sum() == 17:
                    break
                else:
                    self._dealer.get_hand().update_hand(self._shoe.draw())
        
        if self._dealer.get_dealer_strategy() == DealerStrategy.SS17:

            while self._dealer.get_hand().get_hand_sum() < 17:
                self._dealer.get_hand().update_hand(self._shoe.draw())

    
    def _execute_cashflows(self):

        for player in self._players:
            if not player.get_activity_status(): 
                continue

            for hand in player.get_active_hands():
                if self._dealer.is_busted():   
                    player.adjust_bankroll(2  * hand.get_initial_bet() * (not hand.is_busted()))
                else:
                    hand_win = hand.get_hand_sum() > self._dealer.get_hand().get_hand_sum()
                    hand_tie = hand.get_hand_sum() == self._dealer.get_hand().get_hand_sum()
                    cashflow = (2 * hand.get_initial_bet() * hand_win) + (hand.get_initial_bet() * hand_tie)
                    player.adjust_bankroll(cashflow)

        print('New Bankroll ' + str(self._players[0].get_bankroll()))


    
    def _table_plays_one_hand(self):

        # initialize a hand by placing a bet on it
        for player in self._players:
            player.place_bet()

        # initial deal
        self._initial_deal()

        # SPECIAL CASE 1: dealer up card is ace; offer insurance or even money (if applicable)
        if self._dealer.upcard_is_ace():
            insurance_taken = [False for player in self._players] #TODO
            em_taken = [False for player in self._players] #TODO

            # dealer checks for 21
            for i, player in enumerate(self._players):
                # deal with insurance
                payoff = self._dealer.sum_is_twentyone() * insurance_taken[i] * player.get_hand().get_initial_bet()
                player.adjust_bankroll(payoff)

                # deal with even money
                player.adjust_bankroll(em_taken[i] * 2 * player.get_hand().get_initial_bet())
                player.set_activity_status(not em_taken[i])

            if self._dealer.sum_is_twentyone(): 
                for player in self._players:
                    player.reset_hands()
                return
        
        # SPECIAL CASE 2: dealer up card is value 10, check for 21
        if self._dealer.upcard_is_ten() and self._dealer.sum_is_twentyone():
            for player in self._players:
                payoff = player.get_hand().is_blackjack() * player.get_hand().get_initial_bet()
                player.adjust_bankroll(payoff)
                player.reset_hands()
            return
        
        # SPECIAL CASE 3: player has blackjack TODO
        for player in self._players:
            if player.get_hand().is_blackjack():
                payoff = player.get_hand().get_initial_bet() + (1.5 * player.get_hand().get_initial_bet())
                player.adjust_bankroll(payoff)
                player.set_activity_status(False)

        

        # each player plays out
        for player in self._players:
            self._player_playout(player, player.get_hand())

        # dealer plays out
        self._dealer_playout()

        # disperse winnings/losses depeing on outcome
        self._execute_cashflows()

        # clear hands
        for player in self._players:
            player.reset_hands()



    def start_game_simulations(self, num_hands : int):
        n = 0
        while n < num_hands:
            self._table_plays_one_hand()
            if self._shoe.get_cut_card_seen(): self._shoe.shuffle()
            n += 1
        return self._players[0].get_bankroll()

    

if __name__ == '__main__':
    shoe = Shoe()
    dealer = Dealer(dealer_strategy=DealerStrategy.HS17)
    player = Player(strategy=PlayerStrategy('Strategies/BasicStrategy'), bankroll=100)
    table = Table([player], dealer, shoe, 1, 100)
    game = Game(table)
    results = [game.start_game_simulations(20) for _ in range(100)]
    print(results)
    print(sum(results) / 100)