from __future__ import annotations

import enum
from functools import cache


class Digit(int, enum.Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    @cache
    def decrement(self) -> Digit:
        """Decrement a digit, invalid for ZERO"""
        match self:
            case Digit.ZERO:
                raise ValueError("Cannot decrement 0")
            case Digit.ONE:
                return Digit.ZERO
            case Digit.TWO:
                return Digit.ONE
            case Digit.THREE:
                return Digit.TWO
            case Digit.FOUR:
                return Digit.THREE
            case Digit.FIVE:
                return Digit.FOUR
            case Digit.SIX:
                return Digit.FIVE
            case Digit.SEVEN:
                return Digit.SIX
            case Digit.EIGHT:
                return Digit.SEVEN
            case Digit.NINE:
                return Digit.EIGHT

    @cache
    def increment(self) -> Digit:
        """Increment a digit, doesn't support incrementing 9"""
        match self:
            case Digit.ZERO:
                return Digit.ONE
            case Digit.ONE:
                return Digit.TWO
            case Digit.TWO:
                return Digit.THREE
            case Digit.THREE:
                return Digit.FOUR
            case Digit.FOUR:
                return Digit.FIVE
            case Digit.FIVE:
                return Digit.SIX
            case Digit.SIX:
                return Digit.SEVEN
            case Digit.SEVEN:
                return Digit.EIGHT
            case Digit.EIGHT:
                return Digit.NINE
            case Digit.NINE:
                raise ValueError("Cannot increment 9")

    @classmethod
    def from_integer(cls, integer: int) -> Digit:
        if integer < 0 or integer > 9:
            raise ValueError(f"{integer=} must be in range [0,9]")
        return list(cls)[integer]

    def to_integer(self) -> int:
        return self.value


@cache
def increment(digit: Digit, carry: Digit) -> tuple[Digit, Digit]:
    """Increment a digit and carry"""
    if digit is Digit.NINE:
        return (Digit.ZERO, carry.increment())
    return (digit.increment(), carry)


@cache
def add_digit(digit1: Digit, digit2: Digit, carry: Digit) -> tuple[Digit, Digit]:
    """Add the digits and carry, returning a tuple of (added digit, carry)"""
    while digit1 is not Digit.ZERO:
        digit1 = digit1.decrement()
        digit2, carry = increment(digit2, carry)
    return (digit2, carry)
