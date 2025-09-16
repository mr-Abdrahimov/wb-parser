#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тест парсера WildBerries
"""

from wb_parser import WBParser

def test_basic_functionality():
    """Тестирует базовую функциональность парсера"""
    parser = WBParser()
    
    # Тест с простым запросом
    query = "телефон"
    print(f"Тестируем запрос: '{query}'")
    
    product_ids = parser.search_products(query)
    total = parser.get_total_products(query)
    
    print(f"Результат: найдено {len(product_ids)} ID на первой странице")
    print(f"Общее количество товаров: {total}")
    
    if product_ids:
        print("✅ Тест пройден - получены ID продуктов")
        print(f"Первые 5 ID: {product_ids[:5]}")
    else:
        print("❌ Тест не пройден - ID не получены")
    
    return len(product_ids) > 0

if __name__ == "__main__":
    print("🧪 Тестирование WB Parser")
    print("=" * 40)
    
    success = test_basic_functionality()
    
    print("=" * 40)
    if success:
        print("✅ Все тесты пройдены успешно!")
    else:
        print("❌ Тесты не пройдены")
