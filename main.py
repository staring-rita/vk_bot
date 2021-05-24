#Импортировали библиотеку vk_api (pip install vka_pi)
import vk_api
from vk_api import longpoll
#Дотсали из библиотеки две функции
from vk_api.longpoll import VkLongPoll, VkEventType

import RPi.GPIO as GPIO
sun = [13, 19, 16]
cloud = [14, 15, 17, 18, 24, 10, 12, 26, 21]

GPIO.setmode(GPIO.BCM)
for s in sun:
    GPIO.setup(s, GPIO.OUT)
for c in cloud:
    GPIO.setup(c, GPIO.OUT)

#Переменная для хранения токена группы ВК
token = "d67ae749167c4512e35c501b24973c88aedcb70b1350fdd4764419b44331d204112292f0b132996248d0e"

keyboard = '{"buttons":[[{"action":{"type":"text","label":"включить солнце","payload":""},"color":"positive"},{"action":{"type":"text","label":"выключить солнце","payload":""},"color":"negative"}],[{"action":{"type":"text","label":"включить облако","payload":""},"color":"positive"},{"action":{"type":"text","label":"выключить облако","payload":""},"color":"negative"}],[{"action":{"type":"text","label":"включить всё","payload":""},"color":"secondary"},{"action":{"type":"text","label":"выключить всё","payload":""},"color":"primary"}]]}'

#Подключаем токен и longpoll
token_connection = vk_api.VkApi(token = token)
give = token_connection.get_api()
longpoll = VkLongPoll(token_connection)

#функция для ответа на сообщения в ЛС группы
def write_msg(id, text):
    token_connection.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard': keyboard})

#Функция формирования ответа бота
def answer(text):
    if text == 'привет' or text == 'начать':
        return 'Привет, я бот \n༼ つ ◕_◕ ༽つ'
    elif text == 'как дела?':
        return 'Хорошо, а как твои?'
    elif text == "включить облако":
        for c in cloud:
            GPIO.output(c, GPIO.HIGH)
        return('я включил облако')
    elif text == "выключить облако":
        for c in cloud:
            GPIO.output(c, GPIO.HIGH)
        return('я выключил облако')
    elif text == "включить солнце":
        for s in sun:
            GPIO.output(s, GPIO.HIGH)
        return('я включил солнце')
    elif text == "выключить солнце":
        for s in sun:
            GPIO.output(s, GPIO.HIGH)
        return('я выключил солнце')
    elif text == "включить всё":
        for s in sun:
            GPIO.output(s, GPIO.HIGH)
        for c in cloud:
            GPIO.output(c, GPIO.HIGH)
        return('я включил всё')   
    elif text == "выключить всё":
        for s in sun:
            GPIO.output(s, GPIO.HIGH)
        for c in cloud:
            GPIO.output(c, GPIO.HIGH)
        return('я выключил всё')
    else:
        return 'Мой искуственный интелект не распознал твой сообщение'

try:
    #слушаем longpool и ждём новое сообщение боту
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            #если сообщение для бота
            if event.to_me:
                #получаем текст сообщение и переводим его в нижний регистр
                message = event.text.lower()
                #получаем id пользователя
                id = event.user_id
                text = answer(message)
                write_msg(id, text)
                print(id, message, event.datetime)

                user_get=give.users.get(user_ids = (id))
                print(user_get)
                first_name=user_get[0]['first_name']
                last_name=user_get[0]['last_name']
                full_name=first_name+" "+last_name
                print (full_name)


except KeyboardInterrupt:
    print("Stop")
finally:
    print()