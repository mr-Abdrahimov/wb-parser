#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест Mayak API функциональности
"""

from mayak_api import MayakAPI, parse_cookies_string


def test_cookies_parsing():
    """Тест парсинга cookies"""
    print("🧪 Тест парсинга cookies...")
    
    cookies_str = "cookie1=value1; cookie2=value2; cookie3=value3"
    parsed = parse_cookies_string(cookies_str)
    
    expected = {
        'cookie1': 'value1',
        'cookie2': 'value2', 
        'cookie3': 'value3'
    }
    
    if parsed == expected:
        print("✅ Парсинг cookies работает")
        return True
    else:
        print(f"❌ Парсинг cookies не работает. Ожидалось: {expected}, получено: {parsed}")
        return False


def test_codes_splitting():
    """Тест разбиения кодов на чанки"""
    print("🧪 Тест разбиения кодов на чанки...")
    
    api = MayakAPI()
    codes = list(range(1, 51))  # 50 кодов
    
    chunks = api.split_codes_to_chunks(codes, 20)
    
    if len(chunks) == 3 and len(chunks[0]) == 20 and len(chunks[1]) == 20 and len(chunks[2]) == 10:
        print("✅ Разбиение кодов работает")
        return True
    else:
        print(f"❌ Разбиение кодов не работает. Получено {len(chunks)} чанков")
        return False


def test_mayak_api_init():
    """Тест инициализации Mayak API"""
    print("🧪 Тест инициализации Mayak API...")
    
    try:
        # Тест с cookies строкой
        cookies_str = "test_cookie=test_value"
        api1 = MayakAPI(cookies_str)
        
        # Тест с cookies словарем
        cookies_dict = {"test_cookie": "test_value"}
        api2 = MayakAPI(cookies_dict)
        
        # Тест без cookies
        api3 = MayakAPI()
        
        print("✅ Инициализация Mayak API работает")
        return True
    except Exception as e:
        print(f"❌ Инициализация Mayak API не работает: {e}")
        return False


def test_api_request_structure():
    """Тест структуры запроса к API (без реального запроса)"""
    print("🧪 Тест структуры запроса к API...")
    
    try:
        api = MayakAPI()
        
        # Проверяем что URL формируется правильно
        base_url = api.BASE_URL
        endpoint = api.PRODUCTS_ENDPOINT
        max_codes = api.MAX_CODES_PER_REQUEST
        
        if (base_url == "https://app.mayak.bz/api/v1/" and 
            endpoint == "wb/products" and 
            max_codes == 20):
            print("✅ Структура API запроса корректная")
            return True
        else:
            print("❌ Структура API запроса некорректная")
            return False
    except Exception as e:
        print(f"❌ Ошибка в структуре API: {e}")
        return False


def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование Mayak API функциональности")
    print("=" * 50)
    
    tests = [
        test_cookies_parsing,
        test_codes_splitting,
        test_mayak_api_init,
        test_api_request_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно!")
        print("\n💡 Примечание: Реальные запросы к Mayak API требуют валидных cookies")
        return True
    else:
        print("⚠️  Некоторые тесты не прошли")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
