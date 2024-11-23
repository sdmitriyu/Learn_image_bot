import telebot
from PIL import Image, ImageOps
import io
from telebot import types
import random
from conf import TOKEN
from data import JOKES, COMPLIMENTS, MONETKA

bot = telebot.TeleBot(TOKEN)
user_states = {}  # Хранение информации о пользователях


# Обработчик команды /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пожалуйста, отправь мне фото.")


# Обработчик фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]  # Берем самое большое фото
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)

    # Сохраняем информацию о фото
    user_states[message.chat.id] = {'photo': photo.file_id, 'ascii_chars': None}

    # Запрашиваем набор символов для ASCII-арта
    bot.reply_to(message, "Введите набор символов, который будет использоваться для создания ASCII-арта:")
    bot.register_next_step_handler(message, set_ascii_chars)


# Функция для установки пользовательских символов
def set_ascii_chars(message):
    user_states[message.chat.id]['ascii_chars'] = message.text
    bot.reply_to(message, "Ваш набор символов сохранен! Выберите действие:", reply_markup=get_options_keyboard())


# Функция создания клавиатуры с опциями
def get_options_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Pixelate", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII Art", callback_data="ascii")
    negative_btn = types.InlineKeyboardButton('Negative', callback_data='negative')
    reflection_horizontal_btn = types.InlineKeyboardButton('Reflection_horizontal',
                                                           callback_data='reflection_horizontal')
    reflection_vertical_btn = types.InlineKeyboardButton('Reflection_vertical', callback_data='reflection_vertical')
    heat_map_btn = types.InlineKeyboardButton('Тепловая карта', callback_data='Heat map')
    resize_for_sticker_btn = types.InlineKeyboardButton('Изготовление стикера', callback_data='making_sticker')
    random_jokes_btn = types.InlineKeyboardButton('Случайная шутка', callback_data='random_jokes')
    random_compliments_btn = types.InlineKeyboardButton('Случайный комплимент', callback_data='Random_Compliment')
    randon_coin_btn = types.InlineKeyboardButton('Подбтосить монетку', callback_data='Flip a Coin')
    keyboard.add(pixelate_btn, ascii_btn, negative_btn)
    keyboard.add(reflection_horizontal_btn, reflection_vertical_btn)
    keyboard.add(heat_map_btn, resize_for_sticker_btn)
    keyboard.add(random_jokes_btn, random_compliments_btn)
    keyboard.add(randon_coin_btn)
    return keyboard


# Обработчик нажатий на кнопки клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Огрубляем ваше изображение...")
        pixelate_and_send(call.message)
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Преобразуем ваше изображение в ASCII арт...")
        ascii_and_send(call.message)
    elif call.data == 'negative':
        bot.answer_callback_query(call.id, 'Делаем из фотографии негатив...')
        negative_photo(call.message)
    elif call.data == 'reflection_horizontal':
        bot.answer_callback_query(call.id, 'Отражаем изображение по горизонтали')
        mirror_image(call.message, direction='horizontal')
    elif call.data == 'reflection_vertical':
        bot.answer_callback_query(call.id, 'Отражаем изображение по вертикали')
        mirror_image(call.message, direction='vertical')
    elif call.data == 'Heat map':
        bot.answer_callback_query(call.id, 'Создаём тепловую карту')
        convert_to_heatmap(call.message)
    elif call.data == 'making_sticker':
        bot.answer_callback_query(call.id, 'Изготавливаю стикер на основе вашего изображения')
        resize_for_sticker(call.message)
    elif call.data == 'random_jokes':
        bot.answer_callback_query(call.id, 'Случайная шутка')
        jokes_rend(call.message, JOKES)
    elif call.data == 'Random_Compliment':
        bot.answer_callback_query(call.id, 'Случайный комплимент')
        compliment_rend(call.message, COMPLIMENTS)
    elif call.data == 'Flip a Coin':
        bot.answer_callback_query(call.id, 'Подбрасываем монетку')
        coin_rend(call.message, MONETKA)


# Функция преобразования изображения в ASCII и отправки пользователю
def ascii_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)
    ascii_chars = user_states[message.chat.id]['ascii_chars']

    if ascii_chars:
        src_ascii_art = image_to_ascii(image_stream, ascii_chars)
        bot.send_message(message.chat.id, f"<pre>{src_ascii_art}</pre>", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "Набор символов не установлен.")


# Функция преобразования изображения в ASCII с использованием пользовательских символов
def image_to_ascii(image_stream, ascii_chars, new_width=40):
    image = Image.open(image_stream).convert('L')
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(aspect_ratio * new_width * 0.55)
    img_resized = image.resize((new_width, new_height))
    img_str = pixels_to_ascii(img_resized, ascii_chars)
    img_width = img_resized.width
    max_characters = 4000 - (new_width + 1)
    max_rows = max_characters // (new_width + 1)
    ascii_art = ""

    for i in range(0, min(max_rows * img_width, len(img_str)), img_width):
        ascii_art += img_str[i:i + img_width] + "\n"

    return ascii_art


