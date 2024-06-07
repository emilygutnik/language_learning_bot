import telebot
import random
import json
token = '6986543206:AAFh8MS2xiHYikXXUfRIlfdjgf9e4QLU1Ho'
bot=telebot.TeleBot(token)

commands = """/start - starting bot
/info - getting information about bot
/groups - getting list of word's groups for learning
/stop - stop learning"""

groups = {
  'basic phrases':
  {
    'hello':'hola',
    'goodbye':'adiós',
    'good morning':'buen día',
    'good afternoon':'buenas tardes',
    'good night': 'buenas noches',
    'thank you':'gracias',
    'thank you very much':'muchas gracias',
    "you're welcome":'de nada',
    'see you later':'hasta luego',
    'see you soon': 'Hasta pronto',
    'see you tomorrow':'Hasta mañana',
    'how are you?':'¿Cómo estás?',
    "I'm good, how are you?":'Bien, gracias, y tu?',
    'excuse me': 'disculpame',
    'My name is...':'Me llamo...',
    'How old are you?':'¿cuántos años tiene?',
    'I am ... years old': '(yo)Tengo ... años de edad',
    "What's your name?":'¿cómo te llamas?',
    'How much is it?':'¿Cuánto cuesta?',
    'Do you speak spanish?':'¿hablas español?',
    'Where do you live':'¿Dónde vive?',
     'What time is it?':'¿qué hora es?',
    'It is ... oclock':'son las .... en punto'

  },
  'colors':{
    'white':'blanco',
    'black':'negro',
    'red':'rojo',
    'purple':'Morado',
    'violet':'violeta',
    'yellow':'amarillo',
    'green':'verde',
    'blue':'azul',
    'pink':'rosa',
    'orange':'naranja',
    'grey':'gris',
    'brown':'marrón',
    'gold':'oro',
    'silver':'plata'   
  },
  'people':{
    'friend':'amigo',
    # 'friend girl':'amiga',
    'boy':'chico',
    'girl':'chica',
    'woman':'mujer',
    'man':'hombre',
    'boyfriend':'novio',
    'girlfriend':'novia'
  },
  'family':{
    'son':'hijo',
    'daughter':'hija',
    'husband':'esposo',
    'wife':'esposa',
    'parents':'padres',
    'mother':'madre',
    'father':'padre',
    'grandparents':'abuelos',
    'grandmother':'abuela',
    'grandfather':'abuelo',
    'sister':'hermana',
    'brother':'hermano',
    'aunt':'tía',
    'uncle':'tío'

  },
  'fruits':{
    'apple':'manzana',
    'banana':'banana',
    'pineapple': 'piña',
    'melon':'melón',
    'watermelon':'sandía',
    'mango':'mango',
    'pear':'pera',
    'kiwi':'kiwi',
    'strawberry':'fresa',
    'raspberry':'frambuesa',
    'blueberry':'arándano',
    'plum':'ciruela',
    'orange':'naranja',
    'peach':'durazno',
    'avocado':'palta',
  },
  'vegetables':{
    'tomato':'tomate',
    'cucumber':'pepino',
    'papper':'pimienta',
    'onion':'cebolla',
    'carrot':'zanahoria',
    'lettuce':'lechuga',
    'eggplant':'berenjena',
    'beet':'remolacha',
    'cabbage':'repollo'
  }
}


keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
for i in groups:
  keyboard1.row(i)

keyboard2= telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('yes', 'no') 

keyboard3=telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('from English to Spanish')
keyboard3.row('from Spanish to English')
keyboard3.row('''from English to Spanish&
from Spanish to English''')

# data={}
# sent_dict_id = {}
# group=''
# mode=''
with open('users.json', 'r') as file:
  data = json.load(file)


