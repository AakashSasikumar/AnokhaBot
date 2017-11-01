
import telepot
import time
import urllib3
import Bot
from config import *

proxy_url = "http://proxy.server:3128"
# telepot.api._pools = {
#     'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
# }
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(BOT_TOKEN)
prevText = {}
prevReply = {}
people = []


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        if chat_id not in people:
            bot.sendMessage(chat_id, "Hello!  You seem to be a new face, allow me to introduce myself. I am anokhaBot I'm an \
                                      artificial agent that can tell you anything about Anokha. I'm still learning a lot about \
                                      anokha so it would be very helpful if you type /wrong whenever I go wrong somewhere and I promise to get better next time.")
            people.append(chat_id)
        if msg["text"] == "/wrong":
            with open("errors.txt", "a") as file:
                writeData = "cid-" + str(chat_id) + "-txt-" + str(prevText[chat_id]) + "-rep-" + str(prevReply[chat_id]) + "\n"
                file.write(writeData)
                return
        reply = Bot.response(msg["text"])
        prevText[chat_id] = msg["text"]
        prevReply[chat_id] = reply
        bot.sendMessage(chat_id, reply)
        print(prevReply, prevText)

bot.message_loop(handle)

print('Listening ...')
while 1:
    time.sleep(10)
