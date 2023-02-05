from typing import List

from twenty_one import Game, Player



MAX_NUMBER_OF_PLAYERS = 6
PLAYER_CAPITAL = 1000

if __name__ == "__main__":
    
    # sign-up players
    players: List[Player] = []
    for _ in range(0, MAX_NUMBER_OF_PLAYERS):
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

    # initiate the game
    game = Game(p_players=players)
    game.phase_1__start()

    # place the bets
    for player in game.players:
        bet_amount_str = input(f"Enter an integer bet amount less than or equal to {PLAYER_CAPITAL} for {player.name}: ")
        bet_amount = int(bet_amount_str)
        game.phase_2__place_bet(player, bet_amount)

    # pass second cards
    game.phase_3__give_players_the_second_card()

    # ask actions one by one
    while ....
        

