# 🤖 Telegram Mailing Bot for Telegram and Instagram

![](https://img.shields.io/badge/Python-3.10-blue) ![](https://img.shields.io/badge/pyTelegramBotAPI-lightblue) ![](https://img.shields.io/badge/telethon-darkblue) 

Этот проект представляет собой Telegram бота, который имеет несколько функций для управления рекламным контентом и таргетированными рассылками. Вот основные функции бота:

* рассылка о рекламируемом канале юзерам телеграм в публичные чаты с возможностью перегенерирования сообщения с 
помощью GPT моделей
* просмотр сториз у пользователей таргетных каналов, имеющих Telegram Premium
* рассылка сообщений и reels в Instagram

# 👀 Посмотри, как бот работает

Перейди вот по этой ссылке 👉 [[Видео презентация]](https://youtu.be/uf7YYGz7lQo) 👈

# ⚙️ Установка и настройка проекта 

## 1. Склонируйте репозиторий с github
```.sh
git clone <https://.git>
```

## 2. Создайте ``` .env ``` в корне проекта
```.sh
touch .env
```
Содержимое файла ```.env```. Изменять нужно только поля ```TELEGRAM_BOT_TOKEN```, полученный от @BotFather, ```YANDEX_CLOUD_API_KEY``` и ```CATALOG_ID_YANDEX_CLOUD```, если не сказано противного дальше в README.
```.env-example
# Database config
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=db
POSTGRES_HOST=IPAddress
POSTGRES_PORT=5432

# PGAdmin config
PGADMIN_DEFAULT_EMAIL=root@root.com
PGADMIN_DEFAULT_PASSWORD=root

# Telegram bot
TELEGRAM_BOT_TOKEN=token

# YandexGPT
YANDEX_CLOUD_API_KEY=key
CATALOG_ID_YANDEX_CLOUD=id
```

## 3. Установите необходимые зависимости:
```.sh
❯ python3 -m venv venv
❯ source venv/bin/activate
❯ pip install -r requirements.txt
❯ export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## 🐋 Установка базы данных через докер

### 1. Запустите базу данных

Прописывайте следующие команды в **новом** терминале/скрине. Если докер использовался до этого, то остановите все процессы, связанные с ним.
```.sh
❯ sudo docker stop $(sudo docker ps -a -q)
❯ sudo docker rm $(sudo docker ps -a -q)
```
Если до этого он не использовался, то достаточно прописать только эту команду.
```.sh
❯ docker-compose -f docker-compose_db.yaml
```

### 2. Получите IPAddress, на котором запущена база данных
```.sh
❯ docker inspect db | grep IPAddress
```
```.sh
❯ "SecondaryIPAddresses": null,
❯       "IPAddress": "",
❯               "IPAddress": "172.18.0.2",
                              ↑↑↑↑↑↑↑↑↑↑
                              IPAddress
```
Скопируйте полученный IPAddress в буфер. ❗️ При **каждом** перезапуске базы данных IPAddress изменяется.

### 3. Зайдите в ```.env``` и инициализируйте поле ```POSTGRES_HOST``` только что скопированным ```IPAddress```

### 4. Отредактируйте ```alembic.ini```

Перейдите ```cd App/Database``` и замените в ```sqlalchemy.url``` ip-адрес базы данных, на IPAddress, который был уже получен ранее.
```alembic.ini
sqlalchemy.url = postgresql+asyncpg://postgres:postgres@172.18.0.2:5432/db
                                                        ↑↑↑↑↑↑↑↑↑↑
                                                         IPAddress   
```

### * Опционально: Инициализируйте миграции в базе данных

Если в только что скопированном проекте появляются ошибки по типу ```revision not found``` или ```target database is not up to date```, то нужно пересоздать миграции для правильной его работы. Миграции накатываются автоматически каждый раз при запуске бота ```App/Bot/main.py```.

```.sh
❯ rm -rf migrations
❯ alembic init -t async -m 'init'
```

### * Опционально: Импортируйте Base в ```env.py```

Если был выполнен предыдущий шаг "Инициализируйте миграции в базе данных", то этот является **обязательным**. Перейдите ```cd App/Database/migrations``` и отредактируйте файл env.py: импортируйте в него ```Base``` из ```App/Database/Models``` и замените ```target_metadata = None``` на ```Base.metadata```.
```.sh 
from App.Database.Models import Base

target_metadata = Base.metadata
```

## 🐘 Установка базы данных через PostgreSQL

### 1. Скачайте менеджер баз данных PostgreSQL по [ссылке](https://www.postgresql.org/download/)

### 2. Создайте пользователя ```postgres``` с паролем ```postgres```

Если вы не хотите использовать такое имя и пароль, то вам обязательно нужно будет отредактировать поля в ```.env``` ```POSTGRES_NAME``` - имя пользователя PostgreSQl - и ```POSTGRES_PASSWORD``` - пароль пользователя PostgreSQL.

### 3. После логина в пользовтеля нажмите правой кнопкой мыши по полю ```Databases```, чтобы создать новую базу данных с названием ```db```

Если вы не хотите использовать такое название базы данных, то вам обязательно нужно будет отредактировать поле в ```.env``` ```POSTGRES_DB``` - название базы данных.

### 4. Зайдите в ```.env``` и инициализируйте поле ```POSTGRES_HOST```

Замените это поле либо на ```localhost```, либо на ```127.0.0.1```.

### 5. Отредактируйте ```alembic.ini```

Перейдите ```cd App/Database``` и замените в ```sqlalchemy.url``` ip-адрес базы данных, на localhost или 127.0.0.1, который был уже получен ранее.
```.ini
sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost:5432/db
                                                        ↑↑↑↑↑↑↑↑↑↑
                                                         IPAddress   
```

### * Опционально: Инициализируйте миграции в базе данных

Если в только что скопированном проекте появляются ошибки по типу ```revision not found``` или ```target database is not up to date```, то нужно пересоздать миграции для правильной его работы. Миграции накатываются автоматически каждый раз при запуске бота ```App/Bot/main.py```.

```.sh
❯ rm -rf migrations
❯ alembic init -t async -m 'init'
```

### * Опционально: Импортируйте Base в ```env.py```

Если был выполнен предыдущий шаг "Инициализируйте миграции в базе данных", то этот является **обязательным**. Перейдите ```cd App/Database/migrations``` и отредактируйте файл env.py: импортируйте в него ```Base``` из ```App/Database/Models``` и замените ```target_metadata = None``` на ```Base.metadata```.
```.sh 
from App.Database.Models import Base

target_metadata = Base.metadata
```

## ✌🏻 Установка проекта мануально 

После установки базы данных выполните следующие шаги:

1. Создайте 4 терминала/скрина и пропишите в них команды
```.sh
❯ export PYTHONPATH=$PYTHONPATH:$(pwd)
❯ source venv/bin/activate
```
2. Прописать по команде в каждом из терминалов
```.python
❯ python3 App/Bot/main.py
```
```.python
❯ python3 App/UserAgent/UserAgentSpamPlugin.py
```
```.python
❯ python3 App/UserAgent/UserAgentStoriesPlugin.py
```
```.python
❯ python3 App/Parser/ParserSpamPlugin.py
```

## 📦 Установка проекта через docker

После установки базы данных выполните следующие шаги:

```shell
❯ docker-compose -f docker-compose.yaml build - сбилдить образы
❯ docker-compose -f docker-compose.yaml up - запустить образы в контейнерах
```

# 📚 Структура телеграм бота, его классы и их методы
## Bot
Содержит папки:  

```Filters```: message_handler'ы по обработке отправки пересланных сообщений или ответа на них 

```Handlers```: меню бота, основная логика взаимодействия с ним

```Markups```: все markup'ы

```Middlewares```: обработка отправки слишком большого количества запросов боту

```main.py```: запуск бота

## Config
```bot.py```: инициализация объекта bot класса AsyncTelebot по ```TELEGRAM_BOT_TOKEN```

```__init__.py```: 

**singleton**: обертка классов, обеспечивающая создание только одного его экземпляра и предоставляющая
глобальную точку доступа к нему

---

**MessageContextManager**: класс, позволяющий хранить id последнего сообщения с помощью chat_id, по которому происходит его удаление

**help_menu_msgId_to_delete** - поля класса, представляющее собой словарь по chat_id id сообщений

**add_msgId_to_help_menu_dict(self, chat_id, msgId)** - добавление id сообщения в help_menu_msgId_to_delete по chat_id

**delete_msgId_from_help_menu_dict(self, chat_id)** - удаление id сообщения в help_menu_msgId_to_delete по chat_id

---

**AccountContext**: класс, позволяющий хранить название аккаунта, с которого происходит взаимодействие с ботом по chat_id

**account_name** - поля класса, представляющее собой словарь по chat_id account_name

**updateAccountName(self, chat_id: int, account_name: str)** - обновление account_name по chat_id в account_name

---

**LoginPasswordContext**: класс, позволяющий хранить логин и пароль по chat_id

**password** - поля класса, представляющее собой словарь по chat_id password

**login** - поля класса, представляющее собой словарь по chat_id login

**updateLogin(self, chat_id: int, login: str)** - обновление login по chat_id в login

**updatePassword(self, chat_id: int, password: str)** - обновление password по chat_id в password

## Database
Содержит папки и файлы: 

```DAL```, 

```Models```,

```session.py``` (конфигурационный файл базы данных, создание движка для взаимодействия с ней)

## Logger

Содержит файлы: 

```ApplicationLogger.py```: создание класса ApplicationLogger

## Parser

Содержит папки и файлы:

```sessions```: папка для дампа куки файлов аккаунтов инстаграм

```InstagramParser.py```:

**InstagramParserExceptions**: класс исключений, который происходят при работе парсера с instagram.com

---

**InstagramParser**: класс, наследуемый от класса Parser, отвечающий за парсинг веб сайта instagram.com

**login, password, proxy** - поля класса, отвечающие за хранение строк логин, пароля и прокси адреса соответственно

**check_proxy(self)** - метод для проверки подключения к введенному прокси серверу 

**async_check_proxy(self)** - асинхронный метод обертка для check_proxy

**logging_in(self)** - метод, производящий логин в аккаунт Instagram 

**async_logging_in(self)** - асинхронный метод обертка для logging_in

**parse_followers(self, channel: str)** - метод, производящий парсинг фолловеров аккаунта с именем channel

**scroll_followers_dialogue(self, dialogue, followers_count, step=12)** - метод, листающий диалоговое окно с подписчиками канала;
dialogue - объект страницы, followers_count - количество подписчиков, step=12 - количество пролистываемых подписчиков за каждый скрол

**async_parse_follower(self, channel: str)** - асинхронный метод обертка для parse_followers

**send_message(self, message: str, reels_link: str, channel: str)** - метод, отправляющий аккаунту с именем channel message и reels_link

**async_send_message(self, message: str, reels_link: str, channel: str)** - асинхронный метод обертка для send_message

**dump_cookies(self)** - метод для дампа куки файлов 

**load_cookies(self)** - метод для загрузки куки файлов 

---

❗️Если на компьютере установлен веб-браузер Chrome, то важно помнить, чтобы он был последней версии, иначе будут происходить конфликты с webdriver_manager. Также, после каждого официального обновления браузера нужно обновлять undetected-chromedriver во избежание ошибок
```.python
# error: urllib.error.HTTPError: HTTP Error 404: Not Found
# fix:
pip install --upgrade undetected-chromedriver
```

---

```Parser.py```:

**Parser** - родительский класс, предоставляющий глобальную точку доступа и гарантирующий, что будет создан только один его экземпляр

**__init__** - инициализация объекта класса

**close_parser(self)** - закрытия веб ресурсов, связанных с классом, таких как веб драйвер

Для тестирования бота с GUI закомментируйте данные строчки:

```.python
# в __init__
self.__op.add_argument("--no-sandbox") 
self.__op.add_argument("--disable-dev-shm-usage")
self.__op.add_argument(f"--log-path=parser.log")
self.__display = Display(visible=True, size=(1234, 1234))
self.__display.start()
# в close_parser
self.__display.stop()
```

---

```ParserSpamPlugin.py```: плагин, отвечающий за спам рассылку Instagram

```ProxyExtension.py```: создает класс ProxyExtension и подгружает .json файл с введенным прокси, как разрешение браузера

```Xpath.py```: содержит XPATH к объектам страниц, c которых происходит парсинг

## UserAgent

### Core

```UserAgentCore.py```: класс UserAgent и его методы, как обертки над методами pytelegrambotapi

---

Содержит файлы:

```UserAgentDbPremiumUsers.py```:

**DbPremiumExceptions** - класс исключений, который происходят при работе парсера с Telegram

**WRONG_USERNAME_EXCEPTION** - api telegram не смог найти юзера с введенным username'ом

**ADMIN_PRIVILEGES_EXCEPTION** - фолловеры канала, юзернейм которого был введен, не доступны всем пользователям, а только админам

---

**get_members_from_tg(session_name, usernames, limit=None)** - функция для парсинга премиум подписчиков из каналов с usernames для аккаунта с session_name

```UserAgentSpamPlugin.py```: плагин, отвечающий за спам рассылку Telegram

```UserAgentStoriesPlugin.py```: плагин, отвечающий за отслеживание сториз в Telegram

## YandexGPT

Содержит папки и файлы:

```json_history```: папка для хранения логов запросов различных аккаунтов к YandexGPT

```YandexGPTMsgRebuilder.py```:

**YandexGPTMsgRebuilder** - класс конфигурирующий запросы к YandexGPT

**rewrite_message(cls, account_name: str, prompt: str)** - метод, отправляющий YandexGPT сообщение о перегенарации текущего сообщения, согласно промпту 

# ⭐️ Фидбек

[![](https://img.shields.io/badge/Issues-red)](https://github.com/complicat9d/Telegram-Instagram-MailingBot/issues)

Если вам понравился этот проект, то подпишитесь на гитхаб аккаунты создателей и поставьте ему звездочку, это мотивирует нас улучшать даный проект. 

Если вы нашли баг при использовании проекта, то создайте "проблему", мы ее обязательно рассмотрим 🤠


# 👤 Авторы

* [@complicat9d](https://github.com/complicat9d)

* [@kde2podfreebsd](https://github.com/kde2podfreebsd)

