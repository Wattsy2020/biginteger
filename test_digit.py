from hypothesis import given, strategies

from digit import Digit, add_digit, sub_digit


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


@given(
    strategies.integers(min_value=0, max_value=9),
    strategies.integers(min_value=0, max_value=9),
)
def test_sub_digit(digit1: int, digit2: int) -> None:
    if digit1 >= digit2:
        result_digit = sub_digit(Digit.from_integer(digit1), Digit.from_integer(digit2))
        assert result_digit.to_integer() == digit1 - digit2


@given(
    strategies.integers(min_value=0, max_value=9),
    strategies.integers(min_value=0, max_value=9),
)
def test_gt_digit(digit1: int, digit2: int) -> None:
    result = Digit.from_integer(digit1) > Digit.from_integer(digit2)
    assert result == (digit1 > digit2)
