# WildBerries Parser

Программа для парсинга товаров с WildBerries через их API и извлечения ID продуктов.

## Возможности

### Базовая функциональность
- Поиск товаров по любому запросу
- Получение списка ID всех найденных продуктов
- Поддержка пагинации (поиск по страницам)
- Получение общего количества найденных товаров
- Обработка ошибок и логирование

### Расширенная функциональность (NEW!)
- **Получение подробной информации о товарах** через Mayak API
- **Автоматическое разбиение** больших списков ID на чанки по 20 штук
- **Поддержка cookies** для авторизованных запросов
- **Сортировка товаров по продажам** (от большего к меньшему)
- **Красивое табличное отображение** с данными о продажах, выручке и ценах
- **Полнофункциональный CLI** с множеством опций
- **Работа с конкретными ID** товаров
- **Различные форматы вывода**: JSON, CSV, список, таблица

## Установка

1. Клонируйте репозиторий или скачайте файлы
2. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Использование

### Базовое использование

```python
from wb_parser import WBParser

parser = WBParser()

# Поиск по запросу
query = "куртка женская черная"
product_ids = parser.search_products(query)

print(f"Найдено {len(product_ids)} товаров")
print("ID товаров:", product_ids)
```

### Запуск основного скрипта

```bash
python3 wb_parser.py
```

### Запуск примеров

```bash
python3 example_usage.py
```

### Интерактивный режим

```bash
python3 interactive_parser.py
```

Интерактивный режим позволяет вводить запросы в реальном времени и сохранять результаты.

### CLI режим (командная строка)

```bash
# Базовое использование
python3 wb_cli.py -q "куртка женская черная"

# С показом общего количества
python3 wb_cli.py -q "iPhone" --total

# Загрузка нескольких страниц
python3 wb_cli.py -q "телефон" --pages 3

# Сохранение в файл
python3 wb_cli.py -q "ноутбук" --save

# JSON формат
python3 wb_cli.py -q "кроссовки" --format json

# CSV формат с сохранением
python3 wb_cli.py -q "платье" --format csv --save

# Тихий режим (только результаты)
python3 wb_cli.py -q "часы" --quiet
```

### Полнофункциональный CLI (с подробной информацией)

```bash
# Базовый поиск ID
python3 wb_full_cli.py -q "куртка женская черная"

# Поиск с подробной информацией (требуются cookies)
python3 wb_full_cli.py -q "iPhone" --detailed --cookies-file cookies.txt

# Подробная информация для конкретных ID
python3 wb_full_cli.py --ids "306897066,164105063,244733060" --detailed --cookies "session=..."

# Сохранение подробной информации
python3 wb_full_cli.py -q "телефон" --detailed --save results.json --cookies-file cookies.txt

# Ограничение количества товаров
python3 wb_full_cli.py -q "ноутбук" --detailed --max-products 10 --cookies-file cookies.txt

# Показ товаров в виде таблицы, отсортированной по продажам
python3 wb_full_cli.py -q "iPhone" --detailed --show-table --cookies-file cookies.txt

# Анализ конкретных товаров с таблицей продаж
python3 wb_full_cli.py --ids "306897066,164105063,244733060" --detailed --show-table --cookies-file cookies.txt
```

## CLI Параметры

### Основные опции

- `-q, --query` - Поисковый запрос (обязательный)
- `-p, --page` - Номер страницы (по умолчанию: 1)
- `--pages` - Количество страниц для загрузки (с 1 по указанную)
- `-s, --save` - Сохранить в файл (автоматическое имя или указанное)
- `--total` - Показать общее количество товаров
- `--quiet` - Тихий режим (только результаты)
- `--format` - Формат вывода: list, json, csv

### Примеры CLI команд

