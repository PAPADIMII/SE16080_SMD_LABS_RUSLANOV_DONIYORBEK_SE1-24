# Task 9 — Cooperative multiple inheritance and MRO
# ValidateMixin must call super(); otherwise the MRO chain stops before AuditMixin/Model.
class Model:
    def save(self):
        print("Model.save: INSERT/UPDATE")

class TimestampMixin:
    def save(self):
        print("TimestampMixin: set updated_at")
        super().save()

class ValidateMixin:
    def save(self):
        print("ValidateMixin: validate fields")
        if not self.valid:
            raise ValueError("invalid invoice")
        super().save()

class AuditMixin:
    def save(self):
        super().save()
        print("AuditMixin: write audit entry")

class Invoice(TimestampMixin, ValidateMixin, AuditMixin, Model):
    def __init__(self, valid=True):
        self.valid = valid

def test_invoice_save_order(capsys):
    Invoice().save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]

def test_invalid_invoice_stops_before_save(capsys):
    import pytest
    with pytest.raises(ValueError):
        Invoice(valid=False).save()
    output = capsys.readouterr().out.splitlines()
    assert output == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
    ]

# Invoice.__mro__ is Invoice, TimestampMixin, ValidateMixin, AuditMixin, Model, object.
# If Model is placed before ValidateMixin, Model.save() terminates the chain before
# ValidateMixin is reached; cooperative mixins should precede the concrete base.
