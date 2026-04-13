from solution import Inventory, PositiveInt

inv = Inventory(capacity=2)
inv.add('sword')
inv.add('shield')
assert list(inv) == ['sword', 'shield']

try:
    inv.add('x')
except ValueError:
    pass
else:
    raise AssertionError('overflow')

with inv.locked():
    try:
        inv.remove('sword')
    except RuntimeError:
        pass
    else:
        raise AssertionError('locked')

inv.remove('sword')
assert list(inv) == ['shield']
print('OK')