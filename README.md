## Проект сайта новостного блога
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

### Описание проекта

Сайт новостного блога, с возможностью добавления новостей, комментирования новостей других авторов. При желании, каждую публикацию автор может украсить фотографией или картинкой. Для удобства ознакомления, все новости на сайте разбиты по категориям.

В проекте реализована авторизация и аутентификация пользователей блога с верификацией данных, осуществлена пагинация постов сайта, взаимодействие с базой данных, созданы кастомные страницы ошибок 403 CSRF, 404 и 500.

### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Dmitri-prog/news-blog.git
```

```
cd news-blog
```

2. Cоздать в корне проекта файл .env и заполнить его (пример файла .env см. в приложенном файле .env.example). Описание переменных виртуального окружения файла .env для работы проекта:
```
SECRET_KEY - cекретный ключ установки Django. Он используется в контексте криптографической подписи и должен иметь уникальное, непредсказуемое значение. Новый оригинальный секретный ключ можно получить при помощи функции get_random_secret_key(), импортируемой из django.core.management.utils;
DEBUG - настройка вывода отладочной информации в Django-проекте, указывается в файле settings.py, при развертывании проекта должно быть установлено значение False
ALLOWED_HOSTS - список хостов/доменов, для которых может работать текущий проект. По умолчанию доступны хосты '127.0.0.1' и 'localhost'.
```

3. Cоздать и активировать виртуальное окружение:

Windows
```
python -m venv venv
```
```
source venv/Scripts/activate
```
Linux/macOS
```
python3 -m venv venv
```
```
source venv/bin/activate
```

4. Обновить PIP

Windows
```
python -m pip install --upgrade pip
```
Linux/macOS
```
python3 -m pip install --upgrade pip
```

5. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

6. Перейти в директорию с файлом manage.py и выполнить миграции:

Windows
```
cd blogicum
```
```
python manage.py migrate
```

Linux/macOS
```
cd blogicum
```
```
python3 manage.py migrate
```

7. Запустить проект:

Windows
```
python manage.py runserver
```

Linux/macOS
```
python3 manage.py runserver
```

8. При желании, на сайт можно загрузить примеры публикаций:
```
python manage.py loaddata db.json
```

#### Автор

Марков Дмитрий
