
from wxpy import *

import requests
bot = Bot()
bot.enable_puid('wxpy_puid.pkl')

# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('您好，需要什么电影可以直接发送电影名字哦')

@bot.register(msg_types=TEXT)
def print_others(msg):
    print(msg)
    data = str(msg).split(" : ")
    user_name = data[0]
    print (user_name)
    user_movie = data[1].split(" (Text)")[0]
    my_friend = bot.friends().search(user_name)[0]
    user_piud = my_friend.puid
    res = "http://0.0.0.0:8080/session?uid={}&name={}&movie={}".format(
        user_piud,user_name,user_movie
    )
    my_friend.send(res)


embed()
#bot.file_helper.send(requests.get('http://0.0.0.0:8080/session',params=res).text)

