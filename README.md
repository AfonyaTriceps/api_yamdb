# Проект YaMDb

* Проект YaMDb собирает отзывы пользователей на произведения. Сами
произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или
послушать музыку.
* Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
* Произведению может быть присвоен жанр из списка предустановленных.
* Добавлять произведения, категории и жанры может только администратор.
* Благодарные или возмущённые пользователи оставляют к произведениям текстовые
отзывы и ставят произведению оценку в диапазоне от одного до десяти
(целое число); из пользовательских оценок формируется усреднённая оценка
произведения — рейтинг
(целое число). На одно произведение пользователь может оставить только один отзыв.
* Пользователи могут оставлять комментарии к отзывам.
* Добавлять отзывы, комментарии и ставить оценки могут только
аутентифицированные пользователи.

## Техническое описание проекта

### Ресурсы API YaMDb

* Ресурс auth: аутентификация.
* Ресурс users: пользователи.
* Ресурс titles: произведения, к которым пишут отзывы
(определённый фильм, книга или песенка).
* Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
Одно произведение может быть привязано только к одной категории.
* Ресурс genres: жанры произведений. Одно произведение может быть привязано
к нескольким жанрам.
* Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому
произведению.
* Ресурс comments: комментарии к отзывам. Комментарий привязан к
определённому отзыву.

### Пользовательские роли и права доступа

* Аноним — может просматривать описания произведений, читать отзывы и
комментарии.
* Аутентифицированный пользователь (user) — может читать всё, как и
Аноним, может публиковать отзывы и ставить оценки произведениям
(фильмам/книгам/песенкам), может комментировать отзывы; может редактировать
и удалять свои отзывы и комментарии, редактировать свои оценки произведений.
Эта роль присваивается по умолчанию каждому новому пользователю.
* Модератор (moderator) — те же права, что и у Аутентифицированного
пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
* Администратор (admin) — полные права на управление всем контентом проекта.
Может создавать и удалять произведения, категории и жанры.
Может назначать роли пользователям.
* Суперюзер Django должен всегда обладать правами администратора, пользователя
с правами admin. Даже если изменить пользовательскую роль суперюзера —
это не лишит его прав администратора. Суперюзер — всегда администратор,
но администратор — не обязательно суперюзер.

### Самостоятельная регистрация новых пользователей

1. Пользователь отправляет POST-запрос с параметрами email и username на
эндпоинт /api/v1/auth/signup/.
2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code)
на указанный адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и
confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на
запрос ему приходит token (JWT-токен).

### Как запустить проект

> команды указаны для Windows

Клонировать репозиторий и далее перейти в него.
Cоздать и активировать виртуальное окружение:

```sh
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```sh
pip install -r requirements.txt
```

Выполнить миграции:

```sh
python manage.py migrate
```

Запустить проект:

```sh
python manage.py runserver
```

### Примеры работы с API для всех пользователей

Подробная документация доступна по эндпоинту /redoc/

Для неавторизованных пользователей работа с API доступна в режиме чтения,
что-либо изменить или создать не получится.

```sh
Права доступа: Доступно без токена.
GET /api/v1/categories/ - Получение списка всех категорий
GET /api/v1/genres/ - Получение списка всех жанров
GET /api/v1/titles/ - Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ -
Получение списка всех комментариев к отзыву
Права доступа: Администратор
GET /api/v1/users/ - Получение списка всех пользователей
```
