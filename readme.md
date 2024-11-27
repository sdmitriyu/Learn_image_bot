**Документация по проекту "Многофункциональный телеграм-бот"
Многофункциональный телеграм-бот**

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
- ![image_request .png](images%2Fimage_request%20.png)

def handle_photo(message):
- сохраняет user_states изображения
- запрашивает набор символов
- ![character_request .png](images%2Fcharacter_request%20.png)

def get_options_keyboard(): 
- создание клавиатуры с опциями
- ![creating_keyboard.png](images%2Fcreating_keyboard.png)

def callback_query(call): 
- обработчик нажатий на кнопки клавиатуры

Преобразование в ASCII-арт

def ascii_and_send(message):
- Функция преобразования изображения в ASCII и отправки пользователю

def image_to_ascii(image_stream, ascii_chars, new_width=40):
- преобразование изображения в ASCII с использованием пользовательских символов

def pixels_to_ascii(image, ascii_chars):
- преобразование пикселей изображения в ASCII-символы с пользовательским набором
- ![ASCII.png](images%2FASCII.png)

Пикселизация

def pixelate_and_send(message):
- огрубление изображения и отправки пользователю
- ![pixilating_image .png](images%2Fpixilating_image%20.png)

Негатив

def negative_photo(message):
- создание негатива изображения
- ![negative .png](images%2Fnegative%20.png)

Отражение

def mirror_image(message, direction):
- отражение изображения
- ![reflection .png](images%2Freflection%20.png)

def convert_to_heatmap(message):
- Преобразование изображения в тепловую карту
- ![heat_map.png](images%2Fheat_map.png)

def resize_for_sticker(message):
- Изменяем размера изображения для стикера
- ![creating_sticker.png](images%2Fcreating_sticker.png)

def jokes_rend(message, JOKES):
- Функция вызывает случайную шутку из списка JOKES
- ![random_joke.png](images%2Frandom_joke.png)

def callback_query(call):
- Обработчик вызова (callback)

def compliment_rend(message, COMPLIMENTS):
- Функция вызывает случайный комплимент из списка COMPLIMENTS
- ![casual_compliment.png](images%2Fcasual_compliment.png)

def coin_rend(message, MONETKA):
- Функция подбрасывает монетку
- ![flip_coin.png](images%2Fflip_coin.png)