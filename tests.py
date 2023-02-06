import unittest

from twenty_one import Game, States, Action, Player
from cards import Symbols


class TestGameSinglePlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.player_initial_capital = 1000
        self.player = Player(p_name="Player", p_capital=self.player_initial_capital)
        self.game = Game(p_players=[self.player])

    def test_case_01(self):
        """
        Player win
        """
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital

        cards_symbols = [
            Symbols.TEN,
            Symbols.THREE,
            Symbols.FOUR,
            Symbols.THREE,
            Symbols.QUEEN,
            Symbols.NINE,
            Symbols.FIVE,
        ]
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

        self.assertEqual(
            self.game.players[0].capital, self.player_initial_capital + bet_amount
        )

    def test_case_02(self):
        """
        Bank win
        """
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital

        cards_symbols = [
            Symbols.TEN,
            Symbols.THREE,
            Symbols.FIVE,
            Symbols.KING,
            Symbols.NINE,
            Symbols.EIGHT,
        ]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)
        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertEqual(
            self.game.players[0].capital, self.player_initial_capital - bet_amount
        )

    def test_case_03(self):
        """
        Equal points for player and bank, bank win
        """
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital

        cards_symbols = [
            Symbols.NINE,
            Symbols.EIGHT,
            Symbols.TEN,
            Symbols.JACK,
            Symbols.TEN,
        ]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)
        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertEqual(
            self.game.players[0].capital, self.player_initial_capital - bet_amount
        )

    def test_case_04(self):
        """
        single user bust, bank win
        """
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital

        cards_symbols = [
            Symbols.NINE,
            Symbols.SEVEN,
            Symbols.THREE,
            Symbols.TWO,
            Symbols.EIGHT,
            Symbols.SEVEN,
        ]
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

        self.assertEqual(
            self.game.players[0].capital, self.player_initial_capital - bet_amount
        )

    def test_case_05(self):
        """
        bank bust
        """
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital

        cards_symbols = [
            Symbols.ACE,
            Symbols.TEN,
            Symbols.FOUR,
            Symbols.SIX,
            Symbols.SIX,
            Symbols.SEVEN,
        ]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)
        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertCountEqual(self.game.bank.sets[0].state, States.BUST)
        self.assertEqual(
            self.game.players[0].capital, self.player_initial_capital + bet_amount
        )

    def test_case_06(self):
        """
        Spliting when bank bust, player's one set wins and the other set loses
        """
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital

        cards_symbols = [
            Symbols.SEVEN,
            Symbols.SIX,
            Symbols.SEVEN,
            Symbols.FIVE,
            Symbols.NINE,
            Symbols.TEN,
            Symbols.EIGHT,
            Symbols.NINE,
            Symbols.EIGHT,
        ]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()

        self.game.phase_4__take_action_for_player(self.player, Action.SPLIT)
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)

        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)

        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertCountEqual(self.game.players[0].sets[1].state, States.BUST)
        self.assertCountEqual(self.game.bank.sets[0].state, States.BUST)
        self.assertEqual(self.game.players[0].capital, self.player_initial_capital)

    def test_case_07(self):
        """
        Two splits in a row
        """
        self.game.reset()
        self.game.players[0].capital = self.player_initial_capital

        cards_symbols = [
            Symbols.ACE,
            Symbols.TWO,
            Symbols.ACE,
            Symbols.ACE,
            Symbols.NINE,
            Symbols.SIX,
            Symbols.TEN,
            Symbols.EIGHT,
            Symbols.TEN,
            Symbols.NINE,
            Symbols.TEN,
        ]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 200
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player, bet_amount)
        self.game.phase_3__give_players_the_second_card()

        self.game.phase_4__take_action_for_player(self.player, Action.SPLIT)
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.SPLIT)
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)

        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.HIT)

        self.game.phase_4__take_action_for_player(self.player, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player, Action.STAND)

        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertCountEqual(self.game.players[0].sets[1].state, States.BUST)
        self.assertEqual(
            self.game.players[0].capital, self.player_initial_capital - 3 * bet_amount
        )

    def test_case_08(self):
        """
        Multiplayer
        """
        self.players_initial_capital = 1000
        self.player_1 = Player(
            p_name="Player I", p_capital=self.players_initial_capital
        )
        self.player_2 = Player(
            p_name="Player II", p_capital=self.players_initial_capital
        )
        self.player_3 = Player(
            p_name="Player III", p_capital=self.players_initial_capital
        )
        self.game = Game(p_players=[self.player_1, self.player_2, self.player_3])

        cards_symbols = [
            Symbols.SEVEN,
            Symbols.QUEEN,
            Symbols.ACE,
            Symbols.TEN,
            Symbols.ACE,
            Symbols.NINE,
            Symbols.ACE,
            Symbols.NINE,
            Symbols.TWO,
            Symbols.FIVE,
            Symbols.FOUR,
            Symbols.EIGHT,
            Symbols.SEVEN,
        ]
        self.game.set_what_cards_to_reveal(p_symbols=cards_symbols)

        bet_amount = 100
        self.game.phase_1__start()
        self.game.phase_2__place_bet(self.player_1, bet_amount)
        self.game.phase_2__place_bet(self.player_2, bet_amount)
        self.game.phase_2__place_bet(self.player_3, bet_amount)
        self.game.phase_3__give_players_the_second_card()

        self.game.phase_4__take_action_for_player(self.player_1, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player_1, Action.STAND)

        self.game.phase_4__take_action_for_player(self.player_2, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player_2, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player_2, Action.HIT)

        self.game.phase_4__take_action_for_player(self.player_3, Action.HIT)
        self.game.phase_4__take_action_for_player(self.player_3, Action.STAND)

        self.game.phase_5__reveals_banks_second_card()
        self.game.phase_6__bank_hits_until_bust_or_stand()

        self.assertEqual(
            self.game.players[0].capital, self.players_initial_capital - bet_amount
        )
        self.assertEqual(
            self.game.players[1].capital, self.players_initial_capital - bet_amount
        )
        self.assertEqual(
            self.game.players[2].capital, self.players_initial_capital + bet_amount
        )


if __name__ == "__main__":
    unittest.main()
