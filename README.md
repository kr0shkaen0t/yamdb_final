Проект «Yamdb»
https://github.com/kr0shkaen0t/yamdb_final

http://51.250.28.17/admin

http://51.250.28.17/redoc

Технологический стек
[![apiyamdb_final workflow](https://github.com/kr0shkaen0t/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/kr0shkaen0t/yamdb_final/actions/workflows/yamdb_workflow.yml)

Краткое описание проекта
Данный сервис собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий (Category) может быть расширен администратором (например, можно добавить категорию "Ювелирные украшения").
В сервисе предусмотрены разные наборы разрешений на действия в зависимости от роли пользователя: Аноним, Просто аутентифицированный пользователь, Модератор, Администратор, Суперпользователь.
Аноним может просматривать описания произведений, читать отзывы и комментарии.
Аутентифицированный пользователь может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений, просматривать информацию о своём аккаунте, менять её (кроме роли). Эта роль присваивается по умолчанию каждому новому пользователю.
Модератор имеет те же права, что и Аутентифицированный пользователь, плюс право удалять и редактировать любые отзывы и комментарии.
Администратор имеет полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может просматривать список зарегистрированных пользователей. Может создавать и назначать роли пользователям. Но администратор не может удалять других администраторов и менять им роли. А также не может удалять и менять суперпользователей (см. ниже).
Суперпользователь имеет абсолютно все разрешения вне зависимости от его "витринной" роли (которая может быть любой из перечисленных выше). В том числе может удалять администраторов и менять им роли.
При регистрации через API-запрос с указанием username и e-mail пользователь получает на указанный электронный адрес письмо с confirmation_code для подтверждения регистрации.
Независимо от способа (API-сервис, командная строка, панель администратора) регистрация пользователя происходит с выдачей ему JWT-токенов: access - для доступа к ресурсам сервиса - и confirmation_code - для подтверждения первичной регистрации пользователя через API и ситуаций необходимости выдачи нового access-токена.
acess-токен включает в себя в том числе информацию о роли пользователя и его статусе суперюзера; таким образом в сервис заложена возможность идентифицации прав пользователя без обращения к БД. В текущей версии для соответствия условиям поставленной задачи используется идентификация роли через обращение к БД.
При изменении информации о пользователе, к которой чувствителен соответствующий токен, вне зависимости от способа изменения, пользователю выдается новый соответствующий токен.
Установка
Шаг 1. Проверьте установлен ли у вас Docker Прежде, чем приступать к работе, необходимо знать, что Docker установлен. Для этого достаточно ввести:

docker -v
Или скачайте Docker Desktop для Mac или Windows. Docker Compose будет установлен автоматически. В Linux убедитесь, что у вас установлена последняя версия Compose. Также вы можете воспользоваться официальной инструкцией.

Шаг 2. Клонируйте репозиторий себе на компьютер Введите команду: git clone https://github.com/kr0shkaen0t/yamdb_final.git

Шаг 3. Создайте в клонированной директории файл .env Пример:

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
Измените файл settings.py, чтобы значения загружались из переменных окружения:

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='db'),
        'PORT': os.getenv('DB_PORT', default='5432'),
    }
}
Шаг 4. Запуск docker-compose Для запуска необходимо выполнить из директории с проектом команду:

docker-compose up -d

Шаг 5. База данных Создаем и применяем миграции:

docker-compose exec web python manage.py migrate --noinput
Шаг 6. Подгружаем статику Выполните команду:

docker-compose exec web python manage.py collectstatic --no-input

Шаг 7. Заполнение базы тестовыми данными Для заполнения базы тестовыми данными вы можете использовать файл fixtures.json, который находится в infra/ Выполните команду:

docker-compose exec web python manage.py loaddata fixtures.json

Другие команды Создание суперпользователя: docker-compose exec web python manage.py createsuperuser

Остановить работу всех контейнеров можно командой: docker-compose down

Для пересборки и запуска контейнеров воспользуйтесь командой: docker-compose up -d --build

Мониторинг запущенных контейнеров: docker stats

Останавливаем и удаляем контейнеры, сети, тома и образы: docker-compose down -v

Автор: Беляев И.
https://github.com/kr0shkaen0t
