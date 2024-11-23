**Документация по проекту "Многофункциональный телеграм-бот"
Многофункциональный телеграм-бот**

Данный бот сейчас умеет работать с фотографиями и делать ASCII-арт. Предлагается доработать бот, добавив свои функции.

Описание функционала:

Импорты и настройки

- telebot используется для взаимодействия с Telegram API.

- PIL (Python Imaging Library), известная как Pillow, предоставляет инструменты для работы с изображениями.

- TOKEN — это строковая переменная, куда вы должны поместить токен вашего бота, полученный от @BotFather в Telegram.

- bot = telebot.TeleBot(TOKEN) создает экземпляр бота для взаимодействия с Telegram.

Хранение состояний пользователей

def send_welcome(message): 
- приветствует
- запрашивает изображение

def handle_photo(message):
- сохраняет user_states изображения
- запрашивает набор символов

def get_options_keyboard(): 
- создание клавиатуры с опциями

def callback_query(call): 
- обработчик нажатий на кнопки клавиатуры

Преобразование в ASCII-арт

def ascii_and_send(message):
- Функция преобразования изображения в ASCII и отправки пользователю

def image_to_ascii(image_stream, ascii_chars, new_width=40):
- преобразование изображения в ASCII с использованием пользовательских символов

def pixels_to_ascii(image, ascii_chars):
- преобразование пикселей изображения в ASCII-символы с пользовательским набором

Пикселизация

def pixelate_and_send(message):
- огрубление изображения и отправки пользователю

Негатив

def negative_photo(message):
- создание негатива изображения

Отражение

def mirror_image(message, direction):
- отражение изображения

def convert_to_heatmap(message):
- Преобразование изображения в тепловую карту

def resize_for_sticker(message):
- Изменяем размера изображения для стикера

def jokes_rend(message, JOKES):
- Функция вызывает случайную шутку из списка JOKES

def callback_query(call):
- Обработчик вызова (callback)

def compliment_rend(message, COMPLIMENTS):
- Функция вызывает случайный комплимент из списка COMPLIMENTS

def coin_rend(message, MONETKA):
- Функция подбрасывает монетку