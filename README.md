Проект YaMDb
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр. Новые жанры может создавать только администратор. Пользователи могут оставить к произведениям текстовые отзывы и поставить произведению оценку в диапазоне от одного до десяти. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. Присутствует возможность комментирования отзывов.

Функционал API:

Просмотр произведений (кино, музыка, книги), которые подразделяются по жанрам и категориям..
Возможность оставлять отзывы на произведения и ставить им оценки, на основе которых построена система рейтингов.
Комментирование оставленных отзывов.
Проект разработан командой из трех человек с использованием Git в рамках учебного курса Яндекс.Практикум.

Стек технологий
Python 3.9 Django 2.2.16 Django REST Framework 3.12.4 Django REST Framework simplejwt 5.1.0

Шаблон наполнения .env файла
DB_ENGINE=django.db.backends.postgresql Укажите используемую базу данных DB_NAME=postgres Укажите имя созданной базы данных POSTGRES_USER=postgres Укажите имя пользователя POSTGRES_PASSWORD=postgres Укажите пароль для подключения к базе данных DB_HOST=db Укажите название сервиса (контейнера) DB_PORT=5432 Укажите порт для поключения к базе

Запуск приложения в контейнерах:
Установить docker и docker-compose

Запустить docker-compose из папки /infra_sp2/infra/ командой:

docker-compose up
Выполнить миграции командой:

docker-compose exec web python manage.py migrate
Загрузить статику командой:

docker-compose exec web python manage.py collectstatic --no-input
Загрузить фикстуры из файла fixtures.json:

docker-compose exec web python manage.py loaddata fixtures.json
Чтобы остановить контейнеры, воспользуйтесь командой:

docker-compose down -v

## Статус workflow
[![workflow](https://github.com/Mikita2410/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)](https://github.com/Mikita2410/yamdb_final/actions/workflows/yamdb_workflow.yml)