```bash
# Справка
python3 wb_cli.py --help

# Простой поиск
python3 wb_cli.py -q "куртка женская черная"

# Поиск с общим количеством
python3 wb_cli.py -q "iPhone" --total

# Загрузка 3 страниц
python3 wb_cli.py -q "телефон" --pages 3

# Сохранение в JSON
python3 wb_cli.py -q "ноутбук" --format json --save

# Тихий режим с CSV
python3 wb_cli.py -q "кроссовки" --quiet --format csv
```

## API класса WBParser

### Методы

- `search_products(query, page=1)` - поиск товаров по запросу
- `get_total_products(query)` - получение общего количества найденных товаров
- `build_url(query, page=1)` - формирование URL для запроса
- `fetch_data(url)` - выполнение HTTP запроса
- `extract_product_ids(data)` - извлечение ID из JSON ответа

### Параметры

- `query` - поисковый запрос (например, "телефон Samsung")
- `page` - номер страницы (по умолчанию 1)

## Примеры запросов

- "куртка женская черная"
- "телефон iPhone"
- "кроссовки Nike"
- "ноутбук ASUS"
- "платье летнее"

## Структура проекта

```
wb-parser/
├── wb_parser.py           # Основной модуль парсера
├── mayak_api.py          # Модуль для работы с Mayak API
├── wb_cli.py             # Простой CLI с аргументами командной строки
├── wb_full_cli.py        # Полнофункциональный CLI с Mayak API
├── example_usage.py       # Примеры базового использования
├── example_detailed.py   # Примеры с подробной информацией
├── interactive_parser.py  # Интерактивный парсер
├── test_parser.py         # Тесты базовой функциональности
├── test_cli.py           # Тесты CLI
├── test_mayak.py         # Тесты Mayak API
├── cookies_example.txt   # Пример файла с cookies
├── requirements.txt       # Зависимости
└── README.md             # Документация
```

## Работа с подробной информацией (Mayak API)

### Получение cookies

1. Откройте https://app.mayak.bz в браузере
2. Авторизуйтесь в системе
3. Откройте инструменты разработчика (F12)
4. Перейдите на вкладку Network/Сеть
5. Обновите страницу
6. Найдите любой запрос к app.mayak.bz
7. Скопируйте значение заголовка Cookie

### Использование в коде

```python
from wb_parser import WBParser

# Инициализация с cookies
cookies = "session_id=...; user_token=..."
parser = WBParser(mayak_cookies=cookies)

# Поиск с подробной информацией
result = parser.search_and_get_detailed_info("iPhone", max_products=10)

# Подробная информация для конкретных ID
product_ids = [306897066, 164105063, 244733060]
detailed_info = parser.get_products_detailed_info(product_ids)
```

### Использование в CLI

```bash
# Сохранение cookies в файл
echo "ваши_cookies_здесь" > cookies.txt

# Использование
python3 wb_full_cli.py -q "iPhone" --detailed --cookies-file cookies.txt
```

### Формат данных Mayak API

Mayak API возвращает данные в следующем формате:

```json
{
  "64775386": {
    "sales": 7193,
    "revenue": 19747579,
    "lost_revenue": 11161879,
    "avg_price": 2689
  }
}
```

Где:
- `64775386` - ID товара с WildBerries
- `sales` - количество продаж
- `revenue` - выручка в копейках
- `lost_revenue` - упущенная выручка в копейках  
- `avg_price` - средняя цена в копейках

Парсер автоматически:
- Преобразует данные в удобный формат списка
- Сортирует товары по количеству продаж (от большего к меньшему)
- Отображает результаты в красивой таблице

## Особенности

- Использует официальный API WildBerries
- Интегрируется с Mayak API для подробной информации
- Имитирует запросы браузера для стабильной работы
- Поддерживает кодировку URL для русских запросов
- Автоматически разбивает большие списки на чанки
- Включает подробное логирование для отладки
- Обрабатывает ошибки сети и парсинга JSON

## Ограничения

- Базовый парсер получает только ID товаров
- Для подробной информации нужны действующие cookies от mayak.bz
- Максимум 20 товаров за один запрос к Mayak API
- Соблюдайте разумные интервалы между запросами

## Лицензия

MIT License
