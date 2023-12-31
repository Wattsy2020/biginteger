from hypothesis import given, strategies

from integer import BigInteger


@given(strategies.integers(), strategies.integers())
def test_biginteger_add(num1: int, num2: int) -> None:
    result = BigInteger.from_integer(num1) + BigInteger.from_integer(num2)
    assert result.to_integer() == num1 + num2


@given(strategies.integers(), strategies.integers())
def test_biginteger_sub(num1: int, num2: int) -> None:
    result = BigInteger.from_integer(num1) - BigInteger.from_integer(num2)
    assert result.to_integer() == num1 - num2


@given(strategies.integers(), strategies.integers())
def test_biginteger_mul(num1: int, num2: int) -> None:
    result = BigInteger.from_integer(num1) * BigInteger.from_integer(num2)
    assert result.to_integer() == num1 * num2


@given(strategies.integers(), strategies.integers())
def test_biginteger_gt(num1: int, num2: int) -> None:
    result = BigInteger.from_integer(num1) > BigInteger.from_integer(num2)
    assert result == (num1 > num2)