@bot.message_handler(commands=['start'])
def start(message):
  with open('users.json', 'r') as file:
    data = json.load(file)
  data[message.chat.username]={
    'send_dict_id':[],
    'group':"",
    'mode':'',
    'learning': False,
    'words': []
  }
  with open('users.json', 'w') as file:
    json.dump(data, file, indent=2)
  # print(message)
  # print(message.chat.id)
  # bot.send_message(6454461213, 'Someone is using your bot!')
  bot.send_message(message.chat.id, 'Hi! Welcome to language learning bot.')
  bot.send_message(message.chat.id, 'choose a group to learn:\n' + '\n'.join(groups.keys()), reply_markup=keyboard1)


@bot.message_handler(commands=['info'])
def info(message):
  bot.send_message(message.chat.id, 'This bot is written by @EmilyGutnik')
  bot.send_message(message.chat.id, 'This bot is helping you to learn words in groups')
  bot.send_message(message.chat.id, commands)

@bot.message_handler(content_types=['text'])
def handletext(message):
  # global data
  with open('users.json', 'r') as file:
    data = json.load(file)
  # global sent_dict_id
  # global group
  # global mode

  if message.text in groups:
    data[message.chat.username]['group']=message.text 
    bot.send_message(message.chat.id, 'You chose group: ' + message.text)
    data[message.chat.username]['send_dict_id'].append(bot.send_message(message.chat.id, 'Wordlist:\n' + '\n'.join(['*'+key + '* - ' + value for key, value in groups[message.text].items()]), parse_mode='Markdown').message_id)
    # print(data[message.chat.username]['send_dict_id'])
    bot.send_message(message.chat.id, 'Will you start learning these words?', reply_markup=keyboard2)

  elif message.text == 'yes':
    while data[message.chat.username]['send_dict_id']:
      bot.delete_message(message.chat.id, data[message.chat.username]['send_dict_id'].pop())
    bot.send_message(message.chat.id, "Choose a learning mode", reply_markup=keyboard3)

  elif message.text in ('from English to Spanish', 'from Spanish to English', 'from English to Spanish&\nfrom Spanish to English'):
    data[message.chat.username]['mode']=message.text
    data[message.chat.username]['learning'] = True
    bot.send_message(message.chat.id, "Let's begin!")
    if data[message.chat.username]['mode']=='from English to Spanish':
      data[message.chat.username]['words'] = list(groups[data[message.chat.username]['group']].items())

    elif data[message.chat.username]['mode']=='from Spanish to English':
      data[message.chat.username]['words'] = []
      for i in list(groups[data[message.chat.username]['group']].items()):
        data[message.chat.username]['words'].append((i[1], i[0]))

    else: 
      data[message.chat.username]['words'] = []
      for i in list(groups[data[message.chat.username]['group']].items()):
        i = list(i)
        random.shuffle(i)
        data[message.chat.username]['words'].append((i[0], i[1]))


    random.shuffle(data[message.chat.username]['words'])
    data[message.chat.username]['word'], data[message.chat.username]['translation']=data[message.chat.username]['words'].pop(0)
    bot.send_message(message.chat.id, 'translate ' + data[message.chat.username]['word'])


  elif message.text == data[message.chat.username]['translation']:
    bot.send_message(message.chat.id, "You're right!")
    if data[message.chat.username]['words']:
      data[message.chat.username]['word'], data[message.chat.username]['translation']=data[message.chat.username]['words'].pop(0)
      bot.send_message(message.chat.id, 'translate ' + data[message.chat.username]['word'])
    else:
      bot.send_message(message.chat.id, 'Congratulations, you have learnt all words in this group!✨')
  else: 
    bot.send_message(message.chat.id, "You're not right!")
    data[message.chat.username]['words'].append((data[message.chat.username]['word'], data[message.chat.username]['translation']))
    data[message.chat.username]['words']
    data[message.chat.username]['word'], data[message.chat.username]['translation']=data[message.chat.username]['words'].pop(0)
    bot.send_message(message.chat.id, 'translate ' + data[message.chat.username]['word'])
  with open('users.json', 'w') as file:
    json.dump(data, file, indent=2)

bot.polling()
