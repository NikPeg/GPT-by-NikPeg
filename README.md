# GPT-by-NikPeg
Мой бот для доступа к ChatGPT-4. Небольшой приятный ботик, который даст моим друзьям доступ к ChatGPT.

## Разработка
Установите python3.10.8:  
`pyenv install 3.10.8`  
Активируйте виртуальную среду:  
`pyenv virtualenv 3.10 nikenv`  
или:  
`python -m venv nikenv`  
`.\nikenv\Scripts\activate`  
Сделайте виртуальную среду локальной для удобства:  
`pyenv local nikenv`  
Установите необходимые библиотеки:  
`pip3 install -r requirements.txt`

Создайте файл config.py в основной директории:  
`BOT_TOKEN = "your-telegram-bot-token"`  
`GPT_TOKEN = "your-gpt-token"`  
`ADMIN_ID = your-telegram-id`  
`SOS_URL = "your-telegram-url"`  
`DB_FILENAME = "bot.sqlite"`  
`MODEL = "your-favourite-model"`


Запуститe бота:  
`python3 nik_main.py`  
Войти в консоль БД:  
`sqlite3 bot.sqlite`
