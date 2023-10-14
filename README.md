# Проект с использованием Django REST framework, Celery и Redis

Этот проект представляет собой пример Django-приложения, использующего Django REST framework, Celery для асинхронной обработки задач и Redis в качестве брокера сообщений для Celery.

## Установка

### 1. Клонируйте репозиторий:
git clone https://github.com/Alnazhm/upload_file_S3.git
### 2.Создайте виртуальное окружение и активируйте его:
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate  # Для Windows
### 3.Установите зависимости:
pip install -r requirements.txt
### 4.Настройте базу данных, выполнив миграции:
python manage.py migrate
### 5.Запустите сервер:
python manage.py runserver
### 6.Запустите Celery worker для обработки асинхронных задач:
celery -A file_upload worker -l info
### 7.Запустите redis
redis-server
