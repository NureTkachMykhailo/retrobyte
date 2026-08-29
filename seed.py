import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retrobyte_project.settings")
django.setup()

from django.contrib.auth.models import User

from blog.models import Article, Category, Comment

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@retrobyte.local", "admin12345")

author, _ = User.objects.get_or_create(username="mtkach", defaults={"email": "m.tkach@retrobyte.local"})
author.set_password("retrobyte123")
author.save()

reader, _ = User.objects.get_or_create(username="reader", defaults={"email": "reader@retrobyte.local"})
reader.set_password("retrobyte123")
reader.save()

data = {
    "Старі комп'ютери": {
        "description": "Залізо минулого сторіччя",
        "articles": [
            ("ZX Spectrum: комп'ютер, що вчив програмувати ціле покоління", "8-бітна машина 1982 року з гумовою клавіатурою розійшлася мільйонними тиражами і клонами по всьому світу, включно з пострадянським простором."),
            ("Commodore 64: найпродаваніший комп'ютер в історії", "Понад 12 мільйонів проданих одиниць і досі активна спільнота ентузіастів, що пишуть нові ігри під платформу навіть у 2020-х."),
            ("Електроніка БК-0010: радянська відповідь домашнім ПК", "Машина з клавіатурою на кнопках 'Электроника' і власним діалектом Бейсику стала першим комп'ютером для багатьох радянських школярів."),
        ],
    },
    "Ретро-ігри": {
        "description": "Класика, яка не старіє",
        "articles": [
            ("Чому Doom досі портують на все підряд", "Від холодильників до калькуляторів — двигун id Tech 1 виявився настільки компактним, що ентузіасти запускають його буквально де завгодно."),
            ("Tetris: історія гри, яка перетнула залізну завісу", "Створена в СРСР головоломка стала предметом багаторічної судової суперечки за права на видання по всьому світу."),
            ("Секрети спідранів у класичних платформерах", "Механіки прискорення в іграх на кшталт Super Mario Bros. активно вивчаються спідран-спільнотою й донині."),
        ],
    },
    "Історія технологій": {
        "description": "Як ми дійшли до цього",
        "articles": [
            ("Перший модем і початок домашнього інтернету", "Акустичні модеми на 300 біт/с здаються смішними сьогодні, але саме вони поклали початок доступу простих користувачів до мереж."),
            ("Дискети: від 8 дюймів до 3.5", "Еволюція знімних носіїв показує, як індустрія поступово зменшувала форм-фактор, нарощуючи ємність у сотні разів."),
        ],
    },
}

for name, payload in data.items():
    category, _ = Category.objects.get_or_create(name=name, defaults={"description": payload["description"]})
    for title, text in payload["articles"]:
        article, created = Article.objects.get_or_create(
            title=title,
            defaults={"text": text, "category": category, "author": author},
        )
        if created:
            Comment.objects.create(author=reader, text="Дуже пізнавально, не знав про це!", article=article)

print("Seed complete:", Category.objects.count(), "categories,", Article.objects.count(), "articles")
