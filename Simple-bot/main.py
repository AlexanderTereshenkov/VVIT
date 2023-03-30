import telebot
from telebot import types
import psycopg2
from datetime import date
import datetime

conn = psycopg2.connect(
    database="timetable",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

token = '5814511530:AAGoWz_rBxdwrbnomguJqJg7_NEfdmQzPhE'
bot = telebot.TeleBot(token)
helpText = "Я бот-расписание группы БВТ2203.\nУ меня можно узнать расписание на определнный день или неделю.\n" \
           "Также попробуйте команды: /week, /mtuci"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите /help, чтобы узнать, что я умею')


@bot.message_handler(commands=['mtuci'])
def start(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')


@bot.message_handler(commands=['week'])
def start(message):
    week = get_week_count()
    even_or_odd = "Неделя №: " + str(week)
    if week % 2 == 0:
        even_or_odd += " Четная"
    else:
        even_or_odd += " Нечетная"
    bot.send_message(message.chat.id, even_or_odd)


@bot.message_handler(commands=['help'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник")
    keyboard.row("Вторник")
    keyboard.row("Среда")
    keyboard.row("Четверг")
    keyboard.row("Пятница")
    keyboard.row("Суббота")
    keyboard.row("Расписание на текущую неделю")
    keyboard.row("Расписание на следующую неделю")
    bot.send_message(message.chat.id, helpText, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def answer(message):
    week = get_week_count()
    if week % 2 == 0:
        st = "четная"
    else:
        st = "нечетная"
    if message.text.lower() == 'понедельник':
        bot.send_message(message.chat.id, make_day_string('Понедельник', st))
    if message.text.lower() == 'вторник':
        bot.send_message(message.chat.id, make_day_string('Вторник', st))
    if message.text.lower() == 'среда':
        bot.send_message(message.chat.id, make_day_string('Среда', st))
    if message.text.lower() == 'четверг':
        bot.send_message(message.chat.id, make_day_string('Четверг', st))
    if message.text.lower() == 'пятница':
        bot.send_message(message.chat.id, make_day_string('Пятница', st))
    if message.text.lower() == 'суббота':
        bot.send_message(message.chat.id, make_day_string('Суббота', st))
    if message.text.lower() == 'расписание на текущую неделю':
        bot.send_message(message.chat.id, make_week_string(st))
    if message.text.lower() == 'расписание на следующую неделю':
        if st == "четная":
            t_st = "нечетная"
        else:
            t_st = "четная"
        bot.send_message(message.chat.id, make_week_string(t_st))



def get_day_table(day, week):
    cursor.execute("SELECT s.name, tt.room_numb, tt.start_time, tc.full_name, tt.task, tt.paire_count, tt.week "
                   "FROM subject s, timetable tt, teacher tc "
                   "WHERE tt.day_name=%s AND tt.week=%s AND s.id = tt.subject AND tc.subject=s.id "
                   "AND tc.task=tt.task "
                   "ORDER BY tt.paire_count", (day, week))
    return cursor.fetchall()


#def get_week_table(week, day):
 #   cursor.execute("SELECT s.name, tt.room_numb, tt.start_time, tc.full_name, tt.task, tt.paire_count, tt.day_count "
  #                 "FROM subject s, timetable tt, teacher tc "
   #                "WHERE tt.week=%s AND tt.day_name=%s AND s.id = tt.subject AND tc.subject=s.id AND tc.task=tt.task "
    #               "ORDER BY tt.day_count, tt.paire_count", (week, day))
    #return cursor.fetchall()


def make_day_string(day, week):
    s = day + ":" + "\n"
    t = get_day_table(day, week)
    k = 1
    if len(t) == 0:
        for i in range(5):
            s += str(k) + ") " + "Пар нет"
            s += "\n"
            k += 1
    else:
        u = 0
        for i in range(5):
            if k == t[u][5]:
                s += str(k) + ") " + t[u][2] + "\n " + t[u][0] + "\n " + t[u][3] + " " + t[u][1] + "\n " + t[u][4] + "\n"
                k += 1
                if u < len(t) - 1:
                    u += 1
            else:
                s += str(k) + ") " + "Пар нет" + "\n"
                k += 1
    return s


def make_week_string(week):
    days = ['Понедельник', "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    week_s = get_week_count()
    s = "Неделя № " + str(week_s)
    s += " " + week + "\n"
    for day in days:
        s += make_day_string(day, week)
        s += '\n' + '\n'
    return s


def get_week_count():
    today = str(date.today()).split("-")
    week = datetime.date(int(today[0]), int(today[1]), int(today[2])).isocalendar().week - 4
    return week


bot.polling()
