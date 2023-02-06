"""
The implementation of the costumized 21 game
"""
import logging, coloredlogs

coloredlogs.install(level=logging.DEBUG)

from abc import abstractmethod
from typing import List
from enum import Enum

from twenty_one_cards import TwentyOneCards
from cards import Card, Symbols


class Roles(Enum):
    """
    the user type of the user

    BANK: the dealer
    PLAYER: the gambler
    """

    BANK: str = "bank"
    PLAYER: str = "player"


class Action(Enum):
    """
    the actions users can take

    HIT: ask for a card
    STAND: hold the total points and end the turn and finish playing
    SPLIT: split the holding cards into two sets
    """

    HIT: str = "hit"
    STAND: str = "stand"
    SPLIT: str = "split"


class States:
    """
    the status of a set at the time

    OPEN_TO_HIT: user can hit
    STAND: user no longer can hit
    BUST: user has bust (her cards' point has exceeded 21)
    """

    OPEN_TO_HIT: str = "open-to-hit"
    STAND: str = "stand"
    BUST: str = "bust"


class Set:
    """
    Holds the set of cards of the game
    """

    cards: List[Card]
    state: States
    bet_amount: int

    def __init__(self) -> None:
        self.cards = []
        self.state = States.OPEN_TO_HIT
        self.bet_amount = 0

    def append_card(self, p_card: Card):
        self.cards.append(p_card)
        self.check_if_bust()

    def get_total_points(self):
        total_points = sum([card.point for card in self.cards])
        total_points_alternative = sum(
            [
                card.alternative_point
                for card in self.cards
                if card.alternative_point is not None
            ]
        )
        # as its the ACE wich has 2 possible points; 11 and 1 which the difference is 11-1=10:
        if total_points_alternative >= 2:  # TODO: provide a better solution
            return (
                total_points
                if total_points <= 21
                else total_points - (total_points_alternative - 1) * 10
            )
        else:
            return (
                total_points
                if total_points <= 21
                else total_points - total_points_alternative * 10
            )

    def check_if_bust(self):
        total_point = self.get_total_points()

        if total_point > 21 and total_point:
            self.state = States.BUST


class User:
    """
    A base class for bank and players
    """

    name: str
    role: Roles
    sets: List[Set]

    def __init__(self, p_role: Roles, p_name: str) -> None:
        self.role = p_role
        self.name = p_name
        self.sets = []

    def __str__(self) -> str:
        return self.name

    @abstractmethod
    def do_hit(self):
        pass

    @abstractmethod
    def do_stand(self):
        pass

    @abstractmethod
    def append_card(self):
        pass

    def append_card(self, p_card: Card, p_set_number: int = 0):
        # set should exist
        if p_set_number > (len(self.sets) - 1):
            raise Exception("Wrong set number is passed.")

        # bank cant split (have more than one set)
        if self.role is Roles.BANK:
            assert p_set_number == 0

        self.sets[p_set_number].append_card(p_card)


