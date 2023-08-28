from hypothesis import given, strategies

from digit import Digit, add_digit


@given(
    strategies.integers(min_value=0, max_value=9),
    strategies.integers(min_value=0, max_value=9),
)
def test_add_digit(digit1: int, digit2: int) -> None:
    result_digit, carry = add_digit(
        Digit.from_integer(digit1), Digit.from_integer(digit2), Digit.ZERO
    )
    result_int = 10 * carry.to_integer() + result_digit.to_integer()
    assert result_int == digit1 + digit2
