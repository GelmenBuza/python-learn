# Задание: Декораторы и functools

## 🎯 Цель и краткое описание

Собрать **цепочку декораторов** с сохранением метаданных функции, **замыкания** для конфигурации и применение **`functools`**.

## 📚 Темы для изучения/повторения

- `functools.wraps` — сохранение `__name__` и docstring
- `functools.lru_cache` — как контраст к своему простому кэшу (в задании — свой упрощённый)
- Замыкания: фабрика декораторов с параметрами
- Порядок применения декораторов (снизу вверх при объявлении)

## 📝 ТЗ

**Реализовать:**

1. Декоратор `retry(times: int)` — при исключении повторить вызов не более `times` раз (первая попытка + `times` повторов = всего `times + 1` вызовов). Если все неудачны — пробросить последнее исключение. Использовать `functools.wraps`.
2. Декоратор `log_calls(prefix: str)` — перед каждым вызовом писать в переданный `sink: Callable[[str], None]` строку `"{prefix}:{func_name}"`. По умолчанию `sink=print`.
3. Функцию `compose(*decorators)` — принимает декораторы **без аргументов** (уже частично применённые, например через `functools.partial`) и возвращает один декоратор, эквивалентный применению снизу вверх как при `@d1 @d2` к функции.

**Требования:**

- Разрешены: `functools`, `typing`.
- Файл: `solution.py`.

## ✅ Как проверить

```bash
cd tasks/task_03_decorator_pipeline
python -c "
from functools import partial
from solution import retry, log_calls, compose

calls = []
def sink(msg):
    calls.append(msg)

@retry(times=2)
def flaky():
    flaky.n += 1
    if flaky.n < 3:
        raise RuntimeError('x')
    return 'ok'
flaky.n = 0
assert flaky() == 'ok'

@log_calls('T', sink=sink)
def f():
    return 1
f()
assert any('T' in c and 'f' in c for c in calls)

d = compose(partial(log_calls, 'A', sink=sink), partial(retry, times=0))
@d
def g():
    return 2
assert g() == 2
print('OK')
"
```

## 💡 Подсказки и ограничения

- **Не забывать** `wraps` — иначе `compose` и тесты на имя функции ломаются.
- **Акцент:** `retry` считает попытки предсказуемо (зафиксируйте семантику в комментарии в 1 строку).
- **Типичная ошибка:** бесконечная рекурсия в `compose` из-за неправильного порядка — проверьте на простых `lambda: None`.
