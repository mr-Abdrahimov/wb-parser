#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест CLI функциональности WB Parser
"""

import subprocess
import sys
import json
import os


def run_cli_command(args):
    """Запускает CLI команду и возвращает результат"""
    cmd = [sys.executable, "wb_cli.py"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"


def test_basic_search():
    """Тест базового поиска"""
    print("🧪 Тест базового поиска...")
    returncode, stdout, stderr = run_cli_command(["-q", "тест"])
    
    if returncode == 0 and "📦 Всего получено" in stdout:
        print("✅ Базовый поиск работает")
        return True
    else:
        print(f"❌ Базовый поиск не работает: {stderr}")
        return False


def test_json_format():
    """Тест JSON формата"""
    print("🧪 Тест JSON формата...")
    returncode, stdout, stderr = run_cli_command(["-q", "тест", "--quiet", "--format", "json"])
    
    if returncode == 0:
        try:
            # Пытаемся парсить весь вывод как JSON
            json_data = json.loads(stdout.strip())
            
            # Проверяем структуру JSON
            if (isinstance(json_data, dict) and 
                'query' in json_data and 
                'count' in json_data and 
                'product_ids' in json_data and
                isinstance(json_data['product_ids'], list)):
                print("✅ JSON формат работает")
                return True
            else:
                print("❌ JSON структура неверная")
                return False
        except json.JSONDecodeError as e:
            print(f"❌ Невалидный JSON: {e}")
            return False
    else:
        print(f"❌ JSON формат не работает: {stderr}")
        return False


def test_save_file():
    """Тест сохранения в файл"""
    print("🧪 Тест сохранения в файл...")
    test_file = "test_output.txt"
    
    # Удаляем файл если существует
    if os.path.exists(test_file):
        os.remove(test_file)
    
    returncode, stdout, stderr = run_cli_command(["-q", "тест", "--save", test_file])
    
    if returncode == 0 and os.path.exists(test_file):
        print("✅ Сохранение в файл работает")
        os.remove(test_file)  # Очищаем
        return True
    else:
        print(f"❌ Сохранение в файл не работает: {stderr}")
        return False


def test_help():
    """Тест справки"""
    print("🧪 Тест справки...")
    returncode, stdout, stderr = run_cli_command(["--help"])
    
    if returncode == 0 and "usage:" in stdout:
        print("✅ Справка работает")
        return True
    else:
        print(f"❌ Справка не работает: {stderr}")
        return False


def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование CLI функциональности")
    print("=" * 50)
    
    tests = [
        test_help,
        test_basic_search,
        test_json_format,
        test_save_file
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
        return True
    else:
        print("⚠️  Некоторые тесты не прошли")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
