from __future__ import annotations

from functools import cache
from typing import Any

from attrs import define

from digit import Digit, add_digit, decrement, increment, sub_digit
from sign import Sign, multiply_signs


@define(slots=True, frozen=True)
class BigInteger:
    _digits: list[Digit]  # list of least significant digit to most significant
    _sign: Sign

    @property
    def num_digits(self) -> int:
        return len(self._digits)

    @property
    def is_zero(self) -> bool:
        return self._digits == [Digit.ZERO]

    @property
    def is_negative(self) -> bool:
        return self._sign is Sign.NEGATIVE

    def negate(self) -> BigInteger:
        return BigInteger(self._digits, self._sign.negate())

    def with_sign(self, sign: Sign) -> BigInteger:
        return self if self._sign is sign else BigInteger(self._digits, sign)

    def absolute(self) -> BigInteger:
        return self.with_sign(Sign.POSITIVE)

    def greater_than(self, other: BigInteger) -> bool:
        """Calculate whether self is greater than other, both of which must be positive integers"""
        assert not (self.is_negative or other.is_negative)

        if self.num_digits != other.num_digits:
            return self.num_digits > other.num_digits

        for left_digit, right_digit in zip(
            reversed(self._digits), reversed(other._digits)
        ):
            if left_digit is not right_digit:
                return left_digit > right_digit
        return False

    def __gt__(self, other: BigInteger | Any) -> bool:
        if not isinstance(other, BigInteger):
            raise NotImplementedError()
        if self == other:
            return False
        if self.is_negative and other.is_negative:
            return other.negate().greater_than(self.negate())
        if self.is_negative or other.is_negative:
            return other.is_negative
        return self.greater_than(other)

    def _add(self, other: BigInteger) -> BigInteger:
        """Add two big integers"""
        assert not (self.is_negative or other.is_negative)

        result_digits: list[Digit] = []
        max_num_digits = max(self.num_digits, other.num_digits)
        i = 0
        carry_one = False
        while i < max_num_digits:
            left_digit = self._digits[i] if i < self.num_digits else Digit.ZERO
            right_digit = other._digits[i] if i < other.num_digits else Digit.ZERO

            # add in the carry from the previous sum
            if carry_one:
                # note carry_one and new_carry_one cannot both be true
                # if carry_one is true than left_digit must be 9, so now set to 0, so anything + it cannot have a carry
                left_digit, carry_one = increment(left_digit)
                result_digit, new_carry_one = add_digit(left_digit, right_digit)
                carry_one = carry_one or new_carry_one
            else:
                result_digit, carry_one = add_digit(left_digit, right_digit)
            result_digits.append(result_digit)
            i += 1

        # Add a remaining carry as the leading digit
        if carry_one:
            result_digits.append(Digit.ONE)
        return BigInteger(result_digits, self._sign)

    def __add__(self, other: BigInteger | Any) -> BigInteger:
        if not isinstance(other, BigInteger):
            raise NotImplementedError()
        if self.is_zero:
            return other
        if other.is_zero:
            return self
        if self.is_negative and other.is_negative:
            # (-a) + -(b) = -1(a + b)
            return self.negate()._add(other.negate()).negate()
        if other.is_negative:
            return self - other.negate()
        if self.is_negative:
            return other - self.negate()
        return self._add(other)

    def subtract(self, other: BigInteger) -> BigInteger:
        """Subtract other from self. self must be strictly larger than other"""
        assert not (self.is_negative or other.is_negative)

        result_digits: list[Digit] = []
        max_num_digits = max(self.num_digits, other.num_digits)
        i = 0
        borrow_one = False  # whether we borrowed one from from a previous subtraction, e.g. in 27 - 19: 7 - 9 is negative so we borrow a one from 2, getting 18 - 10
        while i < max_num_digits:
            left_digit = self._digits[i] if i < self.num_digits else Digit.ZERO
            right_digit = other._digits[i] if i < other.num_digits else Digit.ZERO

            if borrow_one:
                # subtract the borrow from the previous subtraction
                left_digit, borrow_one = decrement(left_digit)
                result_digit, new_borrow_one = sub_digit(left_digit, right_digit)
                borrow_one = borrow_one or new_borrow_one
            else:
                result_digit, borrow_one = sub_digit(left_digit, right_digit)
            result_digits.append(result_digit)
            i += 1

        # Remove leading zeros
        while result_digits[-1] == Digit.ZERO:
            result_digits.pop()
        return BigInteger(result_digits, self._sign)

    def __sub__(self, other: BigInteger | Any) -> BigInteger:
        if not isinstance(other, BigInteger):
            raise NotImplementedError()
        if self.is_zero:
            return other.negate()
        if other.is_zero:
            return self
        if self == other:
            return ZERO
        if self.is_negative and other.is_negative:
            return other.negate() - self.negate()  # (-a) - (-b) = (-a) + b = b - a
        if other.is_negative:
            return self._add(other.negate())
        if self.is_negative:
            # (-a) - (b) = -((a) - (-b)) = -((a) + (b))
            return self.negate()._add(other).negate()
        if self.greater_than(other):
            return self.subtract(other)
        return other.subtract(self).negate()  # x - y = -1 * (y - x)

    def multiply_tenth_power(self, power: int) -> BigInteger:
        """Efficiently multiply by a tenth power, by adding zeros to the digits"""
        if power < 0:
            raise ValueError(f"{power=} must be positive")
        return BigInteger(([Digit.ZERO] * power) + self._digits, self._sign)

    def multiply(self, other: BigInteger) -> BigInteger:
        """
        Multiply two numbers with multiple digits in them
        Use a power of 10 strategy, e.g. for num * 9091, evaluate as 9*num with three zeros at end, 9*num with 1 zero at end, and 1*num
        """

        @cache
        def calc_multiple(digit: Digit) -> BigInteger:
            """Return digit * self"""
            if digit is Digit.ZERO:
                return ZERO
            if digit is Digit.ONE:
                return self
            return self + calc_multiple(digit.decrement())

        multiples = (
            calc_multiple(digit).multiply_tenth_power(place)
            for place, digit in enumerate(other._digits)
        )
        return sum(multiples, start=ZERO)

    def __mul__(self, other: BigInteger | Any) -> BigInteger:
        if not isinstance(other, BigInteger):
            raise NotImplementedError()
        if self.is_zero or other.is_zero:
            return ZERO

        absolute_result = self.absolute().multiply(other.absolute())
        result_sign = multiply_signs(self._sign, other._sign)
        return absolute_result.with_sign(result_sign)

    @classmethod
    def from_integer(cls, integer: int) -> BigInteger:
        if integer == 0:
            return ZERO

        sign = Sign.of_integer(integer)
        integer = abs(integer)
        digits: list[Digit] = []
        while integer != 0:
            digits.append(Digit.from_integer(integer % 10))
            integer //= 10
        return BigInteger(digits, sign)

    def to_integer(self) -> int:
        return self._sign.to_integer() * sum(
            10**place * digit.to_integer() for place, digit in enumerate(self._digits)
        )

    def __str__(self) -> str:
        return "".join(map(str, reversed(self._digits)))


ZERO = BigInteger([Digit.ZERO], Sign.POSITIVE)
