# Task 10 — Registry at the system boundary
# The registry is the single place that maps external strings to payment classes.
from task01 import (
    PaymentMethod, Card, Click, Payme, Cash, BankTransfer
)

class UnknownPaymentMethodError(ValueError):
    pass

PAYMENT_METHODS = {
    "card": Card,
    "click": Click,
    "payme": Payme,
    "cash": Cash,
    "banktransfer": BankTransfer,
}

def create_payment_method(name: str) -> PaymentMethod:
    key = name.strip().lower()
    try:
        method_class = PAYMENT_METHODS[key]
    except KeyError:
        supported = ", ".join(sorted(PAYMENT_METHODS))
        raise UnknownPaymentMethodError(
            f"unknown payment method {name!r}; supported: {supported}"
        ) from None
    return method_class()

def test_registry_normalises_names():
    assert isinstance(create_payment_method(" Payme "), Payme)
    assert isinstance(create_payment_method("PAYME"), Payme)
    assert isinstance(create_payment_method("payme"), Payme)
    assert isinstance(create_payment_method("banktransfer"), BankTransfer)

def test_unknown_payment_method():
    import pytest
    with pytest.raises(UnknownPaymentMethodError, match="supported"):
        create_payment_method("crypto")
