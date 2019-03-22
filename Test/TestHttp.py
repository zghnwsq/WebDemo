# coding:utf8

from TestCore.Http import *

url = 'https://api.caiyunapp.com/v2/aJkb6gTZrkEqnAQh/121.544379,31.221517/realtime?unit=metric:v2'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
          'Accept-Encoding': 'gzip, deflate, br'
          }
http = Http()
res = http.get(url, headers=header)
print(res)
print(dict(http.get_response_headers())['Content-Type'])
print(http.get_response_text())
print(http.get_res_by_json_path('$.result.temperature'))

