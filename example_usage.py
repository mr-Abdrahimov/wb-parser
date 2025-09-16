#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примеры использования WB Parser
"""

from wb_parser import WBParser


def example_basic_search():
    """Базовый пример поиска"""
    parser = WBParser()
    
    query = "куртка женская черная"
    product_ids = parser.search_products(query)
    
    print(f"Поиск: '{query}'")
    print(f"Найдено ID: {product_ids}")
    print(f"Количество: {len(product_ids)}")
    print("-" * 50)


def example_multiple_pages():
    """Пример поиска по нескольким страницам"""
    parser = WBParser()
    
    query = "iPhone"
    all_ids = []
    
    # Получаем первые 3 страницы
    for page in range(1, 4):
        print(f"Загружаем страницу {page}...")
        product_ids = parser.search_products(query, page)
        all_ids.extend(product_ids)
        
        if not product_ids:  # Если на странице нет товаров, прекращаем
            break
    
    print(f"\nВсего ID собрано: {len(all_ids)}")
    print(f"Уникальных ID: {len(set(all_ids))}")


def example_different_queries():
    """Пример поиска по разным запросам"""
    parser = WBParser()
    
    queries = [
        "телефон Samsung",
        "кроссовки Nike",
        "платье летнее",
        "рюкзак школьный"
    ]
    
    for query in queries:
        product_ids = parser.search_products(query)
        total = parser.get_total_products(query)
        
        print(f"Запрос: '{query}'")
        print(f"Всего товаров: {total}")
        print(f"ID на первой странице: {len(product_ids)}")
        if product_ids:
            print(f"Первые 3 ID: {product_ids[:3]}")
        print("-" * 30)


def example_save_to_file():
    """Пример сохранения результатов в файл"""
    parser = WBParser()
    
    query = "ноутбук"
    product_ids = parser.search_products(query)
    
    # Сохраняем в файл
    filename = f"products_{query.replace(' ', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Поисковый запрос: {query}\n")
        f.write(f"Найдено товаров: {len(product_ids)}\n")
        f.write("ID товаров:\n")
        for product_id in product_ids:
            f.write(f"{product_id}\n")
    
    print(f"Результаты сохранены в файл: {filename}")


if __name__ == "__main__":
    print("=== Примеры использования WB Parser ===\n")
    
    print("1. Базовый поиск:")
    example_basic_search()
    
    print("\n2. Поиск по нескольким страницам:")
    example_multiple_pages()
    
    print("\n3. Разные поисковые запросы:")
    example_different_queries()
    
    print("\n4. Сохранение в файл:")
    example_save_to_file()
