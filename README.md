# Currency Project

## Установка

1. Клонируйте репозиторий:

    ```bash
    mkdir currency_project
    cd currency_project
    git clone https://github.com/SusumoHiroku/Test_HELSI.git

    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```
4. Установите PostgreSQL и создайте базу данных и пользователя для доступа:
   ```bash
    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib
    sudo -u postgres psql
    CREATE DATABASE currency_db;
    CREATE USER client_currency WITH PASSWORD 'client_currency';
    ALTER ROLE client_currency SET client_currency TO 'client_currency';
    ```


5. Примените миграции:

    ```bash
    python manage.py migrate
    ```

6. Запустите Celery:

    ```bash
    celery -A currency_monitor worker --loglevel=info
    celery -A currency_monitor beat --loglevel=info
    ```

7. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

## Использование

### API эндпоинты

- Получение списка валют с текущим курсом:
    ```
    GET /api/currencies/
    ```

- Получение списка валют, которые можно добавить для отслеживания:
    ```
    GET /api/currencies/available/
    ```

- Добавление новой валюты для отслеживания:
    ```
    POST /api/currencies/
    
  {
    "code_a": "555",
    "name_a": "Some Currency",
    "alpha3_a": "SCR"
  }
    ```

- Получение истории курса по конкретной валюте за конкретный период времени:
    ```
    GET /api/rates/{id}/history/{start_date}/{end_date}
    ```

- Включение/отключение валюты из мониторинга:
    ```
    PUT /api/currencies/{id}/toggle/
    ```


### Менеджмент команда

Экспорт валют в CSV файл:

```bash
python manage.py export_currencies


### Swagger

http://127.0.0.1:8000/swagger/



