from __future__ import annotations

import enum
from functools import cache


class Digit(enum.Enum):
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

    def __gt__(self, other: Digit) -> bool:
        left = self
        right = other
        while left is not Digit.ZERO and right is not Digit.ZERO:
            left = left.decrement()
            right = right.decrement()
        return left is not Digit.ZERO

    @classmethod
    def from_integer(cls, integer: int) -> Digit:
        if integer < 0 or integer > 9:
            raise ValueError(f"{integer=} must be in range [0,9]")
        return list(cls)[integer]

    def to_integer(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)


@cache
def decrement(digit: Digit) -> tuple[Digit, bool]:
    """Decrement a digit, return (digit, whether to borrow a one"""
    return (Digit.NINE, True) if digit is Digit.ZERO else (digit.decrement(), False)


@cache
def increment(digit: Digit) -> tuple[Digit, bool]:
    """Increment a digit, return (digit, whether to carry a one)"""
    return (Digit.ZERO, True) if digit is Digit.NINE else (digit.increment(), False)


@cache
def add_digit(digit1: Digit, digit2: Digit) -> tuple[Digit, bool]:
    """Add the digits, returning a tuple of (added digit, whether a one is carried)"""
    carry_one = False
    while digit1 is not Digit.ZERO:
        digit1 = digit1.decrement()
        digit2, new_carry_one = increment(digit2)
        carry_one = carry_one or new_carry_one
    return (digit2, carry_one)


@cache
def sub_digit(digit1: Digit, digit2: Digit) -> Digit:
    """Evaluate digit1 - digit2, note digit1 must be greater than digit2"""
    while digit2 is not Digit.ZERO:
        digit2 = digit2.decrement()
        digit1 = digit1.decrement()
    return digit1
