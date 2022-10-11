<h1 align="center">
JPLearningBot
</h1>
<p align="center">
Бот для помощи в изучении японского языка
<br /><br />
<img alt="Python3.8" src="https://img.shields.io/badge/Python-3.8-blue">
<img alt="Django4.1.1" src="https://img.shields.io/badge/Django-4.1.1-brightgreen">
<img alt="Uvloop0.17.0" src="https://img.shields.io/badge/uvloop-0.17.0-blue">
<img alt="Aiogram2.22.1" src="https://img.shields.io/badge/Aiogram-2.22.1-blue">
</p>

## Взаимодействие с ботом
Следует прочесть вот эту [статью](https://telegra.ph/JPLearning-Bot-10-09)
<br />
Как и все вы можете помочь в моем маленьком проекте, в его развитии, буду очень благодарен ^_^

## Установка и запуск
Сначала создадим виртуальное окружение и установим зависимости
```shell
python3 -m venv env
source env/bin/activate
python -m pip install requirements.txt
```
После нужно провести миграцию моделей для создания базы данных
```shell
python manage.py migrate
```
Теперь в файле [settings](https://github.com/AikoSora/JPLearningBot/blob/main/tgbot/settings.py) в самом низу укажем токен который можно получить [здесь](https://t.me/BotFather)
<br />
После можно запустить бота
```shell
python manage.py startbot
```

## Команды
Все команды можно создавать в папке [commands](https://github.com/AikoSora/JPLearningBot/tree/main/app/bot/commands), примеры вы можете осмотреть там-же