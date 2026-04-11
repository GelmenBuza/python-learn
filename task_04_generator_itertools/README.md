# Задание: Генераторы и itertools

## 🎯 Цель и краткое описание

Построить **ленивые конвейеры** на генераторах и стандартных приёмах **`itertools`** без загрузки всего объёма в память.

## 📚 Темы для изучения/повторения

- Генераторы: `yield`, делегирование `yield from`
- Итераторы как протокол; преимущество ленивости для больших последовательностей
- `itertools.islice`, `chain`, `groupby` (с предварительной сортировкой для `groupby`)
- Ограничение памяти: не материализовать весь файл в список

## 📝 ТЗ

**Реализовать в `solution.py`:**

1. `read_numbers(path: Path) -> Iterator[int]` — читает текстовый файл построчно; пустые строки и строки с `#` в начале пропускать; остальное парсить как целое (`ValueError` на битой строке пробрасывать).
2. `batched(iterable, n: int)` — генератор групп по `n` элементов; последняя группа может быть короче **только если** данных не хватает (не падать на пустом вводе — ничего не выдавать).
3. `run_length_encode(sorted_iterable: Iterable[int]) -> Iterator[tuple[int, int]]` — для **уже отсортированной** последовательности выдаёт пары `(значение, сколько подряд)`. Пустой ввод — пустой результат.

**Требования:**

- `pathlib.Path`, `itertools`, `typing`.
- Без сторонних библиотек.

## ✅ Как проверить

Создайте временный файл в скрипте или используйте `tempfile`:

```bash
cd tasks/task_04_generator_itertools
python -c "
from pathlib import Path
import tempfile
from solution import read_numbers, batched, run_length_encode

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / 't.txt'
    p.write_text('1\n#skip\n2\n\n3\n', encoding='utf-8')
    assert list(read_numbers(p)) == [1, 2, 3]

assert list(batched(range(5), 2)) == [(0,1),(2,3),(4,)]
assert list(run_length_encode([1,1,1,2,2])) == [(1,3),(2,2)]
print('OK')
"
```

## 💡 Подсказки и ограничения

- **Не загружать** весь файл через `read_text().splitlines()` если в ТЗ подразумевается поток — используйте построчное чтение.
- **Акцент:** `groupby` из itertools здесь **не обязателен** для RLE — можно один проход вручную; если используете `groupby`, помните про сортировку.
- **Типичная ошибка:** `batched` с `itertools.batched` — в старых Python его нет; реализуйте сами или через `islice` циклом.
