# api_final

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://git@github.com:KlavaD/api_yamdb.git
```

```
cd api_yamdb
```

Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Сделать импорт из csv файлов:

```
python manage.py addcsv
```

Запустить проект:

```
python3 manage.py runserver
```