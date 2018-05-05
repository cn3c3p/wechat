


import requests

f = open('info')

for item in f :
    data = item.split(' ')
    res = {
        'name':data[0],
        'url':data[1],
        'psd':data[2],
        'money':data[3]
    }
    url =  'http://0.0.0.0:8080/addmovie'
    requests.get(url=url,params=res)
