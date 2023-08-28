from __future__ import annotations

from attrs import define

from digit import Digit, add_digit


@define(slots=True, frozen=True)
class BigInteger:
    _digits: list[Digit]  # list of least significant digit to most significant

    @property
    def num_digits(self) -> int:
        return len(self._digits)

    @property
    def is_zero(self) -> bool:
        return self._digits == [Digit.ZERO]

    def __add__(self, other: BigInteger) -> BigInteger:
        if self.is_zero:
            return other
        if other.is_zero:
            return self

        result_digits: list[Digit] = []
        max_num_digits = max(self.num_digits, other.num_digits)
        i = 0
        carry = Digit.ZERO
        while i < max_num_digits:
            left_digit = self._digits[i] if i < self.num_digits else Digit.ZERO
            right_digit = other._digits[i] if i < other.num_digits else Digit.ZERO

            # add in the carry from the previous sum
            if carry is not Digit.ZERO:
                right_digit, carry = add_digit(right_digit, carry, Digit.ZERO)

            # evaluate the sum of the digits and carry
            result_digit, carry = add_digit(left_digit, right_digit, carry)
            result_digits.append(result_digit)
            i += 1

        # Add any remaining carry as the leading digit
        if carry is not Digit.ZERO:
            result_digits.append(carry)
        return BigInteger(result_digits)

    def __str__(self) -> str:
        return "".join(map(str, reversed(self._digits)))

    @classmethod
    def from_integer(cls, integer: int) -> BigInteger:
        if integer < 0:
            raise NotImplementedError()
        if integer == 0:
            return BigInteger([Digit.ZERO])

        digits: list[Digit] = []
        while integer != 0:
            digits.append(Digit.from_integer(integer % 10))
            integer //= 10
        return BigInteger(digits)

    def to_integer(self) -> int:
        return sum(
            10**place * digit.to_integer() for place, digit in enumerate(self._digits)
        )