# Функция преобразования пикселей изображения в ASCII-символы с пользовательским набором
def pixels_to_ascii(image, ascii_chars):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ascii_chars[pixel * len(ascii_chars) // 256]
    return characters


# Функция огрубления изображения и отправки пользователю
def pixelate_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)

    # Загружаем изображение
    image = Image.open(image_stream)

    # Огрубляем изображение (можно изменить параметры для различной огрубленности)
    pixelated_image = image.resize((image.width // 8, image.height // 8), resample=Image.NEAREST)
    pixelated_image = pixelated_image.resize(image.size, Image.NEAREST)

    # Сохраняем результат в поток
    output_stream = io.BytesIO()
    pixelated_image.save(output_stream, format="JPEG")
    output_stream.seek(0)

    # Отправляем изображение обратно в чат
    bot.send_photo(message.chat.id, output_stream, caption="Ваше изображение огрублено!")


# Функция для создания негатива изображения
def negative_photo(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)

    # Загружаем изображение
    image = Image.open(image_stream)

    # Применяем инверсию
    negative_image = ImageOps.invert(image.convert("RGB"))  # Преобразуем в RGB, если нужно

    # Сохраняем результат в поток
    output_stream = io.BytesIO()
    negative_image.save(output_stream, format="JPEG")
    output_stream.seek(0)

    # Отправляем изображение обратно в чат
    bot.send_photo(message.chat.id, output_stream, caption="Ваше изображение в негативе!")


# Функция отражения изображения
def mirror_image(message, direction):
    horizontal_image = None
    vertical_image = None

    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)

    # Загружаем изображение
    image = Image.open(image_stream)

    if direction == 'horizontal':
        # Отражение по горизонтали (лево-право)
        horizontal_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        output_image = horizontal_image  # Сохраняем отраженное изображение
    elif direction == 'vertical':
        # Отражение по вертикали (вверх-вниз)
        vertical_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        output_image = vertical_image  # Сохраняем отраженное изображение
    else:
        raise ValueError("Direction must be 'horizontal' or 'vertical'")

    # Сохраняем результирующее изображение в байтовый поток
    output_stream = io.BytesIO()
    output_image.save(output_stream, format="JPEG")
    output_stream.seek(0)  # Устанавливаем указатель потока на начало
    bot.send_photo(message.chat.id, output_stream)  # Отправляем фото пользователю


# Преобразование изображения в тепловую карту
def convert_to_heatmap(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)

    # Загружаем изображение
    image = Image.open(image_stream).convert('L')

    # создаём тепловую карту
    heat_map_image = ImageOps.colorize(image, 'blue', 'red')

    # Сохраняем результирующее изображение в байтовый поток
    output_stream = io.BytesIO()
    heat_map_image.save(output_stream, format="JPEG")
    output_stream.seek(0)  # Устанавливаем указатель потока на начало
    bot.send_photo(message.chat.id, output_stream)  # Отправляем фото пользователю


# Изменяем размера изображения для стикера
def resize_for_sticker(message):
    new_width = None
    new_height = None

    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)

    # Загружаем изображение
    image = Image.open(image_stream).convert('RGB')

    # Адаптируем размер изображения для использования в качестве стикера
    width, height = image.size
    if width >= height:
        new_width = 125
        new_height = int(new_width * height / width)
    elif height >= width:
        new_height = 125
        new_width = int(new_height * width / height)
    elif height == width:
        image_resize = image.resize((125, 125), Image.LANCZOS)

    image_resize = image.resize((new_width, new_height), Image.LANCZOS)

    # Отправляем стикер пользователю
    output_stream = io.BytesIO()
    image_resize.save(output_stream, format="JPEG")
    output_stream.seek(0)  # Устанавливаем указатель потока на начало
    bot.send_photo(message.chat.id, output_stream)  # Отправляем фото пользователю


# Функция вызывает случайную шутку из списка JOKES
def jokes_rend(message, JOKES):
    joke = random.choice(JOKES)
    bot.reply_to(message, joke)


# Обработчик вызова (callback)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    jokes_rend(call.message, JOKES)


# Функция вызывает случайный комплимент из списка COMPLIMENTS
def compliment_rend(message, COMPLIMENTS):
    compliment = random.choice(COMPLIMENTS)
    bot.reply_to(message, compliment)


# Обработчик вызова (callback)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    jokes_rend(call.message, COMPLIMENTS)


# Функция подбрасывает монетку
def coin_rend(message, MONETKA):
    coin = random.choice(MONETKA)
    bot.reply_to(message, coin)


# Обработчик вызова (callback)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    coin_rend(call.message, MONETKA)


# Запуск бота
bot.polling()
