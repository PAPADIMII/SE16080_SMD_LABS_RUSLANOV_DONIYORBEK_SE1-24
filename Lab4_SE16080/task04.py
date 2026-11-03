# Task 4 — Append-only audit log
# 4.1 AuditLog is not safely substitutable for list: clear(), pop(), sort(),
# item assignment, etc. violate append-only behaviour.
# 4.3 A tuple makes each recorded entry immutable.
# 4.4 Overriding selected list methods is fragile because list exposes many mutators.
class AuditLog:
    def __init__(self):
        self.__entries = []

    def record(self, user, action):
        self.__entries.append((user, action))

    def __len__(self):
        return len(self.__entries)

    def __iter__(self):
        return iter(self.__entries)

    def last(self, n):
        if n <= 0:
            return []
        return list(self.__entries[-n:])

def test_audit_log():
    log = AuditLog()
    log.record("admin", "approve_loan#77")
    log.record("ali", "login")
    assert len(log) == 2
    assert list(log) == [("admin", "approve_loan#77"), ("ali", "login")]
    assert log.last(1) == [("ali", "login")]
    assert isinstance(log.last(1)[0], tuple)
    assert not hasattr(log, "clear")
