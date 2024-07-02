### Проект сайта новостного блога
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

### Описание проекта.

Сайт новостного блога, с возможностью добавления новостей, комментирования новостей других авторов. При желании, каждую публикацию автор может украсить фотографией или картинкой. Для удобства ознакомления, все новости на сайте разбиты по категориям. 
В проекте реализована авторизация и аутентификация пользователей блога с верификацией данных, осуществлена пагинация постов сайта, взаимодействие с базой данных, созданыкастомные страницы ошибок 403 CSRF, 404 и 500.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Dmitri-prog/news-blog.git
```

```
cd news-blog
```

Cоздать и активировать виртуальное окружение:

Windows
```
python -m venv venv
source venv/Scripts/activate
```
Linux/macOS
```
python3 -m venv venv
source venv/bin/activate
```

Обновить PIP

Windows
```
python -m pip install --upgrade pip
```
Linux/macOS
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

Windows
```
python manage.py migrate
```

Linux/macOS
```
python3 manage.py migrate
```

Запустить проект:

Windows
```
python manage.py runserver
```

Linux/macOS
```
python3 manage.py runserver
```

При желании, на сайт можно загрузить примеры публикаций:

python manage.py loaddata db.json
```
