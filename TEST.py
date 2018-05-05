# -*- coding: utf-8 -*-

import requests

r = requests.get(url="http://0.0.0.0:8080/session?uid=123&name=123&movie=maomaom")
print (r.text)