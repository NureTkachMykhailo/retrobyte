# RetroByte

Блог про ретро-техніку: старі комп'ютери, ретро-ігри, історія технологій. Лабораторна робота №1 з дисципліни ВМПтФ — Django.

## Стек
- Django 6.1, Django ORM (SQLite)
- Django REST Framework — `/api/articles/`
- Паттерн MTV, наслідування шаблонів, пагінація (`Paginator`)
- Docker / docker-compose

## Рівні
- **1** — моделі `Category`/`Article`, список категорій з підрахунком статей через `annotate(Count(...))`
- **2** — модель `Comment`, CRUD статей (`ArticleForm`), права редагування/видалення (тільки автор або staff)
- **3** — наслідування шаблонів (`base.html`), стилізація, пагінація статей (6/стор.) і коментарів (5/стор.)
- **4** — автентифікація (вхід/вихід/реєстрація), пошук за `icontains`, REST API через DRF (`ArticleSerializer`, `ArticleViewSet`)

Демо-акаунти після `seed.py`: `mtkach` / `retrobyte123` (автор), `reader` / `retrobyte123`, `admin` / `admin12345` (суперкористувач).

## Запуск

```bash
pip install -r requirements.txt
python manage.py migrate
python seed.py
python manage.py runserver
```

Або через Docker:

```bash
docker compose up --build
```
