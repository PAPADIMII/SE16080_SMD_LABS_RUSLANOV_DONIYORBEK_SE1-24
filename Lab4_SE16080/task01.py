# Task 1 — Payment methods and Open/Closed design
# 1.2 Click and Payme are separate classes: their fees are equal today, but either
# provider can change independently in the future.
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def fee(self, amount: int) -> int:
        """Return the payment fee in sum."""
        raise NotImplementedError

    @property
    @abstractmethod
    def refundable(self) -> bool:
        raise NotImplementedError

    def charge(self, amount: int) -> dict:
        return {"charged": amount + self.fee(amount), "refundable": self.refundable}

class Card(PaymentMethod):
    def fee(self, amount): return amount * 15 // 1000
    @property
    def refundable(self): return True

class Click(PaymentMethod):
    def fee(self, amount): return amount * 10 // 1000
    @property
    def refundable(self): return True

class Payme(PaymentMethod):
    def fee(self, amount): return amount * 10 // 1000
    @property
    def refundable(self): return True

class Cash(PaymentMethod):
    def fee(self, amount): return 0
    @property
    def refundable(self): return False

class BankTransfer(PaymentMethod):
    def fee(self, amount): return 5_000
    @property
    def refundable(self): return True

class Checkout:
    def pay(self, method: PaymentMethod, amount: int) -> dict:
        return method.charge(amount)

def test_payment_methods():
    checkout = Checkout()
    assert checkout.pay(Card(), 100_000) == {"charged": 101_500, "refundable": True}
    assert checkout.pay(Click(), 100_000) == {"charged": 101_000, "refundable": True}
    assert checkout.pay(Payme(), 100_000) == {"charged": 101_000, "refundable": True}
    assert checkout.pay(Cash(), 100_000) == {"charged": 100_000, "refundable": False}
    assert checkout.pay(BankTransfer(), 100_000) == {"charged": 105_000, "refundable": True}
