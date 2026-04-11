# Задание: asyncio — очередь и задачи

## 🎯 Цель и краткое описание

Смоделировать конвейер **worker**-ов через `asyncio.Queue`, **`create_task`** и координацию завершения без внешних сетевых зависимостей.

## 📚 Темы для изучения/повторения

- `async`/`await`, создание задач `asyncio.create_task`
- `asyncio.Queue`, потребители и производители (паттерн producer-consumer)
- `asyncio.wait_for` или таймауты для отмены «зависших» задач (по желанию)
- Корректное завершение: `queue.join`, `sentinel` для остановки воркеров

## 📝 ТЗ

**Реализовать в `solution.py`:**

1. Асинхронная функция `async_worker(name: str, q: asyncio.Queue, results: list, lock: asyncio.Lock)` — в цикле забирает элементы `int` из очереди; пока не получен `None` (sentinel): кладёт в `results` строку `"{name}:{value}"` под `lock`; при `None` — выходит.
2. `async def run_pipeline(n_workers: int, items: list[int]) -> list[str]` — создаёт очередь, кладёт все `items`, затем `n_workers` раз кладёт `None`, запускает `n_workers` воркеров с именами `w0..w{n-1}`, ждёт завершения, возвращает **отсортированный** список результатов (чтобы тест был детерминированным).

**Требования:**

- Только `asyncio` + стандартная библиотека.
- Не использовать `threading`/`multiprocessing` для логики задания.

## ✅ Как проверить

```bash
cd tasks/task_05_async_worker_queue
python -c "
import asyncio
from solution import run_pipeline

async def main():
    r = await run_pipeline(2, [1, 2, 3])
    assert len(r) == 3
    nums = sorted(int(s.split(':', 1)[1]) for s in r)
    assert nums == [1, 2, 3]
    assert all(s.startswith(('w0:', 'w1:')) for s in r)

asyncio.run(main())
print('OK')
"
```

## 💡 Подсказки и ограничения

- **Не блокировать** event loop синхронными `time.sleep` — только `asyncio.sleep` при необходимости.
- **Акцент:** каждый элемент из `items` обрабатывается ровно одним воркером; в результате ровно `len(items)` строк.
- **Типичная ошибка:** неверное число sentinel-значений — воркеры «висят» или завершаются раньше времени.
