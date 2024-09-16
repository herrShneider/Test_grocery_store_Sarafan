# Test_grocery_store_Sarafan

 Тестовый проект магазина продуктов.

Техническое задание находится в файле:
```
Terms of Reference
```
Решение задачи №1 находиться в файле:
```
Task_1_solution.py
```

Стэк: Python 3.9.10 / Django 3.2.16 / DRF 3.12.4 / Djoser 2.1.0


Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:herrShneider/Test_grocery_store_Sarafan.git
```
```
cd Test_grocery_store_Sarafan/
```
Создать файл .env по образцу .env.example

Создать виртуальное окружение:
Для Windows:
```
python -m venv venv
```
Для Linux:
```
python3 -m venv venv
```
Активировать виртуальное окружение:
Для Windows:
```
source venv/Scripts/activate
```
Для Linux:
```
source venv/bin/activate
```
Перейти в корневую папку проекта:
```
cd Test_grocery_store_Sarafan/
```
Установить зависимости:
```
pip install -r requirements.txt
```
Запустить сервер разработки:
```
python manage.py runserver
```


http://127.0.0.1:8000/admin/

Примеры запросов к API:
Получение списка всех категорий с подкатегориями:
```
GET запрос:
http://127.0.0.1:8000/api/categories/
```
Ответ:
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Fruits",
            "slug": "fruits",
            "image": "http://127.0.0.1:8000/media/categories/images/for_CV.jpg",
            "subcategories": [
                {
                    "id": 2,
                    "name": "Berries",
                    "slug": "berries",
                    "image": "http://127.0.0.1:8000/media/subcategories/images/%D0%94%D0%97.png"
                },
                {
                    "id": 1,
                    "name": "Citrus",
                    "slug": "citrus",
                    "image": "http://127.0.0.1:8000/media/subcategories/images/Bussinnes_11.jpg"
                }
            ]
        }
    ]
}
```
Получение списка продуктов:
```
GET запрос:
http://127.0.0.1:8000/api/products/
```
Ответ:
```
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Raspberry",
            "slug": "raspberry",
            "category": "fruits",
            "subcategory": "berries",
            "price": "100.00",
            "images": [
                {
                    "size": "small",
                    "url": "/media/products/images/small/products/images/original/Apple_J5QRJNs.jpg"
                },
                {
                    "size": "medium",
                    "url": "/media/products/images/medium/products/images/original/Apple_lXN3yRf.jpg"
                },
                {
                    "size": "large",
                    "url": "/media/products/images/large/products/images/original/Apple_67P51ob.jpg"
                }
            ]
        },
        {
            "name": "Bulba",
            "slug": "bulba",
            "category": "vegitables",
            "subcategory": "tomatos",
            "price": "999.00",
            "images": [
                {
                    "size": "small",
                    "url": "/media/products/images/small/products/images/original/12.1.jpg"
                },
                {
                    "size": "medium",
                    "url": "/media/products/images/medium/products/images/original/12.1.jpg"
                },
                {
                    "size": "large",
                    "url": "/media/products/images/large/products/images/original/12.1.jpg"
                }
            ]
        },
            ]
        }
    ]
}
```
Добавление, изменения (изменение количества) и удаления выбранного продукта в корзину.
Если количество не передано то в корзину добавляется одна единица продукта по умолчанию:
```
POST запрос:
http://127.0.0.1:8000/api/products/3/shopping_cart_item/
{
    "amount": 3
}
```
Ответ:
```
{
    "user": 2,
    "product": 3,
    "amount": 3
}
```
```
DELETE запрос:
http://127.0.0.1:8000/api/products/3/shopping_cart_item/
```
Ответ:
```
204_NO_CONTENT
```

Вывода состава корзины с подсчетом количества товаров и суммы стоимости товаров в корзине:
```
GET запрос:
http://127.0.0.1:8000/api/shopping_cart/
```
Ответ:
```
{
    "products": [
        {
            "product_name": "Pear",
            "product_price": "95.00",
            "amount": 6,
            "total_product_cost": 570.0
        },
        {
            "product_name": "Bulba",
            "product_price": "999.00",
            "amount": 3,
            "total_product_cost": 2997.0
        }
    ],
    "total_cost": 3567.0
}
```
Полная очистка корзины:
```
DELETE запрос:
http://127.0.0.1:8000/api/shopping_cart/
```
Ответ:
```
{
    "detail": "Корзина очищена."
}
```

Эндпоинты Djoser:
```
http://127.0.0.1:8000/api/auth/users/
http://127.0.0.1:8000/api/auth/token/login/
http://127.0.0.1:8000/api/auth/token/logout/
```

Авторы: 

- [Ласовский Владимир](https://github.com/herrShneider?tab=repositories) 