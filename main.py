import os
from typing import final
from dotenv import load_dotenv
import telebot
from telebot import types
import logging
import sqlite3
import sys
import threading
import time
from database import DB_PATH, init_db, save_applicant
init_db()
logging.basicConfig(level=logging.INFO)
load_dotenv()
API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

user_state = {}
user_data = {}

@bot.message_handler(commands=['getdb'])
def send_db_file(message):
    try:
        with open(DB_PATH, 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

#start command
@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, "Добро пожаловать! Я чат-бот ГАУ ТО «Тобольский межрайонный центр ветеринарии».")
  markup = types.InlineKeyboardMarkup()
  #each button has a callback data that is used to identify the button when its pressed
  button1 = types.InlineKeyboardButton("Чем мы занимаемся и какова наша миссия", callback_data="button1")
  button2 = types.InlineKeyboardButton("Преимущества работы в нашем учреждении", callback_data="button2")
  button3 = types.InlineKeyboardButton("Истории успеха ветеринарных специалистов", callback_data="button3")
  button4 = types.InlineKeyboardButton("Как присоединиться к нашей команде", callback_data="button4")
  #Add buttons to markup in one colomn
  markup.add(button1)
  markup.add(button2)
  markup.add(button3)
  markup.add(button4)
  bot.send_message(message.chat.id, "Выберите интересующую информацию", reply_markup=markup)
