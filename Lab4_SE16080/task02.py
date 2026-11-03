# Task 2 — Abstract notifier
# 2.1 The misspelled sned() is a different method; inherited send() silently does nothing.
# 2.3 send() is abstract; notify() is concrete shared logic.
from abc import ABC, abstractmethod

class Notifier(ABC):
    max_length = 1000

    @abstractmethod
    def send(self, recipient, text):
        raise NotImplementedError

    def notify(self, recipient, text):
        self.send(recipient, text[:self.max_length])

class TelegramNotifier(Notifier):
    max_length = 4096
    def send(self, recipient, text):
        self.last_message = (recipient, text)

class SmsNotifier(Notifier):
    max_length = 160
    def send(self, recipient, text):
        self.last_message = (recipient, text)

def test_notifier_limits():
    message = "x" * 5000
    telegram = TelegramNotifier()
    sms = SmsNotifier()
    telegram.notify("@ali", message)
    sms.notify("+998901234567", message)
    assert len(telegram.last_message[1]) == 4096
    assert len(sms.last_message[1]) == 160

def test_notifier_is_abstract():
    import pytest
    with pytest.raises(TypeError):
        Notifier()
