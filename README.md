Проект YaMDb Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр. Новые жанры может создавать только администратор. Пользователи могут оставить к произведениям текстовые отзывы и поставить произведению оценку в диапазоне от одного до десяти. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. Присутствует возможность комментирования отзывов.

Функционал API:

Просмотр произведений (кино, музыка, книги), которые подразделяются по жанрам и категориям.. Возможность оставлять отзывы на произведения и ставить им оценки, на основе которых построена система рейтингов. Комментирование оставленных отзывов. Проект разработан командой из трех человек с использованием Git в рамках учебного курса Яндекс.Практикум.

Разработчик Нестеров Никита (https://github.com/Mikita2410): Разработка системы регистрации и аутентификации, прав доступа, работы с токеном, системы подтверждения через e-mail.

Стек технологий Python 3.9 Django 3.2 Django REST Framework 3.12.4 Django REST Framework simplejwt 5.1.0


Запуск Docker контейнеров: Запустите docker-compose cd infra/ docker-compose up -d --build 

Cоздайте суперпользователя: docker-compose exec web python manage.py createsuperuser 

Следующими шагами загрузить дамп (резервную копию) базы: cd api_yamdb && python manage.py loaddata ../infra/fixtures.json 

Проверьте доступность сервиса http://localhost/admin 

Документация http://localhost/redoc/ 

Права доступа: Доступно без токена. GET /api/v1/categories/ - Получение списка всех категорий 

GET /api/v1/genres/ - Получение списка всех жанров 

GET /api/v1/titles/ - Получение списка всех произведений 

GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов 

GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву 

Права доступа: Администратор GET /api/v1/users/ - Получение списка всех пользователей 

Получение JWT-токена: POST /api/v1/auth/token/

{ "username": "string", "confirmation_code": "string" }

## Ссылки на проект:
* http://51.250.29.80/api/v1/titles/
* http://51.250.29.80/api/v1/categories/
* http://51.250.29.80/api/v1/genres/
* http://51.250.29.80/redoc/
* http://51.250.29.80/admin/

## Статус workflow
[![workflow](https://github.com/Mikita2410/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)](https://github.com/Mikita2410/yamdb_final/actions/workflows/yamdb_workflow.yml)