# import random

# num_splits = 0
# def play_out(hand : list):
#         #print(f'origian hand {hand}')
#     	# if there is just one card draw the second
#         if hand[1] is None: hand[1] = 1 + int(10 * random.uniform(0.7,1))
#         print(hand)

#         # get the action 
#         action = 'split' if hand[0] == hand[1] else 'stay'

#         # if action is split and number of splits is <= 3
#         if action=='split':
#             hand1 = [hand[0], None]
#             play_out(hand1)
#             hand2 = [hand[1], None]
#             play_out(hand2)
        
#         if action == 'dd':
#             hand.adjust_inital_bet()
#             player.update_hand(draw())
#             return
        
#         if action is hit
#             # draw a card
#             player.update_hand(draw())
#             return

#         # if action is stay
#             return

#         if action=='stay':
#             return
        

# def dealer_play_out(hand : list):
#       None

# if __name__ == '__main__':
#       play_out([8,8])