def send_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Чем мы занимаемся и какова наша миссия", callback_data="button1")
    button2 = types.InlineKeyboardButton("Преимущества работы в нашем учреждении", callback_data="button2")
    button3 = types.InlineKeyboardButton("Истории успеха ветеринарных специалистов", callback_data="button3")
    button4 = types.InlineKeyboardButton("Как присоединиться к нашей команде", callback_data="button4")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)
    bot.send_message(chat_id, "Выберите опцию", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
  if call.data == "button1":
    text = ("в целях осуществления предусмотренных законодательством  Российской  Федерации полномочий  в сфере ветеринарии.\n\n"
       "Чем мы занимаемся:\n"
       "- реализуем мероприятия по предупреждению и ликвидации заразных и иных болезней животных, включая сельскохозяйственных, домашних, зоопарковых и других животных, пушных зверей, птиц, рыб и пчел, в том числе:\n"
        "- проведение противоэпизоотических мероприятий, направленных на предупреждение и ликвидацию болезней животных;\n"
        "- вакцинация животных;\n"
        "- диагностические мероприятия, в том числе лабораторные исследования на болезни животных;\n"
        "- лечение животных;\n"
        "- проведение ветеринарно-санитарной экспертизы;\n"
        "- оформление ветеринарных сопроводительных документов.\n\n"
        "Территория обслуживания:\n" 
          "• город Тобольск;\n"
          "• Тобольский район;\n"
          "• Уватский район;\n"
          "• Вагайский район.")

    markup_restart = types.InlineKeyboardMarkup()
    restart_button = types.InlineKeyboardButton("Вернуться к списку информации", callback_data="send_main_menu")
    markup_restart.add(restart_button)

    bot.send_message(call.message.chat.id, text, reply_markup=markup_restart)

  elif call.data == "send_main_menu":
    send_main_menu(call.message.chat.id)

  elif call.data == "button2":
    with open("guarantees.jpg", "rb") as photo:
      markup_restart = types.InlineKeyboardMarkup()
      restart_button = types.InlineKeyboardButton("Вернуться к списку информации", callback_data="send_main_menu")
      markup_restart.add(restart_button)

      bot.send_photo(call.message.chat.id, photo, reply_markup=markup_restart)
        
  elif call.data == "button3":
    with open("thestory.jpg", "rb") as photo:
      bot.send_photo(call.message.chat.id, photo, caption="📌 История успеха: от ветеринарного фельдшера до директора ветеринарного учреждения\n\n"

"👨‍⚕Абрамов Иван Владимирович\n"
"Директор ГАУ ТО «Тобольский ветцентр»\n\n"

"🔹 Как была выбрана профессия:\n\n"

"— Моя мама 42 года отработала ветеринарным врачом в крупном хозяйстве, — рассказывает Иван Абрамов. — Если случался отёл или падёж скота – люди бежали к ней на помощь. С малых лет мама брала меня с собой. Я и видел, с какой заботой и любовью она помогает животным. Потом стал помогать ей – научился делать уколы и инъекции.\n"
"С детства мечтал, как мама, быть ветеринаром. Поэтому свою профессию выбрал осознанно, поступил в Курганский сельскохозяйственный техникум.\n\n")

    text = ( "🔹 Трудовая деятельность:\n\n"

"Иван Абрамов начинал как ветеринарный фельдшер в селе Чердынцево Курганской области. Через год молодого специалиста перевели на ветстанцию в г. Кургане, где он стал ведущим ветеринарным врачом. Одновременно получал высшее образование в Уральском аграрном университете.\n\n"

"Следующее место работы — ветврач Тюменской области, село Бердюжье. Переезд оказался символичным — это родина супруги Ивана Абрамова, и в этот момент учреждению срочно требовался ветеринарный врач.\n\n"
"🔹 Работа директором ГАУ ТО \«Тобольский межрайонный центр ветеринарии\»:\n\n"
                     
"Высокий профессионализм и многолетний опыт были замечены — Ивана Абрамова назначили директором учреждения. Он делится:\n\n"

"— Ветеринария не стоит на месте. Появляются новые препараты, методы лечения. Поэтому мы стараемся успевать за новшествами — изучаем литературу, повышаем квалификацию, участвуем в семинарах.\n"
"Помимо этого, делимся опытом и знаниями с коллегами. Работаем с мотивацией и любовью к делу, вкладываем душу.\n\n"

"Сегодня Иван Абрамов возглавляет успешное ветеринарное учреждение.\n\n"

"🔹 Сотрудники — главная ценность:\n\n"

"Создание дружелюбной атмосферы в коллективе — неотъемлемая часть успеха. Именно она формирует мотивацию и сплочённость:\n\n"

"«Сотрудники для меня — на первом месте. Я уважаю каждого, стараюсь проявлять заботу и внимание. Мы — одна большая семья!»")
    markup_restart = types.InlineKeyboardMarkup()
    restart_button = types.InlineKeyboardButton("Вернуться к списку информации", callback_data="send_main_menu")
    markup_restart.add(restart_button)

    bot.send_message(call.message.chat.id, text, reply_markup=markup_restart)
      
  elif call.data == "button4":
    bot.send_message(call.message.chat.id, "Присоединиться к нашей команде можно в следующих форматах:\n\n"
                     
    "Для ветспециалистов, имеющих высшее или среднее профессиональное образование, – возможность трудоустройства или включения в кадровый резерв.\n\n"
    "Для студентов – будущих ветеринарных специалистов, которые получают высшее или среднее профессиональное образование, – возможность прохождения производственной практики и (или) включения кадровый резерв.\n\n"
    "Предлагаем ответить на несколько простых вопросов, которые помогут нам узнать о вас больше и связаться с вами для дальнейшего трудоустройства, включения в кадровый резерв или прохождения производственной практики.")

    markup2 = types.InlineKeyboardMarkup()
    buttonemp1 = types.InlineKeyboardButton("Трудоустройство", callback_data="buttonemp1")
    buttonemp2 = types.InlineKeyboardButton("Включение в кадровый резерв", callback_data="buttonemp2")
    buttonemp3 = types.InlineKeyboardButton("Прохождение производственной практики", callback_data="buttonemp3")
    buttonemp4 = types.InlineKeyboardButton("Прохождение практики и кадровый резерв", callback_data="buttonemp4")
    markup2.add(buttonemp1)
    markup2.add(buttonemp2)
    markup2.add(buttonemp3)
    markup2.add(buttonemp4)

    bot.send_message(call.message.chat.id, "Какие варианты вас интересуют?", reply_markup=markup2)

    
    
  # Agreement button
  elif call.data in ["buttonemp1", "buttonemp2", "buttonemp3", "buttonemp4"]:
    markup_agreement = types.InlineKeyboardMarkup()
    markup_agreement.add(types.InlineKeyboardButton("Даю согласие ✅", callback_data="button_click"))
  
    bot.send_message(call.message.chat.id,
                     "Спасибо за интерес!\n\n"
                     "Для того, чтобы мы смогли с вами связаться, нам нужно спросить у вас согласие на обработку персональных данных:\n"
                     "[Согласие на обработку](https://docs.google.com/document/d/1V8MUnGQf-M2TcC7ujAyGCe8Qwl1bzD7ce7lhn4YzrxQ/edit?usp=sharing)",
                     parse_mode="Markdown", reply_markup=markup_agreement)

  elif call.data == "button_click":
    markup_status = types.InlineKeyboardMarkup()
    buttonstatus1 = types.InlineKeyboardButton("Ветеринарный специалист", callback_data="buttonstatus1")
    buttonstatus2 = types.InlineKeyboardButton("Студент – будущий ветеринарный специалист", callback_data="buttonstatus2")
    markup_status.add(buttonstatus1)
    markup_status.add(buttonstatus2)
    bot.send_message(call.message.chat.id, "Вы (на выбор):", reply_markup=markup_status)
  
  elif call.data == "buttonstatus1":
    markup_wet = types.InlineKeyboardMarkup()
    buttonwet1 = types.InlineKeyboardButton("Ветеринарный врач", callback_data="buttonwet1")
    buttonwet2 = types.InlineKeyboardButton("Ветеринарный фельдшер", callback_data="buttonwet2")
    markup_wet.add(buttonwet1)
    markup_wet.add(buttonwet2)
    bot.send_message(call.message.chat.id, "Выберите вашу должность:", reply_markup=markup_wet)
  elif call.data == "buttonstatus2":
    markup_student = types.InlineKeyboardMarkup()
    buttonstudent1 = types.InlineKeyboardButton("Будущий ветеринарный врач", callback_data="buttonstudent1")
    buttonstudent2 = types.InlineKeyboardButton("Будущий ветеринарный фельдшер", callback_data="buttonstudent2")
    markup_student.add(buttonstudent1)
    markup_student.add(buttonstudent2)
    bot.send_message(call.message.chat.id, "Выберите вашу специальность:", reply_markup=markup_student)

  
    # CV or questionnaire
  elif call.data in ["buttonwet1", "buttonwet2", "buttonstudent1", "buttonstudent2"]:
    markup_questionnaire = types.InlineKeyboardMarkup()
    buttonquestionnaire = types.InlineKeyboardButton("Ответить на вопросы", callback_data="buttonquestionnaire")
    markup_questionnaire.add(buttonquestionnaire)

    bot.send_message(call.message.chat.id, "Ответьте на несколько вопросов", reply_markup=markup_questionnaire)

  elif call.data == "buttonquestionnaire":
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    user_state[user_id] = "waiting_fio"
    user_data[user_id] = {}
    bot.send_message(chat_id, "Введите ваше ФИО (Фамилия Имя Отчество):")

@bot.message_handler(func=lambda m: True)
def main_handler(message):
    user_id = message.from_user.id
    state = user_state.get(user_id)

    if state == "waiting_for_resume":
        pass

    elif state == "waiting_fio":
        fio = message.text.strip()
        if len(fio.split()) != 3:
            bot.send_message(message.chat.id, "Некорректное ФИО, введите ваше ФИО еще раз.")
            return
        user_data[user_id]["fio"] = fio
        user_state[user_id] = "waiting_edu"
        bot.send_message(message.chat.id, "Укажите наименование учебного заведения:")


    elif state == "waiting_edu":
        user_data[user_id]["edu"] = message.text
        user_state[user_id] = "waiting_year"
        bot.send_message(message.chat.id, "Укажите год окончания (планируемый год окончания)")

    elif state == "waiting_year":
        try:
            year = int(message.text)
            if 1900 <= year <= 2100:
                user_data[user_id]["year"] = year
                user_state[user_id] = "waiting_age"
                bot.send_message(message.chat.id, "Укажите ваш возраст")
            else:
                bot.send_message(message.chat.id, "Пожалуйста, введите год в диапазоне от 1900 до 2100.")
        except ValueError:
            bot.send_message(message.chat.id, "Некорректный ввод. Введите год цифрами, например 2025.")


    elif state == "waiting_age":
        try:
            age = int(message.text)
            if 16 <= age <= 99:
                user_data[user_id]["age"] = age
                user_state[user_id] = "waiting_exp" 
                bot.send_message(message.chat.id, "Укажите организации, в которых работали, и стаж работы по специальности\n"
"Пример: ООО «________», 1 год")
            else:
                bot.send_message(message.chat.id, "Пожалуйста, введите возраст от 16 до 99 лет.")
        except ValueError:
            bot.send_message(message.chat.id, "Некорректный ввод. Введите возраст цифрами, например 25.")

    elif state == "waiting_exp":
        user_data[user_id]["exp"] = message.text
        user_state[user_id] = "waiting_about"
        bot.send_message(message.chat.id, "Что вы еще хотели бы рассказать о себе?")

    elif state == "waiting_about":
        user_data[user_id]["about"] = message.text
        user_state[user_id] = "waiting_contact"
        data = user_data[user_id]
        contact_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        contact_button = types.KeyboardButton("Поделиться номером телефона 📞", request_contact=True)
        contact_keyboard.add(contact_button)
        bot.send_message(message.chat.id, "Спасибо за ответы! Теперь, пожалуйста, поделитесь Вашим номером телефона:", reply_markup=contact_keyboard)
    
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.from_user.id
    contact = message.contact.phone_number
    user_data[user_id]["contact"] = contact
    user_state[user_id] = None  # Сброс состояния
    bot.send_message(message.chat.id, "Спасибо! Мы обязательно с вами свяжемся!", reply_markup=types.ReplyKeyboardRemove())

    # Сохраняем данные сразу, без задержки
    data = user_data.get(user_id)
    if data:
        applicant_data = {
            "telegram_id": user_id,
            "fio": data.get("fio"),
            "contact": data.get("contact"),
            "age": data.get("age"),
            "edu": data.get("edu"),
            "year": data.get("year"),
            "exp": data.get("exp"),
            "about": data.get("about")
        }
        try:
            save_applicant(applicant_data)
            print(f"Данные сохранены: {applicant_data}")  # Логирование
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
        finally:
            user_data[user_id] = {}

    # Отправляем финальное сообщение
    final_text = (
        "Подпишитесь на наши социальные сети, чтобы не пропустить свежие новости о деятельности учреждения "
        "и ежедневно получайте полезную информацию в сфере ветеринарии!\n\n"
        "[Ссылка на соцсети](https://vk.com/public200521064)"
    )
    markup_restart = types.InlineKeyboardMarkup()
    restart_button = types.InlineKeyboardButton("🔁 Перезапустить бота", callback_data="send_main_menu")
    markup_restart.add(restart_button)
    bot.send_message(message.chat.id, final_text, parse_mode='Markdown', reply_markup=markup_restart)


@bot.message_handler(commands=['showdb'])
def show_db(message):
    try:
        conn = sqlite3.connect("applicants.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM applicants")
        data = cur.fetchall()

        response = "Данные в БД:\n"
        for row in data:
            response += f"{row}\n"

        # Разбиваем на части, если слишком длинное сообщение
        if len(response) > 4000:
            for x in range(0, len(response), 4000):
                bot.send_message(message.chat.id, response[x:x+4000])
        else:
            bot.send_message(message.chat.id, response)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")
    finally:
        if conn:
            conn.close()





if os.path.exists("last_chat.txt"):
    with open("last_chat.txt", "r") as f:
        saved_chat_id = f.read().strip()

    if saved_chat_id:
        try:
            class FakeMessage:
                def __init__(self, chat_id):
                    self.chat = type("Chat", (), {"id": chat_id})

            fake_message = FakeMessage(int(saved_chat_id))
            start_handler(fake_message)
        except Exception as e:
            print("Ошибка при вызове start после перезапуска:", e)
        os.remove("last_chat.txt")
if __name__ == '__main__':
    while True:
        try:
            print("Бот запущен...")
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            print("Перезапуск через 10 секунд...")
            time.sleep(10)
