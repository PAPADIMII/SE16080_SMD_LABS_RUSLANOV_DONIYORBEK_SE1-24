# Task 5 — Employee role composition
# 5.1 Employment identity remains the same; the employee's role changes.
# 5.4 Employee owns its role history (composition); each entry stores the role and start date.
from dataclasses import dataclass
from datetime import date

class Role:
    def monthly_pay(self):
        raise NotImplementedError

@dataclass
class LecturerRole(Role):
    hours: int
    def monthly_pay(self):
        return self.hours * 120_000

@dataclass
class HeadRole(Role):
    salary: int
    def monthly_pay(self):
        return self.salary + 3_000_000

class Employee:
    def __init__(self, emp_id, name, role, start_date=None):
        self.emp_id = emp_id
        self.name = name
        self.role = role
        self.role_history = [(role, start_date or date.today())]

    def monthly_pay(self):
        return self.role.monthly_pay()

    def change_role(self, new_role, start_date=None):
        self.role = new_role
        self.role_history.append((new_role, start_date or date.today()))

    def pay_for_date(self, when):
        applicable = [entry for entry in self.role_history if entry[1] <= when]
        if not applicable:
            raise ValueError("No role recorded for this date")
        role, _ = max(applicable, key=lambda entry: entry[1])
        return role.monthly_pay()

def test_employee_promotion_preserves_identity():
    from datetime import date
    employee = Employee(7, "Ali", LecturerRole(100), date(2026, 1, 1))
    same_object = employee
    assert employee.monthly_pay() == 12_000_000
    employee.change_role(HeadRole(14_000_000), date(2026, 2, 1))
    assert employee is same_object
    assert employee.emp_id == 7
    assert employee.monthly_pay() == 17_000_000
    assert employee.pay_for_date(date(2026, 1, 15)) == 12_000_000
    assert employee.pay_for_date(date(2026, 2, 15)) == 17_000_000
