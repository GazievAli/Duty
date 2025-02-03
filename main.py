import telebot
import json
import os
from datetime import datetime
from keys import *

DATA_FILE = 'duty_data.json'
bot = telebot.TeleBot(TOKEN)


def load_data():
    if not os.path.exists(DATA_FILE):
        data = {
            'current_duty_index': 0,
            'duty_list': ["Артем", "Слава", "Али"]
        }
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)
        return data

    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            if 'duty_list' not in data:
                data['duty_list'] = ["Артем", "Слава", "Али"]
                save_data(data)
            return data
    except json.JSONDecodeError:
        data = {
            'current_duty_index': 0,
            'duty_list': ["Артем", "Слава", "Али"]
        }
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)
        return data



def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)


def send_duty_message():
    data = load_data()
    current_duty_index = data['current_duty_index']
    duty_list = data['duty_list']

    duty_person = duty_list[current_duty_index]
    message = f"Сегодня дежурит: {duty_person} 🧹"
    bot.send_message(CHAT_ID, message)

    next_duty_index = (current_duty_index + 1) % len(duty_list)
    data['current_duty_index'] = next_duty_index
    save_data(data)


@bot.message_handler(commands=['info'])
def send_duty_info(message):
    data = load_data()
    current_duty_index = data['current_duty_index']
    duty_list = data['duty_list']

    duty_person = duty_list[current_duty_index]
    info_message = f"На этой неделе дежурит: {duty_person} 🧹"

    bot.send_message(message.chat.id, info_message)


@bot.message_handler(commands=['add'])
def add_duty_person(message):
    try:
        new_person = message.text.split(maxsplit=1)[1].strip()
        if not new_person:
            raise ValueError("Имя не указано.")

        data = load_data()
        duty_list = data['duty_list']

        duty_list.append(new_person)
        data['duty_list'] = duty_list
        save_data(data)

        bot.reply_to(message, f"✅ {new_person} добавлен(а) в список дежурных.")
    except IndexError:
        bot.reply_to(message, "❌ Укажите имя нового дежурного. Например: /add Иван")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")


@bot.message_handler(commands=['remove'])
def remove_duty_person(message):
    try:
        person_to_remove = message.text.split(maxsplit=1)[1].strip()
        if not person_to_remove:
            raise ValueError("Имя не указано.")

        data = load_data()
        duty_list = data['duty_list']
        if person_to_remove in duty_list:
            duty_list.remove(person_to_remove)
            data['duty_list'] = duty_list
            save_data(data)
            bot.reply_to(message, f"✅ {person_to_remove} удалён(а) из списка дежурных.")
        else:
            bot.reply_to(message, f"❌ {person_to_remove} не найден(а) в списке дежурных.")
    except IndexError:
        bot.reply_to(message, "❌ Укажите имя дежурного для удаления. Например: /remove Иван")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")


if __name__ == "__main__":
    today = datetime.today()
    if today.weekday() == 6:
        send_duty_message()
    bot.polling(none_stop=True)