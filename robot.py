
from wxpy import *

import requests
bot = Bot()


# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('哈哈，我自动接受了你的好友请求')

@bot.register()
def print_others(msg):
    print(msg)
    data = str(msg).split(" : ")
    user_name = data[0]
    print (user_name)
    text = data[1].split(" (Text)")[0]
    my_friend = bot.friends().search(user_name)[0]
    my_friend.send(text)


embed()
#bot.file_helper.send(requests.get('http://0.0.0.0:8080/session',params=res).text)

