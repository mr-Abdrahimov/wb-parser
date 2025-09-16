#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mayak API Client
Модуль для работы с API mayak.bz для получения подробной информации о товарах WB
"""

import requests
import json
from typing import List, Dict, Any, Optional, Union
import logging
from urllib.parse import urljoin


logger = logging.getLogger(__name__)


class MayakAPI:
    """Класс для работы с API Mayak"""
    
    BASE_URL = "https://app.mayak.bz/api/v1/"
    PRODUCTS_ENDPOINT = "wb/products"
    MAX_CODES_PER_REQUEST = 20
    
    def __init__(self, cookies: Optional[Union[str, Dict[str, str]]] = None):
        """
        Инициализация клиента Mayak API
        
        Args:
            cookies: Cookies в виде строки или словаря
        """
        self.session = requests.Session()
        
        # Настройка заголовков
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://app.mayak.bz/',
        })
        
        # Установка cookies
        if cookies:
            self.set_cookies(cookies)
    
    def set_cookies(self, cookies: Union[str, Dict[str, str]]):
        """
        Установка cookies для запросов
        
        Args:
            cookies: Cookies в виде строки или словаря
        """
        if isinstance(cookies, str):
            # Парсим строку cookies
            cookie_pairs = []
            for cookie in cookies.split(';'):
                cookie = cookie.strip()
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookie_pairs.append((name.strip(), value.strip()))
            
            for name, value in cookie_pairs:
                self.session.cookies.set(name, value)
                
        elif isinstance(cookies, dict):
            for name, value in cookies.items():
                self.session.cookies.set(name, value)
        
        logger.info(f"Установлено {len(self.session.cookies)} cookies")
    
    def split_codes_to_chunks(self, codes: List[Union[int, str]], chunk_size: int = None) -> List[List[str]]:
        """
        Разбивает список кодов на чанки
        
        Args:
            codes: Список кодов товаров
            chunk_size: Размер чанка (по умолчанию MAX_CODES_PER_REQUEST)
            
        Returns:
            Список чанков с кодами
        """
        if chunk_size is None:
            chunk_size = self.MAX_CODES_PER_REQUEST
        
        # Преобразуем все коды в строки
        str_codes = [str(code) for code in codes]
        
        chunks = []
        for i in range(0, len(str_codes), chunk_size):
            chunks.append(str_codes[i:i + chunk_size])
        
        logger.info(f"Разбито {len(str_codes)} кодов на {len(chunks)} чанков")
        return chunks
    
    def get_products_info(self, codes: List[Union[int, str]]) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о товарах по их кодам
        
        Args:
            codes: Список кодов товаров (максимум 20)
            
        Returns:
            Словарь с информацией о товарах или None в случае ошибки
        """
        if len(codes) > self.MAX_CODES_PER_REQUEST:
            logger.warning(f"Передано {len(codes)} кодов, максимум {self.MAX_CODES_PER_REQUEST}")
            codes = codes[:self.MAX_CODES_PER_REQUEST]
        
        # Преобразуем коды в строки и объединяем через запятую
        codes_str = ','.join(str(code) for code in codes)
        
        url = urljoin(self.BASE_URL, self.PRODUCTS_ENDPOINT)
        params = {'codes': codes_str}
        
        try:
            logger.info(f"Запрос к Mayak API: {url}?codes={codes_str[:100]}{'...' if len(codes_str) > 100 else ''}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Получен ответ от Mayak API, размер: {len(response.text)} символов")
            
            # Преобразуем данные в более удобный формат
            if isinstance(data, dict):
                products_list = []
                for product_id, product_data in data.items():
                    if isinstance(product_data, dict):
                        # Добавляем ID к данным товара
                        product_info = product_data.copy()
                        product_info['id'] = product_id
                        products_list.append(product_info)
                
                logger.info(f"Преобразовано {len(products_list)} товаров в список")
                return products_list
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к Mayak API: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка при парсинге JSON от Mayak API: {e}")
            return None
    
    def get_all_products_info(self, codes: List[Union[int, str]]) -> List[Dict[str, Any]]:
        """
        Получает информацию о всех товарах, разбивая на чанки при необходимости
        
        Args:
            codes: Список кодов товаров
            
        Returns:
            Список с информацией о всех товарах
        """
        all_products = []
        chunks = self.split_codes_to_chunks(codes)
        
        for i, chunk in enumerate(chunks, 1):
            logger.info(f"Обрабатывается чанк {i}/{len(chunks)} ({len(chunk)} кодов)")
            
            chunk_data = self.get_products_info(chunk)
            if chunk_data:
                # Предполагаем, что API возвращает список товаров
                if isinstance(chunk_data, list):
                    all_products.extend(chunk_data)
                elif isinstance(chunk_data, dict):
                    # Если возвращается словарь, ищем список товаров
                    if 'products' in chunk_data:
                        all_products.extend(chunk_data['products'])
                    elif 'data' in chunk_data:
                        all_products.extend(chunk_data['data'])
                    else:
                        all_products.append(chunk_data)
        
        logger.info(f"Получена информация о {len(all_products)} товарах")
        return all_products
    
    def save_products_info(self, products: List[Dict[str, Any]], filename: str, format_type: str = 'json'):
        """
        Сохраняет информацию о товарах в файл
        
        Args:
            products: Список товаров
            filename: Имя файла
            format_type: Формат файла (json, csv)
        """
        try:
            if format_type == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(products, f, ensure_ascii=False, indent=2)
            
            elif format_type == 'csv':
                import csv
                if not products:
                    return
                
                # Получаем все возможные ключи
                all_keys = set()
                for product in products:
                    if isinstance(product, dict):
                        all_keys.update(product.keys())
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
                    writer.writeheader()
                    
                    for product in products:
                        if isinstance(product, dict):
                            writer.writerow(product)
            
            logger.info(f"Информация о товарах сохранена в файл: {filename}")
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении в файл {filename}: {e}")

    def sort_products_by_sales(self, products: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Сортирует товары по количеству продаж
        
        Args:
            products: Список товаров с данными
            reverse: True для сортировки от большего к меньшему (по умолчанию)
            
        Returns:
            Отсортированный список товаров
        """
        try:
            sorted_products = sorted(
                products,
                key=lambda x: x.get('sales', 0),
                reverse=reverse
            )
            
            logger.info(f"Отсортировано {len(sorted_products)} товаров по продажам ({'убывание' if reverse else 'возрастание'})")
            return sorted_products
            
        except Exception as e:
            logger.error(f"Ошибка при сортировке товаров: {e}")
            return products
    
    def format_products_table(self, products: List[Dict[str, Any]], limit: int = None) -> str:
        """
        Форматирует список товаров в виде таблицы
        
        Args:
            products: Список товаров
            limit: Ограничение количества товаров для вывода
            
        Returns:
            Форматированная таблица
        """
        if not products:
            return "Нет данных о товарах"
        
        # Ограничиваем количество если указано
        display_products = products[:limit] if limit else products
        
        lines = []
        lines.append("📊 ТОВАРЫ ПО ПРОДАЖАМ")
        lines.append("=" * 95)
        lines.append(f"{'№':>3} | {'ID товара':>10} | {'Продажи':>8} | {'Выручка':>12} | {'Средняя цена':>12} | {'Фото':>5}")
        lines.append("-" * 95)
        
        for i, product in enumerate(display_products, 1):
            product_id = product.get('id', 'N/A')
            sales = product.get('sales', 0)
            revenue = product.get('revenue', 0)
            avg_price = product.get('avg_price', 0)
            lost_revenue = product.get('lost_revenue', 0)
            pics = product.get('pics', 0)
            
            lines.append(f"{i:>3} | {product_id:>10} | {sales:>8,} | {revenue:>12,} | {avg_price:>12,} | {pics:>5}")
        
        if limit and len(products) > limit:
            lines.append("-" * 95)
            lines.append(f"... и еще {len(products) - limit} товаров")
        
        lines.append("=" * 95)
        lines.append(f"Всего товаров: {len(products)}")
        
        return '\n'.join(lines)


def parse_cookies_string(cookies_string: str) -> Dict[str, str]:
    """
    Парсит строку cookies в словарь
    
    Args:
        cookies_string: Строка с cookies
        
    Returns:
        Словарь cookies
    """
    cookies = {}
    for cookie in cookies_string.split(';'):
        cookie = cookie.strip()
        if '=' in cookie:
            name, value = cookie.split('=', 1)
            cookies[name.strip()] = value.strip()
    return cookies
