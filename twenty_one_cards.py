"""
This script prepares and generates the cards for the 21 game.
"""
import itertools
from typing import List

import cards

from random import shuffle


class TwentyOneCards:
    """
    the cards with the asociated points for the 21 game
    """
    cards_set: List[cards.Card]

    def __init__(self, p_number_of_decks: int=1, do_shuffle: bool=True) -> None:
        self.cards = []

        the_ace = cards.Symbols.ACE
        usual_cards_symbol = [symbol for symbol in cards.Symbols][1:10]  # cards from 2 to 10

        # generate cards and set the points for the game
        for deck, suit, symbol in itertools.product(
            range(p_number_of_decks), 
            cards.Suits, 
            cards.Symbols):

            # generate the card
            card = cards.Card(
                p_suit=suit,
                p_symbol=symbol,
                p_deck_number=deck,
            )

            # set the point of the card

            if card.symbol is the_ace:
                card.set_point(
                    p_value=11, 
                    p_alternative_value=1,
                )

            elif card.symbol in usual_cards_symbol:
                card.set_point(p_value=int(symbol.value))

            elif card.symbol is cards.Symbols.JACK:
                card.set_point(p_value=1)

            elif card.symbol is cards.Symbols.QUEEN:
                card.set_point(p_value=2)

            elif card.symbol is cards.Symbols.KING:
                card.set_point(p_value=3)
            
            # append tha card
            self.cards.append(card)

        # shuffle the cards
        if do_shuffle:
            shuffle(self.cards)
