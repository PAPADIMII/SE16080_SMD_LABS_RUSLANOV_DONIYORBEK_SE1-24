# Task 3 — Subscription pricing
# Children override net() only; the parent applies VAT exactly once.
class Subscription:
    VAT_PERCENT = 12

    def __init__(self, user, months):
        self.user = user
        self.months = months
        self.base_monthly = 50_000

    def net(self):
        return self.base_monthly * self.months

    def price(self):
        return self.net() * (100 + self.VAT_PERCENT) // 100

class StudentSubscription(Subscription):
    def net(self):
        return self.base_monthly * self.months // 2

class FamilySubscription(Subscription):
    def __init__(self, user, months, members):
        super().__init__(user, months)
        self.members = members

    def net(self):
        base = super().net()
        extra = 20_000 * (len(self.members) - 1) * self.months
        return base + extra

def test_subscription_prices():
    standard = Subscription("Ali", 3)
    student = StudentSubscription("Vali", 3)
    family = FamilySubscription("Sami", 3, ["A", "B", "C", "D"])
    assert standard.price() == 168_000
    assert student.price() == 84_000
    assert family.price() == 369_600

def test_vat_is_inherited():
    Subscription.VAT_PERCENT = 15
    try:
        assert Subscription("A", 1).price() == 57_500
        assert StudentSubscription("B", 1).price() == 28_750
        assert FamilySubscription("C", 1, ["A", "B"]).price() == 80_500
    finally:
        Subscription.VAT_PERCENT = 12
