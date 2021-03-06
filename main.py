"""
Überlegungen:

Funktionen vom Bot:
    Gruppenverwaltung:
        Willkommensnachricht senden !check!
        User kicken oder bannen !check!
        Captcha !in Arbeit!
        fed aufbauen? !in Arbeit!
        andere Bots entfernen !in Arbeit!
    Kanalverwaltung:
        Aus dem Netz Infos filtern und in Gruppe senden
        aus anderen Kanälen und Gruppen infos Filtern
"""

import telebot
from random import *
from datetime import datetime
import json
zzahl = randint(1, 300)

bot_token = '<TOKEN>'
bot = telebot.TeleBot(bot_token)
bot_username = "@antifantis_hhbot"

bot.can_join_groups = True

def json_write(datta, filename='Antifantis.json'):
    with open(filename, 'w') as f:
        json.dump(datta,f,indent=4)
with open('Antifantis.json') as file:
    data = json.load(file)

fascho_info = data["info"]["fascho Info"]+'\n\n'
schwurbel_info = data["info"]["schwurbel Info"]+'\n\n'
antifa_info = data["info"]["antifa Info"]+'\n\n'
corona_hinweis = "Denkt an Masken und Abstände, seid solidarisch!\n\n" \
                 "Wenn ihr Corona-Symptome habt bleibt bitte zuhause! Egal wie wichtig das Thema ist! ✊\n\n"
emojis = "✊🏳️‍🌈🏴🚩🐘"

@bot.message_handler(commands=['set_fascho'])
def set_fascho(message):
    command = message.text.split()[0]
    data["info"]["fascho Info"] = message.text[len(command) + 1:]
    json_write(data)
    bot.reply_to(message, 'Gespeichert:\n\n' + data["info"]["fascho Info"])
@bot.message_handler(commands=['set_antifa'])
def set_antifa(message):
    command = message.text.split()[0]
    data["info"]["antifa Info"] = message.text[len(command) + 1:]
    json_write(data)
    bot.reply_to(message, 'Gespeichert:\n\n' + data["info"]["antifa Info"])
@bot.message_handler(commands=['set_schwurbel'])
def set_schwurbel(message):
    command = message.text.split()[0]
    data["info"]["schwurbel Info"] = message.text[len(command) + 1:]
    json_write(data)
    bot.reply_to(message, 'Gespeichert:\n\n' + data["info"]["schwurbel Info"])

# Regeln
@bot.message_handler(commands=['rules'])
def send_rules(message):
    bot.reply_to(message, "Das sind unsere Regeln:\n\nWichtigstes: Seid solidarisch! Der Rest ist zweitrangig...\n\n"
                          "(noch in Arbeit, stimmt gerne bei der Umfrage oben ab!)")

# Befehl "/start"
@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Hi, ich bin der Bot des Antifant*innen Netzwerkes auf Telegram! Sende /help um "
                          "Hilfe zu bekommen!\n\n"
                          "✊🏳️‍🌈🏴🚩🐘")

# Befehl "/help"
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, data["bot"]["help"])

# neuer Benutzer
@bot.message_handler(content_types=['new_chat_member'])
def send_welcome(message):
    for user in message.new_chat_members:
        if user.is_bot:
            userId = user.id
            chatId = message.chat.id
            bot.kick_chat_member(chatId, userId)
        else:
            bot.reply_to(message, data["group"]["welcome"])
#    global new_time
#    new_time = datetime.now()

@bot.message_handler(commands=['welcome'])
def welcome(message):
    bot.send_message(message.chat.id, data["group"]["welcome"])

@bot.message_handler(commands=['set_welcome'])
def set_welcome(message):
    try:
        command = message.text.split()[0]
        data["group"]["welcome"] = message.text[len(command) + 1:]
        json_write(data)
        bot.reply_to(message, 'Gespeichert!')
    except Exception as ex:
        bot.reply_to(message, "Irgendwas ist schiefgelaufen")
        print(ex)

"""
@bot.message_handler(func=lambda m: True)
def check_captcha(message):
    userId = message.from_user.id
#    now = datetime.now()
    try:
        if userId == data["group"]["joined"][-1]:
            if message.text == "Fight Nazis":
                bot.reply_to(message, "Captcha Complete")
            else:
                bot.kick_chat_member(message.chat.id, userId)
    except Exception:
        pass
"""

