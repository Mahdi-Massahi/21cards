from typing import List
from random import randint, seed

from twenty_one import Game, Player, States, Action


PLAYER_CAPITAL = 1000

if __name__ == "__main__":
    random_seed = randint(1, 99999)
    print("seed:", random_seed)
    seed(random_seed)
    
    # sign-up players
    players: List[Player] = []
    while True:
        player_name = input("Enter a name to create a player: ")
        player = Player(
            p_capital=PLAYER_CAPITAL,
            p_name=player_name, 
            )
        players.append(player)

        command = input("Enter N/n to add a new player, and S/s to start playing: ")
        # TODO: safe string comperison
        if str.lower(command) == 's':
            break

    while True:
        # initiate the game
        game = Game(p_players=players)
        game.phase_1__start()

        # place the bets
        if player.capital > 0:
            for player in game.players:
                bet_amount_str = input(f"Enter an integer bet amount less than or equal to {player.capital} for {player.name}: ")
                bet_amount = int(bet_amount_str)  # TODO: safe checking
                if bet_amount > player.capital:
                    print("You cannot bet greater than your capital.")
                    exit()  # TODO: better to let the user re enter a true value
                else:
                    game.phase_2__place_bet(player, bet_amount)
        else:
            print("You do not have enough capital.")
            exit()

        # pass second cards
        game.phase_3__give_players_the_second_card()

        # ask actions player by player and set by set
        while not game.check_if_all_players_are_ready():
            for player in game.players:
                for set in player.sets:
                    if set.state is States.OPEN_TO_HIT:
                        msg_ask_action = f"It's {player.name}'s turn; enter H/h to hit, S/s to stand and P/p to split: "
                        action = str.lower(input(msg_ask_action))
                        while action not in ['h', 's', 'p']:
                            print("Invalid action, try again.")
                            action = str.lower(input(msg_ask_action))
                        if action == 'h':
                            game.phase_4__take_action_for_player(player, Action.HIT)
                        elif action == 's':
                            game.phase_4__take_action_for_player(player, Action.STAND)
                        elif action == 'p':
                            game.phase_4__take_action_for_player(player, Action.SPLIT)
        
        # other actions by bank
        game.phase_5__reveals_banks_second_card()
        game.phase_6__bank_hits_until_bust_or_stand()

        # play again?
        do_play_again = str.lower(input("Enter Y/y to play again, any other key to stop: "))
        if do_play_again != 'y':
            break

        game.reset()

            

