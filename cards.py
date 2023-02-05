"""
This class holds the classes related to the cards
"""
from enum import Enum


class Suits(Enum):
    """
    the suit of the cards
    """
    DIMOND: str = '♦'
    SPADE: str = '♠'
    HEART: str = '♥'
    CLUB: str = '♣'


class Symbols(Enum):
    """
    the symbols of the cards
    """
    ACE: str = 'A'
    TWO: str = '2'
    THREE: str = '3'
    FOUR: str = '4'
    FIVE: str = '5'
    SIX: str = '6'
    SEVEN: str = '7'
    EIGHT: str = '8'
    NINE: str = '9'
    TEN: str = '10'
    JACK: str = 'J'
    QUEEN: str = 'Q'
    KING: str = 'K'


class Colors(Enum):
    """
    the color of the cards
    """
    RED: str = "R"
    BLACK: str = "B"


class Card:
    """
    a single card
    """
    suit: Suits
    symbol: Symbols
    color: Colors
    deck_number: int
    point: int
    alternative_point: int

    def __init__(self, p_suit: Suits, p_symbol: Symbols, p_deck_number: int=1) -> None:
        self.suit = p_suit
        self.symbol = p_symbol
        self.color = Colors.RED if p_symbol in [Suits.DIMOND, Suits.HEART] else Colors.BLACK
        self.deck_number = p_deck_number
    
    def __str__(self) -> str:
        return f"{self.symbol.value}{self.suit.value}"
    
    def set_point(self, p_value: int, p_alternative_value: int=None) -> None:
        self.point = p_value
        self.alternative_point = p_alternative_value