class Player(User):
    """
    A user who gamples
    """

    capital: int = 0

    def __init__(self, p_name: str, p_capital: int) -> None:
        super().__init__(Roles.PLAYER, p_name)

        if p_capital < 0:
            raise Exception("Capital can not be negative.")
        self.capital = p_capital
        self.sets.append(Set())

    def place_initial_bet(self, p_bet_amount: int):
        self.capital -= p_bet_amount
        self.sets[0].bet_amount += p_bet_amount
        logging.info(f"{self.name} beted {p_bet_amount}.")

    def _get_set_states(self):
        sets_state = [set.state for set in self.sets]
        return sets_state

    def do_hit(self, p_card: Card):
        logging.info(f"{self.name} choosed to HIT.")
        # check if player can hit
        sets_state = self._get_set_states()
        if not States.OPEN_TO_HIT in sets_state:
            logging.warning(
                f"There is no open to hit set to hit anymore. Action ignored."
            )
        else:
            # do hit
            target_set = sets_state.index(States.OPEN_TO_HIT)
            self.append_card(p_card=p_card, p_set_number=target_set)

    def do_stand(self):
        logging.info(f"{self.name} choosed to STAND.")
        # check if player can stand
        sets_state = self._get_set_states()
        if not States.OPEN_TO_HIT in sets_state:
            logging.warning(f"There is no open set to stand. Action ignored.")
        else:
            # do hit
            target_set = sets_state.index(States.OPEN_TO_HIT)
            self.sets[target_set].state = States.STAND

    def do_split(self):
        logging.info(f"{self.name} choosed to SPLIT.")
        # check if player can split
        sets_state = self._get_set_states()
        # -- if there is already an open to hit set
        if not States.OPEN_TO_HIT in sets_state:
            logging.warning(
                f"Can not split as there is no open to hit set. Action ignored."
            )
        else:
            target_set = sets_state.index(States.OPEN_TO_HIT)
            # -- if the open set has more than one card
            if len(self.sets[target_set].cards) > 2:
                logging.warning(
                    f"Can not split when there are 3 cards or more in a set. Action ignored."
                )
            # -- if the points of the cards in the set are the same
            elif (
                self.sets[target_set].cards[0].point
                != self.sets[target_set].cards[1].point
            ):
                logging.warning(
                    f"The points of the cards in set are not equal to perform split. Action ignored."
                )
            else:
                # do split
                card = self.sets[target_set].cards.pop()
                self.sets.append(Set())
                self.sets[-1].cards.append(card)
                bet_amount = self.sets[target_set].bet_amount
                self.capital -= bet_amount
                self.sets[-1].bet_amount = bet_amount


class Bank(User):
    """
    A user who deals
    """

    def __init__(self, p_name: str) -> None:
        super().__init__(Roles.BANK, p_name)
        self.sets.append(Set())  # but the bank can hold only one set

    def do_hit(self, p_card: Card):
        logging.info(f"{self.name} choosed to HIT.")
        # check if bank can hit
        # -- if there is already an open to hit set
        if not States.OPEN_TO_HIT is self.sets[0].state:
            logging.warning(
                f"There is no open to hit set to hit anymore. Action ignored."
            )
        else:
            # -- if there the total points of the held cards is less than or equal to 16
            if self.sets[0].get_total_points() > 17:
                logging.warning(
                    f"Bank can't hit when her totla point is more than 16. Action ignored"
                )
            else:
                # do hit
                self.append_card(p_card=p_card, p_set_number=0)

    def do_stand(self):
        logging.info(f"{self.name} choosed to HIT.")
        self.sets[0].state = States.STAND


