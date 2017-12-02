
import telepot
import time
import urllib3
from config import *
import json
import Bot
import tflearn
import tensorflow as tf
import os
import _thread
import subprocess
import Main

proxy_url = "http://proxy.server:3128"
# telepot.api._pools = {
#     'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
# }
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(BOT_TOKEN)
prevText = {}
prevReply = {}
permAdmin = [361154639]
people = [361154639]
admin = [361154639]


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':

        if chat_id in admin:
            if msg['text'] == '/train':
                Main.train()
                # time.sleep(10)
                subprocess.Popen(['python', 'Restart.py'])
                Bot.sendMessage(chat_id, "Training is done! Wait for 15 seconds for restart.")
                _thread.interrupt_main()

            if msg['text'] == '/errortxt':
                with open('errors.txt') as s:
                    for line in s:
                        bot.sendMessage(chat_id, line)

            if 'inc' in msg['text'][:4].lower():
                newContext = msg['text'][4:]
                bot.sendMessage(chat_id, "Going to add " + newContext + " as a new context")
                with open("context.json") as jsonData:
                    context = json.load(jsonData)
                dicti = {'tag': newContext, 'patterns': [], 'responses': []}
                context['contexts'].append(dicti)
                with open('context.json', 'w') as j:
                    json.dump(context, j)
                bot.sendMessage(chat_id, "Context added")

            if 'ap' in msg['text'][:3].lower():
                content = msg['text'][3:]
                context = content.split('-')[0]
                pattern = content.split('-')[1]
                with open('context.json') as j:
                    data = json.load(j)
                for tags in data['contexts']:
                    if tags['tag'] == context:
                        tags['patterns'].append(pattern)
                with open('context.json', 'w') as j:
                    json.dump(data, j)
                bot.sendMessage(chat_id, "Pattern " + pattern + " added to context " + context)

            if 'ar' in msg['text'][:3].lower():
                content = msg['text'][3:]
                context = content.split('-')[0]
                response = content.split('-')[1]
                with open('context.json') as j:
                    data = json.load(j)
                for tags in data['contexts']:
                    if tags['tag'] == context:
                        tags['responses'].append(response)
                with open('context.json', 'w') as j:
                    json.dump(data, j)
                bot.sendMessage(chat_id, "Response " + response + " added to context " + context)

            if 'adm' in msg['text'][:4].lower():
                chatID = int(msg['text'][4:])
                if chatID not in permAdmin:
                    permAdmin.append(chatID)
                if chatID not in admin:
                    admin.append(chatID)
                bot.sendMessage(chat_id, "Chat ID " + chatID + " is not an admin")
                bot.sendMessage(chatID, "You have been made an admin")

            if 'rmadm' in msg['text'][:6].lower():
                admin.remove(chat_id)
                people.remove(chat_id)
                bot.sendMessage(chat_id, "You are not an admin anymore. You can become an admin once again by typing /makemeadmin")
                return
            bot.sendMessage(chat_id, "Greetings admin. What do you wanna do?\ninsertNewContext(inc)\n/train\naddPattern(ap)\n/errortxt\naddResponse(ar)\naddAdmin(adm)\nremoveAdmin(rmadm)")

        if chat_id not in people:
            bot.sendMessage(chat_id, "Hello!  You seem to be a new face, allow me to introduce myself. I am anokhaBot I'm an \
                                      artificial agent that can tell you anything about Anokha. I'm still learning a lot about \
                                      anokha so it would be very helpful if you type /wrong whenever I go wrong somewhere and I promise to get better next time.")
            people.append(chat_id)
        if msg["text"] == "/wrong" or msg['text'] == '\wrong':
            with open("errors.txt", "a") as file:
                writeData = "cid-" + str(chat_id) + "-txt-" + str(prevText[chat_id]) + "-rep-" + str(prevReply[chat_id]) + "\n"
                file.write(writeData)
                return
        if chat_id not in admin:
            if msg['text'] == '/makemeadmin' and chat_id in permAdmin:
                admin.append(chat_id)
                bot.sendMessage(chat_id, "You are now an admin")
                return
            reply = Bot.response(msg["text"])
            prevText[chat_id] = msg["text"]
            prevReply[chat_id] = reply
            bot.sendMessage(chat_id, reply)
            print(prevReply, prevText)


def msgToAdmin(chatID):
    bot.sendMessage(chatID, """Greetings admin. What do you wanna do?\ninsertNewContext(inc-context name) /
                               \n/train\naddPattern(ap-context name-question)\n/errortxt\naddResponse(ar-context name-response)
                               \naddAdmin(adm-chat id)\nremoveAdmin(rmadm(you won't be admin anymore))\n
                               You can type /makemeadmin when to become an admin again.""")
bot.message_loop(handle)

print('Listening ...')
while 1:
    time.sleep(10)
