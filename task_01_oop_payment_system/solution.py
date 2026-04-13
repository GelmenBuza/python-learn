from decimal import Decimal
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: Decimal):
        pass

class CardPayment(PaymentStrategy):
    def pay(self, amount: Decimal):
        return f'CARD:{amount}'

class WalletPayment(PaymentStrategy):
    def pay(self, amount: Decimal):
        return f'WALLET:{amount}'

class PaymentService:
    def __init__(self, payment_strategy: PaymentStrategy, logger=None):
        self.payment_strategy = payment_strategy
        self.logger = logger or (lambda s: None)
    def process(self, amount: Decimal):
        if amount <= 0:
            raise ValueError
        else:
            self.logger(str(amount))
            return self.payment_strategy.pay(amount)