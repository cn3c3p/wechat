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

app = Sanic()
import Levenshtein

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
    data = {
        'name': request.args.get('name'),
        'money': request.args.get('money',0),
        'url': request.args.get('url'),
        'password':request.args.get('psd'),
        'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
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
        res = ['我没有找到你需要的电影，下列电影是否有您需要的，若是请将其复制发送']

        datas = await app.mongo['test']['movie'].find().to_list(10000)

        for data in datas:
            if Levenshtein.distance(data['name'],session_data['name']) < 4 :
                res.append(data['name'])
        return (html(res))


@app.exception(NotFound)
def ignore_404s(request, exception):
    return redirect('/')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
