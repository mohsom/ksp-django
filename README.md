# Django Todo

Примітивний список задач на Django: додати, позначити виконаною, видалити. Створений на основі структури з туторіалу [Django Girls](https://tutorial.djangogirls.org/en/) (спочатку був блог, потім замінений на todo).

## Швидкий старт

```bash
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/ · Адмінка: http://127.0.0.1:8000/admin/

Тести: `python manage.py test`

## Короткий огляд Django

Django — це Python-фреймворк «з батарейками» для веб-застосунків. Використовує шаблон **MTV** (Model–Template–View):

| Шар | Що робить | У цьому проєкті |
|-----|-----------|-----------------|
| **Model** | Опис даних; ORM перетворює класи на таблиці БД | `todo/models.py` → `Task` |
| **View** | Приймає `HttpRequest`, повертає `HttpResponse` | `todo/views.py` |
| **Template** | HTML з вставками (`{{ }}`, `{% %}`) | `todo/templates/` |
| **URLconf** | Зіставляє URL з в’ю | `mysite/urls.py`, `todo/urls.py` |

Також із коробки: адмінка, автентифікація, сесії, захист від CSRF, форми з валідацією, міграції.

### Життєвий цикл запиту

```
Браузер → runserver/WSGI → Middleware (вхід)
        → URLconf (mysite/urls.py → todo/urls.py)
        → View (Model/ORM ↔ БД)
        → Template → HttpResponse
        → Middleware (вихід) → Браузер
```

1. Запит проходить ланцюжок **middleware** (безпека, сесії, CSRF, автентифікація…).
2. **URLconf** шукає перший збіг шляху й викликає відповідне в’ю з параметрами (наприклад, `pk`).
3. **View** отримує дані через ORM (`Task.objects.filter(...)`), обробляє форми.
4. `render()` підставляє контекст у **шаблон** і повертає HTML.

## Структура проєкту

```
ksp-django/
├── manage.py              # CLI: runserver, migrate, test, shell…
├── requirements.txt
├── mysite/                # конфігурація проєкту
│   ├── settings.py        # налаштування (БД, застосунки, middleware, TZ…)
│   ├── urls.py            # кореневий URLconf: admin + include(todo.urls)
│   └── wsgi.py / asgi.py  # точки входу для серверів
└── todo/                  # застосунок
    ├── models.py          # Task
    ├── admin.py           # Task в адмінці (list_display, фільтр)
    ├── forms.py           # TaskForm (ModelForm)
    ├── views.py           # в’ю на функціях
    ├── urls.py            # маршрути
    ├── tests.py           # тести
    ├── migrations/        # історія змін схеми БД
    └── templates/todo/task_list.html
```

**Проєкт vs застосунок:** проєкт (`mysite`) — це конфігурація та склейка; застосунок (`todo`) — переюзабельний модуль із власними моделями, в’ю та шаблонами. Підключається через `INSTALLED_APPS`.

## Модель даних

`Task`: `title`, `done` (за замовчуванням `False`), `created_at` (`auto_now_add`). Сортування за `created_at`.

## Маршрути

| URL | В’ю | Дія |
|-----|-----|-----|
| `/` (GET, POST) | `task_list` | список / додати задачу |
| `/tasks/<pk>/toggle/` (POST) | `task_toggle` | змінити статус |
| `/tasks/<pk>/delete/` (POST) | `task_delete` | видалити |
| `/admin/` | адмінка | staff |

## Ключові рішення

- **ModelForm:** `TaskForm` генерує форму й валідацію з моделі (порожній заголовок відхиляється).
- **Іменовані URL-и** (`{% url 'task_toggle' pk=task.pk %}`, `redirect('task_list')`) замість жорстко прописаних шляхів.
- **POST для змін:** toggle і delete тільки через POST (`@require_POST`) із CSRF-токеном; GET повертає 405.
- **Post/Redirect/Get:** після успішної дії — `redirect`, щоб оновлення сторінки не повторювало запит.
- **БД:** SQLite (`db.sqlite3`, не в git); схема керується міграціями.

## Корисні команди

```bash
python manage.py makemigrations   # створити міграції зі змін моделей
python manage.py migrate          # застосувати міграції
python manage.py shell            # інтерактивна оболонка з ORM
python manage.py check            # перевірка конфігурації
python manage.py collectstatic    # зібрати статику (для деплою)
```
