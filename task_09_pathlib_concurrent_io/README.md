# Задание: pathlib, JSON и concurrent.futures

## 🎯 Цель и краткое описание

Обойти дерево каталогов, собрать метаданные в **JSON**, ускорить обработку **пулом потоков** (I/O-bound), без сторонних HTTP-клиентов.

## 📚 Темы для изучения/повторения

- `pathlib.Path.rglob`, фильтрация по суффиксу
- `json` — сериализация списков словарей
- `concurrent.futures.ThreadPoolExecutor` — параллельное чтение маленьких файлов
- Кодировка UTF-8, обработка ошибок чтения (пропуск или запись в отчёт)

## 📝 ТЗ

**Реализовать в `solution.py`:**

1. `scan_txt(root: Path) -> list[dict]` — рекурсивно находит файлы `*.txt` под `root`, для каждого возвращает `{"path": str posix, "lines": int, "chars": int}` (число строк и символов содержимого файла).
2. `scan_parallel(root: Path, max_workers: int = 4) -> list[dict]` — то же, но подсчёт для каждого файла выполняется в `ThreadPoolExecutor` (одна задача — один файл).
3. `write_report(out: Path, data: list[dict]) -> None` — записывает JSON с `ensure_ascii=False` и отступом 2.

**Требования:**

- Только стандартная библиотека.
- При ошибке чтения файла — пропустить файл и добавить `{"path": "...", "error": "<сообщение>"}` без полей `lines`/`chars`.

## ✅ Как проверить

```bash
cd tasks/task_09_pathlib_concurrent_io
python -c "
import tempfile
from pathlib import Path
from solution import scan_txt, scan_parallel, write_report

with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    (root / 'a').mkdir()
    (root / 'a' / 'f.txt').write_text('line1\nline2\n', encoding='utf-8')
    (root / 'b.txt').write_text('x', encoding='utf-8')
    s = sorted(scan_txt(root), key=lambda x: x['path'])
    assert len(s) == 2
    p = sorted(scan_parallel(root), key=lambda x: x['path'])
    assert len(p) == 2
    write_report(root / 'out.json', s)
    assert (root / 'out.json').read_text(encoding='utf-8').strip().startswith('[')
print('OK')
"
```

## 💡 Подсказки и ограничения

- **Не использовать** `httpx`/`requests` — задание про ФС.
- **Акцент:** не смешивать порядок — сортируйте по `path` для сравнения в тестах.
- **Типичная ошибка:** передать в executor не picklable — для потоков достаточно замыкания с `Path`.
