# Домашнее задание - 8

## Создание проекта, работа с моделями и продвинутая настройка админки

## Цель и задачи проекта
- [x] Создание проекта и настройка моделей.
   
1. config директория - с настройками и подключением к нашему приложению
2. store директория - файлы нашего приложения
3. migrations директория - файлы миграций наших моделей
4. db.sqlite3 - файл базы данных в формате sqlite
      
1. store/models.py

    Category - класс категорий продуктов, наследуется от базового класса для всех наших классов models.Model

    Product - класс продуктов, в нем мы реализовали связь один ко многим через ForeignKey.

    Пример связи. Категория молочные продукты. Продукты такие как творог, сметана, сыр.

2. Заполнение базы данных.
    Ниже список команд которые использовались для заполнения БД через python manage.py shell
```commandline
category_milk = Category.objects.create(name='Молочные продукты', description='Продукты сделанные из коровьего молока')
category_frut = Category.objects.create(name='Фрукты', description='Фрукты из садов')
product_tvorog = Product.objects.create(name='Творог', description='Творок в упаковке, цена за кг', price='480', category=category_milk)
product_smetana = Product.objects.create(name='Сметана', description='Сметана в упаковке, цена за 500 гр', price='215', category=category_milk)

product_apple = Product.objects.create(name='Яблоки', description='Яблоки на развес, цена за кг', price='180', category=category_frut)
product_mandarin = Product.objects.create(name='Мандарины', description='Мандарины на развес, цена за кг', price='240', category=category_frut)
```
3. Проверка связанности
    Через категорию посмотрим какие к ней привязаны продукты
```commandline
>>> category_milk.products.all()
<QuerySet [<Product: name=Творог, description=Творок в упаковке, цена за кг, price=480.0, created_at=2026-08-01 16:34:41.813749+00:00>,
           <Product: name=Сметана, description=Сметана в упаковке, цена за 500 гр, price=215.0, created_at=2026-08-01 16:37:40.944851+00:00>]>
```