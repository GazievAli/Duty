import telebot
import json
import os
from datetime import datetime
from keys import TOKEN, CHAT_ID

duty_list = ["Артем", "Слава", "Али"]
DATA_FILE = 'duty_data.json'

bot = telebot.TeleBot(TOKEN)


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(0)
        return 0

    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return data.get('current_duty_index', 0)
    except json.JSONDecodeError:
        save_data(0)
        return 0



def save_data(current_duty_index):
    data = {'current_duty_index': current_duty_index}
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)


def send_duty_message():
    current_duty_index = load_data()
    duty_person = duty_list[current_duty_index]
    message = f"Сегодня дежурит: {duty_person} 🧹"
    bot.send_message(CHAT_ID, message)

    next_duty_index = (current_duty_index + 1) % len(duty_list)
    save_data(next_duty_index)


@bot.message_handler(commands=['info'])
def send_duty_info(message):
    current_duty_index = load_data()
    duty_person = duty_list[current_duty_index]
    info_message = f"На этой неделе дежурит: {duty_person} 🧹"

    bot.send_message(message.chat.id, info_message)



if __name__ == "__main__":
    today = datetime.today()
    if today.weekday() == 6:
        send_duty_message()
    bot.polling(none_stop=True)
