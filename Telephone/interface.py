import telebot
from telebot import types
import logger as lg

bot = telebot.TeleBot()

@bot.message_handler(commands=['start'])
def start(message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=True)
    print_all = types.KeyboardButton('Вывести все записи.')
    find_name = types.KeyboardButton('Найти запись.')
    edit_name = types.KeyboardButton('Изменить запись.')
    keyboard_markup.add(print_all, find_name, edit_name)
    bot.send_message(message.chat.id, 'Добрый день!', reply_markup=keyboard_markup)

@bot.message_handler(content_types=['text'])
def Controller(message):
    t = message.text
    if t == 'Вывести все записи.':
        lg.logging.info('user has selected to print all entries')
        bot.register_next_step_handler(message, print_all_to_console)
    if t == 'Найти запись.':
        lg.logging.info('user has selected entry search')
        bot.send_message(message.chat.id, 'Введите имя:')
        bot.register_next_step_handler(message, find_name)
    if t == 'Изменить запись.':
        lg.logging.info('user has selected change entry')
        bot.send_message(message.chat.id, 'Введите имя:')
        bot.register_next_step_handler(message, Edit_Entry)

@bot.message_handler(commands=['print'])
def print_all_to_console(message):
    with open('employees.csv', encoding="utf-8") as data:
        f = data.read()
        bot.send_message(message.chat.id, f)    
    
def find_name(message):
    name = message.text
    try:
        bot.send_message(message.chat.id, name)
        with open('employees.csv', encoding="utf-8") as data:
            for line in data:
                if name in line:
                    bot.send_message(message.chat.id, line)
                    lg.logging.info(f'User entered: {line}')
    except:
        bot.send_message(message.chat.id, 'не найдено')
        
lines = []
new_number = 0
gl_name = ''
new_num_in = ''

def Edit_Entry(message):
    global gl_name
    gl_name = message.text
    lg.logging.info(f'User entered: {gl_name}')
    lines = []
    with open('employees.csv', 'r', encoding="utf-8") as data:
            for line in data:
                if not gl_name in line: 
                    lines += line
                else:
                    bot.send_message(message.chat.id, line) 
                    bot.send_message(message.chat.id, "Нометр элемента для замены: ")
                    bot.register_next_step_handler(message, edit_el)

def edit_el(message):
    global new_number
    new_number = int(message.text)
    lg.logging.info(f'User entered: {new_number}')
    bot.send_message(message.chat.id, "На что заменить?")
    bot.register_next_step_handler(message, edit_past)
    
def edit_past(message):
    global new_number
    global lines
    global gl_name
    global new_num_in
    new_num_in = message.text
    lg.logging.info(f'User entered: {new_num_in}')
    with open('employees.csv', 'r', encoding="utf-8") as data:
        for line in data:
            if not gl_name in line: 
                lines += line
            else:
                line = line.split(", ")
                line[new_number - 1] = new_num_in
                line = ", ".join(line)
                lines += line

    with open('employees.csv', 'w', encoding="utf-8") as data:
            data.writelines(lines)
    bot.send_message(message.chat.id, 'Изменение произведено...')

bot.polling(none_stop=True)