class Game:
    """
    The class which hold the functionalities of the game
    """

    cards: List[Card]
    bank: Bank
    players: List[Player]
    current_random_card_index: int = 0

    def __init__(self, p_players: List[Player]) -> None:
        self.players = p_players
        self.bank = Bank(p_name="Banky")

        # for every 3 group of players we need one deck of shuffled cards
        self.cards = TwentyOneCards(
            do_shuffle=True,
            p_number_of_decks=(len(p_players) // 4) + 1,
        ).cards

    def set_what_cards_to_reveal(self, p_symbols: List[Symbols]):
        """
        A heler function for unit testing which allows us to choose what cards to reveal
        The filter is the cards symbol as it's the only factor wich determins the point of the card.
        """

        def find_the_card(cards: List[Card], p_symbol: Symbols):
            """
            A helper function for finding the target card based on the symbol it has
            """
            for card in cards:
                if card.symbol is p_symbol:
                    return card

        target_cards: List[Card] = []
        for symbol in p_symbols:
            target_cards.append(find_the_card(cards=self.cards, p_symbol=symbol))

        # replace the previously generated set of cards to the new set of cards
        self.cards = target_cards

    def reset(self):
        for player in self.players:
            for set in player.sets:
                set.cards.clear()
                set.bet_amount = 0
                set.state = States.OPEN_TO_HIT

    def get_a_random_card(self) -> Card:
        a_random_card = self.cards[self.current_random_card_index]
        self.current_random_card_index += 1
        return a_random_card

    def check_if_all_players_are_ready(self):
        for player in self.players:
            for set in player.sets:
                if set.state is States.OPEN_TO_HIT:
                    return False
        return True

    def phase_1__start(self):
        """
        Game initializes by givving all the players and the bank a card
        """
        # start from the first random card
        self.current_random_card_index = 0

        # give each user a card
        # -- give a card to players
        for player in self.players:
            card = self.get_a_random_card()
            player.append_card(p_card=card)

        # -- give a card to bank
        card = self.get_a_random_card()
        self.bank.append_card(p_card=card)

        self.draw_the_game()

    def phase_2__place_bet(self, p_player: Player, p_bet_amount: int):
        """
        Places bets both for bank and players.
        """
        p_player.place_initial_bet(p_bet_amount)

    def phase_3__give_players_the_second_card(self):
        """
        Give players the second card. Therefore, by then they will have 2 cards in total.
        """
        for player in self.players:
            card = self.get_a_random_card()
            player.append_card(p_card=card)

        self.draw_the_game()

    def phase_4__take_action_for_player(self, p_player: Player, p_action: Action):
        """
        Perform action for the player
        """
        if p_action is Action.HIT:
            card = self.get_a_random_card()
            p_player.do_hit(p_card=card)

        if p_action is Action.STAND:
            p_player.do_stand()

        if p_action is Action.SPLIT:
            p_player.do_split()

        self.draw_the_game()

    def phase_5__reveals_banks_second_card(self):
        """
        It's done by a hit action, but it is equivalent to the revealing of the bank's second card in action.
        """
        # check if all players are ready
        can_bank_hit = self.check_if_all_players_are_ready()
        if not can_bank_hit:
            raise Exception(
                f"Can't reveal bank's card as not all players have finished their sets."
            )

        # check internal conditions and do hit if possible
        card = self.get_a_random_card()
        self.bank.do_hit(p_card=card)

        self.draw_the_game()

    def phase_6__bank_hits_until_bust_or_stand(self):
        """
        Continously perform hit action for bank untill it becomes impossible
        """
        # check if bank should hit
        # -- if players are ready
        can_bank_hit = self.check_if_all_players_are_ready()
        if not can_bank_hit:
            raise Exception(
                f"Bank can't hit as not all players have finished their sets."
            )

        # -- if there is at least one player who stands
        is_there_atleast_one_standing_player = False
        for player in self.players:
            for set in player.sets:
                if set.state is States.STAND:
                    is_there_atleast_one_standing_player = True
                    break
            if is_there_atleast_one_standing_player:
                break

        if not is_there_atleast_one_standing_player:
            self.bank.do_stand()
        else:
            # -- if bank's points does not exceed 16
            while self.bank.sets[0].get_total_points() <= 16:
                # check few other conditions and do hit if possible
                card = self.get_a_random_card()
                self.bank.do_hit(p_card=card)

            # -- if bank is not bust then she should stand when her score has exceed 16
            if not self.bank.sets[0].state is States.BUST:
                self.bank.do_stand()

        self.draw_the_game()
        self.evaluate()

    def evaluate(self):
        """
        finds the loser and winner sets and make the calculatios regarding the capital
        """
        # players set bust
        for player in self.players:
            for set in player.sets:
                if set.state is States.BUST:
                    # bank wins the set
                    set.bet_amount = 0

        # bank set bust
        if self.bank.sets[0].state is States.BUST:
            for set in player.sets:
                if set.state is States.STAND:
                    # player wins the set
                    player.capital += set.bet_amount * 2
                    set.bet_amount = 0

        # check by point of sets if no-one bust
        bank_total_points = self.bank.sets[0].get_total_points()
        for player in self.players:
            for set in player.sets:
                if set.get_total_points() <= bank_total_points:
                    # bank wins the set
                    set.bet_amount = 0
                else:
                    # player wins the set
                    player.capital += set.bet_amount * 2
                    set.bet_amount = 0

        for player in self.players:
            logging.info(f"{player.name}'s capital is {player.capital}.")

    def draw_the_game(self):
        """
        Draw the cards and points in console
        """
        print("-" * 40)
        print("Bank:")
        print("\t[ ", end="")
        for card in self.bank.sets[0].cards:
            print(card, end=" ")
        print(
            f"] => {self.bank.sets[0].get_total_points()} points - {self.bank.sets[0].state}"
        )

        for player in self.players:
            print(f"{player.name}:")
            for i, set in enumerate(player.sets):
                print(f"{i}:\t[ ", end="")
                for card in set.cards:
                    print(card, end=" ")
                print(f"] => {set.get_total_points()} points - {set.state}")
