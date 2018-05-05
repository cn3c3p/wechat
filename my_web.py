# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
 Created by howie.hu at 21/01/2018.
"""
import aiohttp
import random

from sanic import Sanic
from sanic.exceptions import NotFound


from sanic.response import html, json, redirect ,text

from sanic_mongo import Mongo

import time

import gensim
from jieba import analyse

new_model = gensim.models.Word2Vec.load('news_12g_baidubaike_20g_novel_90g_embedding_64.model')


def get_vector(str):
    # 将传入的文本投入词向量空间

    tfidf = analyse.extract_tags
    num = 0
    items = tfidf(str)
    # 输出抽取出的关键词
    temp = new_model['好玩'] - new_model['好玩']  # 初始化一个空列表

    for item in items:
        try:
                temp = temp + new_model[item]
                num = num + 1  # 记入总数
        except:
            pass
    return (temp / num)




app = Sanic()


mongo_uri = "mongodb://{host}:{port}/{database}".format(
    database='wechat',
    port=27017,
    host='localhost'
)

Mongo.SetConfig(app, test=mongo_uri)
Mongo(app)

@app.route("/")
async def post_json(request):
    docs = 'hello'
    print (request.args)

    return html(docs)

#生成短链定义　http://0.0.0.0:8080/addmovie?name=123&psd=123&url=123
@app.route("/addmovie")
async def post_json(request):
    matrix = await get_vector(request.args.get('name'))
    data = {
        'name': request.args.get('name'),
        'money': request.args.get('money',0),
        'url': request.args.get('url'),
        'password':request.args.get('psd'),
        'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
        'matrix': matrix
    }
   # print (data['name'])

    docs = await app.mongo['test']['movie'].update({'name':data['name']},data,True)
    #if utf - 8  use text  if js  json

    return html(docs)



#生成短链定义　http://0.0.0.0:8080/session?uid=123&name=123&movie=123
"""
每一次的ＰＯＳＴ 把用户记录并且记录下回话请求
"""
@app.route("/session")
async def post_json(request):
    moive = request.args.get('movie')
    time_now = time.strftime("%Y-%m-%d %X", time.localtime())

    session_data = {
        'name':moive,
        'time':time_now
    }

    uesr_data = {
        'uid':request.args.get('uid'),
        'name': request.args.get('name'),
        'movie':[session_data],
        'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
    }

   # print (data['game'])

    tar = await app.mongo['test']['movie'].find({'name':moive}).to_list(length=1)
    try:
        res  = tar.pop()
        print (res)
        docs = await app.mongo['test']['session'].find({'uid':uesr_data['uid']}).to_list(length=1)

        try :
            temp = docs.pop()
            temp['movie'].append(session_data)
        except:
            temp = uesr_data
        finally:
            docs = await app.mongo['test']['session'].update({'uid':uesr_data['uid']},temp,True)

        print (uesr_data)
        return html(res)
    except:
        return html('not finds')






@app.exception(NotFound)
def ignore_404s(request, exception):
    return redirect('/')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
