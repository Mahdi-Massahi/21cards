import unittest

from twenty_one import Game, States, Action, Player
from cards import Symbols


class TestGameSinglePlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.player_initial_capital = 1000
        self.player = Player(p_name="Player", p_capital=self.player_initial_capital)
        self.game = Game(p_players=[self.player])

    def test_case_01(self):
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital

        cards_symbols = [Symbols.TEN, Symbols.THREE, Symbols.FOUR, Symbols.THREE, Symbols.QUEEN, Symbols.NINE, Symbols.FIVE]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)
        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertEqual(self.game.players[0].capital, self.player_initial_capital + bet_amount)


    def test_case_02(self):
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital
        
        cards_symbols = [Symbols.TEN, Symbols.THREE, Symbols.FIVE, Symbols.KING, Symbols.NINE, Symbols.EIGHT]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)
        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertEqual(self.game.players[0].capital, self.player_initial_capital - bet_amount)


    def test_case_03(self):
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital
        
        cards_symbols = [Symbols.NINE, Symbols.EIGHT, Symbols.TEN, Symbols.JACK, Symbols.TEN]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)
        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertEqual(self.game.players[0].capital, self.player_initial_capital - bet_amount)


    def test_case_04(self):
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital
        
        cards_symbols = [Symbols.NINE, Symbols.SEVEN, Symbols.THREE, Symbols.TWO, Symbols.EIGHT, Symbols.SEVEN]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)

        self.assertCountEqual(self.game.players[0].sets[0].state, States.BUST)

        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertEqual(self.game.players[0].capital, self.player_initial_capital - bet_amount)


    def test_case_05(self):
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital
        
        cards_symbols = [Symbols.ACE, Symbols.TEN, Symbols.FOUR, Symbols.SIX, Symbols.SIX, Symbols.SEVEN]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)
        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertCountEqual(self.game.bank.sets[0].state, States.BUST)

        self.assertEqual(self.game.players[0].capital, self.player_initial_capital + bet_amount)



if __name__ == '__main__':
    unittest.main()