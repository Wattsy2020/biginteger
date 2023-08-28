from __future__ import annotations

import enum


class Sign(int, enum.Enum):
    NEGATIVE = 0
    POSITIVE = 1

    def negate(self) -> Sign:
        return Sign.POSITIVE if self is Sign.NEGATIVE else Sign.NEGATIVE

    @classmethod
    def of_integer(cls, integer: int) -> Sign:
        return Sign.NEGATIVE if integer < 0 else Sign.POSITIVE

    def to_integer(self) -> int:
        return -1 if self is Sign.NEGATIVE else 1


def multiply_signs(sign1: Sign, sign2: Sign) -> Sign:
    """Calculate the sign resulting from multiplying two signs together"""
    if (sign1 is Sign.POSITIVE) == (sign2 is Sign.POSITIVE):
        return Sign.POSITIVE
    return Sign.NEGATIVE
