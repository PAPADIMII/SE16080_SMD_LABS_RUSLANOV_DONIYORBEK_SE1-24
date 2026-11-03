# Task 7 — Immutable Money value object
# Ordering is implemented explicitly so different currencies are never compared.
from dataclasses import dataclass
from functools import total_ordering

class CurrencyMismatchError(ValueError):
    pass

@total_ordering
@dataclass(frozen=True)
class Money:
    amount: int
    currency: str

    def __post_init__(self):
        if not isinstance(self.amount, int):
            raise TypeError("amount must be an int in minor units")
        if not isinstance(self.currency, str) or len(self.currency) != 3:
            raise ValueError("currency must be a 3-letter code")
        object.__setattr__(self, "currency", self.currency.upper())

    def _check_currency(self, other):
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"cannot combine {self.currency} with {other.currency}"
            )

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other):
        if other == 0:
            return self
        return NotImplemented

    def __mul__(self, quantity):
        if not isinstance(quantity, int):
            return NotImplemented
        return Money(self.amount * quantity, self.currency)

    def __rmul__(self, quantity):
        return self.__mul__(quantity)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return self.amount < other.amount

def test_money():
    import pytest
    price = Money(500, "UZS")
    assert price + Money(200, "UZS") == Money(700, "UZS")
    assert price * 3 == Money(1500, "UZS")
    assert 3 * price == Money(1500, "UZS")
    assert sum([price, Money(200, "UZS")]) == Money(700, "UZS")
    assert (price == 500) is False
    assert len({price: "value"}) == 1
    assert Money(100, "UZS") < Money(200, "UZS")
    with pytest.raises(CurrencyMismatchError):
        _ = Money(100, "USD") + Money(1, "UZS")
    with pytest.raises(CurrencyMismatchError):
        _ = Money(100, "USD") > Money(1, "UZS")

# Money * Money and Money / Money are intentionally unsupported:
# their meaning is not obvious for a monetary amount.
