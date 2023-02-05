"""
The implementation of the costumized 21 game
"""
from abc import abstractmethod
from typing import List
from enum import Enum

from twenty_one_cards import TwentyOneCards
from cards import Card


class Roles(Enum):
    """
    the user type of the user

    BANK: the dealer 
    PLAYER: the gambler
    """
    BANK: str = 'bank'
    PLAYER: str = 'player'


class Action(Enum):
    """
    the actions users can take

    HIT: ask for a card
    STAND: hold the total points and end the turn and finish playing
    SPLIT: split the holding cards into two sets
    """
    HIT: str = 'hit'
    STAND: str = 'stand'
    SPLIT: str = 'split'


class States:
    """
    the status of a set at the time

    OPEN_TO_HIT: user can hit
    STAND: user no longer can hit
    BUST: user has bust (her cards' point has exceeded 21)
    """
    OPEN_TO_HIT: str = "open to hit"
    STAND: str = "stand"
    BUST: str = "bust"


class Set:
    cards: List[Card]
    state: States
    bet_amount: int

    def __init__(self) -> None:
        self.cards = []
        self.state = States.OPEN_TO_HIT
        self.has_won = None
        self.bet_amount = 0

    def append_card(self, p_card: Card):
        self.cards.append(p_card)
        self.check_if_bust()

    def get_total_points(self):
        return sum([card.point for card in self.cards])

    def check_if_bust(self):
        total_point = self.get_total_points()
        if total_point > 21:
            self.state = States.BUST


class User:
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

    def append_card(self, p_card: Card, p_set_number: int=0):

        # set should exist
        assert p_set_number <= (len(self.sets)-1)

        # bank cant split (have more than one set)
        if self.role is Roles.BANK:
            assert p_set_number == 0

        self.sets[p_set_number].append_card(p_card)

    # TODO: check abstracted methods 


class Player(User):

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

    def _get_set_states(self):
        sets_state = [set.state for set in self.sets]
        return sets_state

    def do_hit(self, p_card: Card):
        # check if player can hit
        sets_state = self._get_set_states()
        if not States.OPEN_TO_HIT in sets_state:
            raise Exception(f"There is no open to hit set to hit anymore.")
        target_set = sets_state.index(States.OPEN_TO_HIT)
        
        # do hit
        self.append_card(p_card=p_card, p_set_number=target_set)

    def do_stand(self):
        # check if player can stand
        sets_state = self._get_set_states()
        if not States.OPEN_TO_HIT in sets_state:
            raise Exception(f"There is no open set to stand.")
        target_set = sets_state.index(States.OPEN_TO_HIT)

        # do hit
        self.sets[target_set].state = States.STAND

    def do_split(self):
        # check if player can split
        sets_state = self._get_set_states()
        # -- if there is already an open to hit set
        if not States.OPEN_TO_HIT in sets_state:
            raise Exception(f"Can not split as there is no open to hit set.")
        target_set = sets_state.index(States.OPEN_TO_HIT)
        # -- if the open set has more than one card
        if len(self.sets[target_set].cards) > 2:
            raise Exception(f"Can not split when there are 3 cards or more in a set.")
        # -- if the points of the cards in the set are the same
        if self.sets[target_set].cards[0].point != self.sets[target_set].cards[1].point:
            raise Exception(f"The points of the cards in set are not equal to perform split.")

        # do split
        card = self.sets[target_set].cards.pop()
        self.sets.append(Set())
        self.sets[-1].cards.append(card)


class Bank(User):

    def __init__(self, p_name: str) -> None:
        super().__init__(Roles.BANK, p_name)
        self.sets.append(Set())  # but the bank can hold only one set

    def do_hit(self, p_card: Card):
        # check if bank can hit
        # -- if there is already an open to hit set
        if not States.OPEN_TO_HIT is self.sets[0].state:
            raise Exception(f"There is no open to hit set to hit anymore.")
        # -- if there the total points of the held cards is less than or equal to 16
        if self.sets[0].get_total_points() > 17:
            raise Exception(f"Bank can't hit when her totla point is more than 16.")
            
        # do hit
        self.append_card(p_card=p_card, p_set_number=0) 


    def do_stand(self):
        pass


class Game:

    cards: List[Card]
    bank: Bank
    players: List[Player]
    current_random_card_index: int = 0
    state:int = 0  # the current state of the game

    def __init__(self, p_players: List[Player]) -> None:
        self.players = p_players
        self.bank = Bank(p_name="Banky")

        # for every 3 group of players we need one deck of shuffled cards
        self.cards = TwentyOneCards(
            do_shuffle=True,
            p_number_of_decks=(len(p_players)//4)+1,
        ).cards

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

    def phase_4__take_action_for_player(self, p_player: Player, p_action: Action):
        if p_action is Action.HIT:
            card = self.get_a_random_card()
            p_player.do_hit(p_card=card)

        if p_action is Action.STAND:
            p_player.do_stand()

        if p_action is Action.SPLIT:
            p_player.do_split()

    def phase_5__reveals_banks_second_card(self):
        """
        It's done by a hit action, but it is equivalent to the revealing of the bank's second card in action.
        """
        # check if all players are ready
        can_bank_hit = self.check_if_all_players_are_ready()
        if not can_bank_hit:
            raise Exception(f"Can't reveal bank's card as not all players have finished their sets.")        
        
        # check internal conditions and do hit if possible
        card = self.get_a_random_card()
        self.bank.do_hit(p_card=card)

    def phase_6__bank_hits_until_bust_or_stand(self):
        # check if bank should hit
        # -- if players are ready
        can_bank_hit = self.check_if_all_players_are_ready()
        if not can_bank_hit:
            raise Exception(f"Can't bank cant hit as not all players have finished their sets.")
        # -- if there is at least one player who stands
        is_there_atleast_one_standing_player = False
        for player in self.players:
            for set in player.sets:
                if set.state is States.STAND:
                    is_there_atleast_one_standing_player = True
                    break
            if is_there_atleast_one_standing_player:
                break
        # -- if bank's points does not exceed 16
        while self.bank.sets[0].get_total_points() <= 16:
            # check few other conditions and do hit if possible
            card = self.get_a_random_card()
            self.bank.do_hit(p_card=card)
        # -- if bank is not bust then she should stand when her score has exceed 16
        if not self.bank.sets[0].state is States.BUST:
            self.bank.sets[0].state = States.STAND
        
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
    