# Benutzer geht
@bot.message_handler(content_types=['left_chat_member'])
def send_bye(message):
    bot.reply_to(message, "Und Tschüss!")

"""
# Privatsphäre-Info
@bot.message_handler(content_types=['audio', 'voice', 'video'])
def send_privcy_info(message):
    message_chat_id = message.chat.id
    if int(message_chat_id) != -1001338300583:
        bot.reply_to(message, "Wir sind ein öffentliches Netzwerk, hier könnten auch Faschos und/oder Cops "
                              "mitlesen. Gebe nichts von dir Preis, was nicht an die Cops oder an "
                              "Faschos gehen sollte! :D\n\n"
                              "✊🏳️‍🌈🏴🚩🐘")
"""

# Nutzer Kicken
@bot.message_handler(commands=['kick'])
def kick_person(message):
    try:
        userId = message.reply_to_message.from_user.id
        bot.kick_chat_member(message.chat.id, userId)
        bot.send_message(message.chat.id, message.reply_to_message.from_user.first_name + ' wurde gekickt!')
    except AttributeError:
        try:
            userId = int(message.text.split()[-1])
            bot.kick_chat_member(message.chat.id, userId)
            bot.send_message(message.chat.id, str(userId) + ' wurde geckickt!')
        except ValueError:
            bot.send_message(message.chat.id, "Du musst eine*n Nutzer*innen-ID angeben oder auf eine Nachricht der Nutzer*in antworten!")
        except Exception:
            bot.send_message(message.chat.id, "Irgendwas ist Schiefgelaufen. Versuche nochmal!")

# Aktionsinfo
@bot.message_handler(commands=['fascho'])
def send_faschoinfo(message):
    bot.reply_to(message, str(fascho_info) + str(corona_hinweis) + emojis)

@bot.message_handler(commands=['schwurbel'])
def send_schwurbelinfo(message):
    bot.reply_to(message, str(schwurbel_info) + str(corona_hinweis) + emojis)

@bot.message_handler(commands=['antifainfo'])
def send_antifainfo(message):
    bot.reply_to(message, str(antifa_info) + str(corona_hinweis) + emojis)

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, 'Faschos in Hamburg:\n'+str(fascho_info) + 'Schwurbel in Hamburg:\n'+str(schwurbel_info) + 'Antifa-Aktionen:\n'+str(antifa_info) + corona_hinweis + emojis)

# Channel
@bot.message_handler(commands=['channel'])
def send_channel_link(message):
    bot.reply_to(message, "https://t.me/antifaschismus_hh")

# Föderation Antifantis

@bot.message_handler(commands=['joinfed'])
def join_fed(message):
    chatId = message.chat.id
    groups = data["Foederation"]["groups"]
    try:
        if chatId in groups:
            bot.reply_to(message, "Gruppe ist schon in Föderation!")
        else:
            groups.append(chatId)
            bot.reply_to(message, "Föderation beigetreten!")
    except Exception as ex:
        bot.reply_to(message, "Irgendwas ist schiefgelaufen!")
        print(ex)

@bot.message_handler(commands=['leavefed'])
def leave_fed(message):
    chatId = message.chat.id
    groups = data["Foederation"]["groups"]
    try:
        if chatId in groups:
            groups.remove(chatId)
            bot.reply_to(message, "Erfolgreich ausgetreten!")
        else:
            bot.reply_to(message, "Chat gehört Föderation nicht an!")
    except Exception as ex:
        bot.reply_to(message, "Irgendwas ist schiefgelaufen!")
        print(ex)

@bot.message_handler(commands=['emojis'])
def emoji(message):
    bot.reply_to(message, emojis)

@bot.message_handler(commands=['send'])
def send_in_channel(message):
    bot.forward_message('@eintestkanalf', -1001338300583, message.reply_to_message.id)

"""
@bot.message_handler(commands=['send'])
def send_in_channel(message):
    photo = message.reply_to_message.photo
    text = message.text
    message_to_forward = photo + text
    bot.send_message('@eintestkanalf', message_to_forward)
"""
# print(new_time)

while True:
    try:
        print("Start Polling    "+str(datetime.now()))
        bot.polling()
    except Exception as e:
        print("Error, retry ...  " + str(e)+'    '+str(datetime.now()))
