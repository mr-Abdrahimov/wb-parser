#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интерактивный парсер WildBerries
Позволяет вводить запросы и получать результаты в реальном времени
"""

from wb_parser import WBParser
import sys


def print_separator():
    """Печатает разделитель"""
    print("=" * 60)


def print_results(query, product_ids, total_products):
    """
    Выводит результаты поиска в красивом формате
    
    Args:
        query: Поисковый запрос
        product_ids: Список ID продуктов
        total_products: Общее количество продуктов
    """
    print_separator()
    print(f"🔍 Запрос: '{query}'")
    print(f"📊 Всего найдено товаров: {total_products}")
    print(f"📋 ID на первой странице: {len(product_ids)}")
    
    if product_ids:
        print("\n📦 Список ID продуктов:")
        # Выводим по 5 ID в строке для компактности
        for i in range(0, len(product_ids), 5):
            row = product_ids[i:i+5]
            print("   " + " | ".join(f"{pid:>9}" for pid in row))
    else:
        print("\n❌ Товары не найдены")
    
    print_separator()


def save_results_interactive(query, product_ids):
    """
    Интерактивное сохранение результатов
    
    Args:
        query: Поисковый запрос
        product_ids: Список ID продуктов
    """
    save = input("\n💾 Сохранить результаты в файл? (y/n): ").strip().lower()
    
    if save in ['y', 'yes', 'да', 'д']:
        filename = f"wb_results_{query.replace(' ', '_').replace('/', '_')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"WildBerries Parser Results\n")
                f.write(f"Запрос: {query}\n")
                f.write(f"Количество ID: {len(product_ids)}\n")
                f.write(f"Дата: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n")
                
                for i, product_id in enumerate(product_ids, 1):
                    f.write(f"{i:3d}. {product_id}\n")
            
            print(f"✅ Результаты сохранены в файл: {filename}")
            
        except Exception as e:
            print(f"❌ Ошибка при сохранении: {e}")


def main():
    """Основная функция интерактивного парсера"""
    parser = WBParser()
    
    print("🛍️  WildBerries Interactive Parser")
    print("Интерактивный парсер товаров с WildBerries")
    print_separator()
    print("Введите поисковый запрос или 'exit' для выхода")
    print("Примеры запросов: 'iPhone', 'куртка женская', 'кроссовки Nike'")
    print_separator()
    
    while True:
        try:
            # Получаем запрос от пользователя
            query = input("\n🔍 Введите запрос: ").strip()
            
            # Проверяем команды выхода
            if query.lower() in ['exit', 'quit', 'выход', 'выйти', 'q']:
                print("👋 До свидания!")
                break
            
            # Проверяем пустой запрос
            if not query:
                print("❌ Пустой запрос. Попробуйте еще раз.")
                continue
            
            print(f"\n⏳ Выполняется поиск по запросу: '{query}'...")
            
            # Выполняем поиск
            product_ids = parser.search_products(query)
            total_products = parser.get_total_products(query)
            
            # Выводим результаты
            print_results(query, product_ids, total_products)
            
            # Предлагаем сохранить результаты
            if product_ids:
                save_results_interactive(query, product_ids)
            
            # Предлагаем продолжить
            print("\n" + "─" * 60)
            continue_search = input("🔄 Выполнить еще один поиск? (y/n): ").strip().lower()
            
            if continue_search not in ['y', 'yes', 'да', 'д', '']:
                print("👋 До свидания!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Программа прервана пользователем. До свидания!")
            sys.exit(0)
            
        except Exception as e:
            print(f"\n❌ Произошла ошибка: {e}")
            print("Попробуйте еще раз.")


if __name__ == "__main__":
    main()
