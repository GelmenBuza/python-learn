from decimal import Decimal
from solution import PaymentService, CardPayment, WalletPayment

svc = PaymentService(CardPayment())
assert 'CARD' in svc.process(Decimal('10.00'))

svc2 = PaymentService(WalletPayment(), logger=lambda s: None)
assert svc2.process(Decimal('1')).startswith('WALLET')

try:
    PaymentService(CardPayment()).process(Decimal('-1'))
except ValueError:
    pass
else:
    raise AssertionError('expected ValueError')
print('OK')