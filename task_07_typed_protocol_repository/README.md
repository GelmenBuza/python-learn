# Задание: Типизация — Protocol, TypeVar, Generic

## 🎯 Цель и краткое описание

Описать **репозиторий** через `Protocol`, обобщить идентификатор через **`TypeVar`**, проверить статически **`mypy`** (без запуска внешних сервисов).

## 📚 Темы для изучения/повторения

- `typing.Protocol` — структурная типизация (duck typing формализованный)
- `TypeVar` с ограничениями (`bound=`)
- `Generic[T]` для класса хранилища
- `TypedDict` для записей (опционально в решении)

## 📝 ТЗ

**Реализовать в `solution.py`:**

1. `T = TypeVar('T', bound='Entity')` — базовый класс `Entity` с полем `id: int`.
2. `Protocol` `SupportsId` с read-only свойством `id: int` (можно через `@property` в протоколе не требуется — достаточно атрибута в реализации).
3. Класс `InMemoryRepository(Generic[T])` с методами `get(entity_id: int) -> T | None`, `save(entity: T) -> None` — хранит в `dict[int, T]`.
4. Две сущности: `User(Entity)` и `Item(Entity)` — разные поля кроме `id`.

**Проверка mypy (после `pip install mypy` — опционально для студента; в автономном режиме достаточно аннотаций):**

```bash
python -m mypy solution.py --strict
```

Если `mypy` не установлен — задание всё равно считается выполненным при корректных аннотациях и прохождении assert ниже.

## ✅ Как проверить

```bash
cd tasks/task_07_typed_protocol_repository
python -c "
from solution import User, Item, InMemoryRepository

ur = InMemoryRepository[User]()
ir = InMemoryRepository[Item]()
u = User(id=1, name='a')
ur.save(u)
assert ur.get(1) is u

it = Item(id=2, sku='x')
ir.save(it)
assert ir.get(2).sku == 'x'
print('OK')
"
```

## 💡 Подсказки и ограничения

- **Не использовать** `Any` для сущностей без необходимости.
- **Акцент:** `InMemoryRepository[User]` не должен принимать `Item` в `save` — это ловит mypy.
- **Типичная ошибка:** забыть `from __future__ import annotations` в старых версиях — при необходимости добавьте в начало файла.
