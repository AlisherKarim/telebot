import telebot
import requests
from bs4 import BeautifulSoup
from listofregions import reg, times

mybot = telebot.TeleBot("1036287869:AAGpBPiZ4xkrGuVHwK7LRShbOxzOrr56WRU")
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('hello', 'I\'ve an idea')
key2 = telebot.types.ReplyKeyboardMarkup(True, True)
key2.row('almaty', 'atyrau')
markup = telebot.types.ForceReply()

#=========================================================================================
@mybot.message_handler(commands=['start'])
def start_message(message):
    mybot.send_message(message.chat.id, "hello again nigga", reply_markup=keyboard1)

#==========================================================================================

@mybot.message_handler(commands=['find'])
def find_time(message):
    sent = mybot.send_message(message.chat.id, "Send me the Name of the place, ex. Almaty")
    mybot.register_next_step_handler(sent, send_found_time)


def send_found_time(message):
    mybot.send_message(message.chat.id, "searching for " + message.text + '...')
    quote_page = "https://www.timeanddate.com/worldclock/kazakhstan/"+message.text
    response = requests.get(quote_page)
    soup = BeautifulSoup(response.content, 'html.parser')
    time_box = soup.find('span', attrs={'id':'ct'})
    if time_box:
        found_time = time_box.text.strip()
        mybot.send_message(message.chat.id, found_time)
    else:
        quote_page = "https://www.timeanddate.com/worldclock/kazakstan/" + message.text
        response = requests.get(quote_page)
        soup = BeautifulSoup(response.content, 'html.parser')
        time_box = soup.find('span', attrs={'id': 'ct'})
        if time_box:
            found_time = time_box.text.strip()
            mybot.send_message(message.chat.id, found_time)
        else:
            mybot.send_message(message.chat.id, "couldn't find, sorry")

#============================================================================================


@mybot.message_handler(commands=['ntime'])
def ntime_q(message):
    sent = mybot.send_message(message.chat.id, "Please select your Region...", reply_markup=key2)
    mybot.register_next_step_handler(sent, ntime_region)


def ntime_region(message):
    keycity = telebot.types.ReplyKeyboardMarkup(True, True)
    global regionname
    regionname = message.text
    for i in reg[message.text]:
        keycity.add(i)
    sent = mybot.send_message(message.chat.id, "Select location...", reply_markup=keycity)
    mybot.register_next_step_handler(sent, finding_time)
    telebot.types.ReplyKeyboardRemove()


def finding_time(message):
    mybot.send_message(message.chat.id, "Searching...")
    query_link = 'https://namaz.kuran.kz/en/'+ regionname +'/'+message.text
    response = requests.get(query_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    tanbox = soup.find_all('div', attrs={'class':'time'})
    print(tanbox)
    if tanbox:
        for i in range(len(tanbox)):
            mybot.send_message(message.chat.id, times[i] + " " + tanbox[i].text)
    else:
        mybot.send_message(message.chat.id,"seems you typed incorrectly... try again by /ntime and use only keyboard options")
#=============================================================================================


@mybot.message_handler(content_types='text')
def bad_request_m(message):
    mybot.send_message(message.chat.id,"try to use commands first, I can't understand you without them :( ")




@mybot.message_handler(content_types=['sticker'])
def send_info(message):
    mybot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAM7XpgPmhxI6zrrYBkhZuekLw0XiV0AAlcAAxCS-BpxKS4vStIeHBgE') #sending ers' sticker

mybot.polling()