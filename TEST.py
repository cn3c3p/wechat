# -*- coding: utf-8 -*-

import requests

r = requests.get(url="http://www.ygdy8.net/html/gndy/china/list_4_2.html")
print (r.text)