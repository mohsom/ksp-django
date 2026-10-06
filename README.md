# Django Girls Blog

Навчальний блог на Django за туторіалом [Django Girls](https://tutorial.djangogirls.org/en/): публічний список постів, детальна сторінка, а для авторизованого користувача — створення, редагування, чернетки, публікація та видалення.

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
| **Model** | Опис даних; ORM перетворює класи на таблиці БД | `blog/models.py` → `Post` |
| **View** | Приймає `HttpRequest`, повертає `HttpResponse` | `blog/views.py` |
| **Template** | HTML з вставками (`{{ }}`, `{% %}`) | `blog/templates/` |
| **URLconf** | Зіставляє URL з в’ю | `mysite/urls.py`, `blog/urls.py` |

Також із коробки: адмінка, автентифікація, сесії, захист від CSRF, форми з валідацією, міграції.

### Життєвий цикл запиту

```
Браузер → runserver/WSGI → Middleware (вхід)
        → URLconf (mysite/urls.py → blog/urls.py)
        → View (Model/ORM ↔ БД)
        → Template → HttpResponse
        → Middleware (вихід) → Браузер
```

1. Запит проходить ланцюжок **middleware** (безпека, сесії, CSRF, автентифікація…).
2. **URLconf** шукає перший збіг шляху й викликає відповідне в’ю з параметрами (наприклад, `pk`).
3. **View** отримує дані через ORM (`Post.objects.filter(...)`), обробляє форми.
4. `render()` підставляє контекст у **шаблон** і повертає HTML.

## Структура проєкту

```
ksp-django/
├── manage.py              # CLI: runserver, migrate, test, shell…
├── requirements.txt
├── mysite/                # конфігурація проєкту
│   ├── settings.py        # налаштування (БД, застосунки, middleware, TZ…)
│   ├── urls.py            # кореневий URLconf: admin, login/logout, include(blog.urls)
│   ├── wsgi.py / asgi.py  # точки входу для серверів
└── blog/                  # застосунок
    ├── models.py          # Post
    ├── admin.py           # реєстрація Post в адмінці
    ├── forms.py           # PostForm (ModelForm)
    ├── views.py           # в’ю на функціях
    ├── urls.py            # маршрути блогу
    ├── tests.py           # тести
    ├── migrations/        # історія змін схеми БД
    ├── static/css/blog.css
    └── templates/
        ├── blog/          # base, post_list, post_detail, post_edit, post_draft_list
        └── registration/  # login.html
```

**Проєкт vs застосунок:** проєкт (`mysite`) — це конфігурація та склейка; застосунок (`blog`) — переюзабельний модуль із власними моделями, в’ю та шаблонами. Застосунок підключається через `INSTALLED_APPS`.

## Модель даних

`Post`: `author` (FK на `User`), `title`, `text`, `created_date`, `published_date` (null = чернетка). Метод `publish()` ставить дату публікації.

## Маршрути

| URL | В’ю | Доступ |
|-----|-----|--------|
| `/` | `post_list` — опубліковані пости | усі |
| `/post/<pk>/` | `post_detail` | усі |
| `/post/new/` | `post_new` | логін |
| `/post/<pk>/edit/` | `post_edit` | логін |
| `/drafts/` | `post_draft_list` | логін |
| `/post/<pk>/publish/` | `post_publish` (POST) | логін |
| `/post/<pk>/remove/` | `post_remove` (POST) | логін |
| `/accounts/login/`, `/accounts/logout/` | вбудовані `LoginView` / `LogoutView` | — |
| `/admin/` | адмінка | staff |

## Ключові рішення

- **Успадкування шаблонів:** `base.html` містить каркас сторінки, решта шаблонів розширюють `{% block content %}`.
- **ModelForm:** `PostForm` генерує форму й валідацію з моделі; `save(commit=False)` дає змогу виставити `author` перед збереженням.
- **Іменовані URL-и** (`{% url 'post_detail' pk=post.pk %}`, `redirect('post_detail', ...)`) замість жорстко прописаних шляхів.
- **Безпека:** `@login_required` на змінних діях; публікація та видалення лише через POST (`@require_POST`) із CSRF-токеном.
- **БД:** SQLite (`db.sqlite3`, не в git); схема керується міграціями.

## Корисні команди

```bash
python manage.py makemigrations   # створити міграції зі змін моделей
python manage.py migrate          # застосувати міграції
python manage.py shell            # інтерактивна оболонка з ORM
python manage.py check            # перевірка конфігурації
python manage.py collectstatic    # зібрати статику (для деплою)
```
