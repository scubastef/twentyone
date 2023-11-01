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


    
    def _initial_deal(self, bets):

        temp = [self._shoe.draw() for _ in range((len(self._players) + 1) * 2)]

        for i, player in enumerate(self._players):
            player.set_hand(PlayerHand(temp[i], temp[i+len(self._players)], bets[i]))
            player.adjust_bankroll(-bets[i])

        dealer.set_hand(temp[-1], temp[-2])

        print('Player Hand: ' + str(self._players[0].get_hand().get_card1()) + ','
              + str(self._players[0].get_hand().get_card2()))
        
        print("Dealer Hand: up card: " + str(dealer.get_hand().get_upcard()))


    def _player_playout(self, player : Player, hand : PlayerHand) :
        
        # get the action
        action = player.get_action(hand, self._dealer.get_hand())
        print('Action ' + str(action))

        if action==Action.SPLIT:
            if hand.get_card1() == 11 and hand.get_card2() == 11:
                player.increment_num_splits()
                hand1 = PlayerHand(hand.get_card1(), self._table.get_shoe().draw(), hand.get_initial_bet())
                hand2 = PlayerHand(hand.get_card2(), self._table.get_shoe().draw(), hand.get_initial_bet())
                hand1.update_hand(0)
                hand2.update_hand(0)
                player.add_active_hand(hand1)
                player.add_active_hand(hand2)
                return

            player.increment_num_splits()
            hand1 = PlayerHand(hand.get_card1(), self._table.get_shoe().draw(), hand.get_initial_bet())
            self._player_playout(player, hand1)
            hand2 = PlayerHand(hand.get_card2(), self._table.get_shoe().draw(), hand.get_initial_bet())
            self._player_playout(player, hand2)

        if action == Action.DD:
            hand.adjust_initial_bet(hand.get_initial_bet())
            hand.update_hand(self._table.get_shoe().draw())
            player.add_active_hand(hand)
            print(player.get_hand().get_hand_sum()) #
            return
        
        if action == Action.HIT :
            # draw a card
            hand.update_hand(self._table.get_shoe().draw())
            self._player_playout(player, hand)

        if action == Action.STAND :
            player.add_active_hand(hand)
            print(player.get_hand().get_hand_sum()) #
            return
        



    def _dealer_playout(self):

        if self._dealer.get_dealer_strategy() == DealerStrategy.HS17:

            while self._dealer.get_hand().get_hand_sum() <= 17:
                if ~self._dealer.get_hand().exists_soft_ace() and self._dealer.get_hand().get_hand_sum() == 17:
                    break
                else:
                    self._dealer.get_hand().update_hand(self._shoe.draw())
        
        if self._dealer.get_dealer_strategy() == DealerStrategy.SS17:

            while self._dealer.get_hand().get_hand_sum() < 17:
                self._dealer.get_hand().update_hand(self._shoe.draw())

    
    def _execute_cashflows(self):

        for player in self._players:
            for hand in player.get_active_hands():
                if self._dealer.is_busted():   
                    player.adjust_bankroll(hand.is_busted() * 2 * hand.get_initial_bet())
                else:
                    hand_win = hand.get_hand_sum() > self._dealer.get_hand().get_hand_sum()
                    hand_tie = hand.get_hand_sum() == self._dealer.get_hand().get_hand_sum()
                    cashflow = (2 * hand.get_initial_bet() * hand_win) + (hand.get_initial_bet() * hand_tie)
                    player.adjust_bankroll(cashflow)

        print('New Bankroll ' + str(self._players[0].get_bankroll()))





    
    def _table_plays_one_hand(self):

        # get bets
        bets = [player.get_bet() for player in self._players]

        # initial deal
        self._initial_deal(bets)

        # SPECIAL CASE 1: dealer up card is ace; offer insurance or even  money
        if self._dealer.upcard_is_ace():
            insurance_taken = [False for player in self._players] #TODO
            even_money_taken = [False for player in self._players] #TODO

            # dealer checks for 21
            for player, took_insurance, took_em in zip(self._players, insurance_taken, even_money_taken):
                assert not took_insurance and not took_em, 'cant take insurance and even money'

                # deal with insurance
                bool1 = ~took_insurance and self._dealer.sum_is_twentyone()
                bool2 = took_insurance and ~self._dealer.sum_is_twentyone()
                insurance_payoff = -player.get_hand().get_initial_bet() * (bool1 + self._table.get_insurance_rate() * bool2)
                player.adjust_bankroll(insurance_payoff)

                # deal with even money
                player.adjust_bankroll(took_em * 2 *  player.get_hand().get_initial_bet())
                player.set_activity_status(not took_em)

            if self._dealer.sum_is_twentyone(): 
                for player in self._players:
                    player.set_activity_status(True)
                return
        
        # SPECIAL CASE 2: dealer up card is value 10, check for 21
        if self._dealer.upcard_is_ten() and self._dealer.sum_is_twentyone():
            for player in self._players:
                payoff = (1 - player.get_hand().get_is_blackjack()) * -player.get_hand().get_initial_bet()
                player.adjust_bankroll(payoff)
            return

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

    

if __name__ == '__main__':
    shoe = Shoe()
    dealer = Dealer(dealer_strategy=DealerStrategy.HS17)
    player = Player(strategy=PlayerStrategy('Strategies/BasicStrategy'), bankroll=5000)
    table = Table([player], dealer, shoe, 1, 100)
    game = Game(table)
    game.start_game_simulations(100)