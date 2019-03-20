# coding:utf8

import requests
import json
import jsonpath


class Http:

    def __init__(self):
        self.session = requests.session()
        self.url = ''
        self.response = None
        self.headers = {}
        self.cookie = {}
        self.body = ''
        self.js = ''

    def __set_url_params(self, dic):
        """
        将字典形式的url参数拼接到url中
        :param dic: 字典形式的url参数
        :return: 拼接后的url
        """
        if type(dic) != dict:
            raise Exception("Wrong type! Dict required!")
        url_params = '?'
        for key in dic.keys():
            url_params = url_params + '&' + key + '=' + dic[key]
        self.url += url_params

    def set_headers(self, hds):
        """
        设置请求的headers，原有headers将被清空
        :param hds: 字典形式的headers
        :return:
        """
        if type(hds) != dict:
            raise Exception("Wrong type! Dict required!")
        else:
            self.headers.clear()
            self.headers = hds

    def add_headers(self, headers):
        """
        添加/更新请求的headers，保持原有键值
        :param headers: 字典形式的headers
        :return:
        """
        if type(headers) != dict:
            raise Exception("Wrong type! Dict required!")
        else:
            for key in headers.keys():
                self.headers[key] = headers[key]

    def remove_headers(self, headers):
        """
        删除部分headers
        :param headers: 待删除headers的key
        :return:
        """
        keys = headers.split(sep=',')
        for key in keys:
            del self.headers[key]

    def clear_headers(self):
        """
        清空headers
        :return:
        """
        self.headers.clear()

    def set_cookie(self, cookie):
        """
        手动设置cookie
        :param cookie: 要设置的cookie
        :return:
        """
        if type(cookie) != dict:
            raise Exception("Wrong type! Dict required!")
        else:
            for key in cookie.keys():
                self.cookie[key] = cookie[key]

    def clear_cookie(self):
        """
        清空cookie
        :return:
        """
        self.cookie.clear()

    def set_body(self, body):
        """
        设置发送的body数据，对应request的kwargs:data
        :param body: 发送的body数据
        :return:
        """
        self.body = body

    def set_js(self, js):
        """
        设置发送的json格式body数据，对应request的kwargs:json
        :param js: 发送的json格式body数据
        :return:
        """
        self.js = js

    def get(self, url, dic=None, headers=None, cookie=None):
        """
        以Get方式发送请求
        :param url: 请求的URL，可以直接拼接好参数
        :param dic: 以字典形式存储的url参数
        :param headers: 以字典形式存储的Header
        :param cookie: 以字典形式存储的cookie
        :return: 返回requests.response对象(状态码)
        """
        self.url = url
        if dic is not None:
            self.__set_url_params(dic)
        if headers is not None:
            self.session.headers = headers
        elif self.headers != {}:
            self.session.headers = self.headers
        if cookie is not None:
            self.set_cookie(cookie)
        self.session.cookies = self.cookie
        self.response = self.session.get(self.url)
        return self.response

    def post(self, url, dic=None, headers=None, cookie=None, data=None, js=None):
        """
        以POST方式发送请求
        :param url: 请求的URL，可以直接拼接好参数
        :param dic: 以字典形式存储的url参数
        :param headers: 以字典形式存储的Header
        :param cookie: 以字典形式存储的cookie
        :param data: body中要发送的数据
        :param js: body中要发送的json
        :return: 返回requests.response对象(状态码)
        """
        self.url = url
        if dic is not None:
            self.__set_url_params(dic)
        if headers is not None:
            self.session.headers = headers
        elif self.headers != {}:
            self.session.headers = self.headers
        if cookie is not None:
            self.set_cookie(cookie)
        self.session.cookies = self.cookie
        self.response = self.session.post(self.url, data=data or self.body, json=js or self.js)
        self.body = ''
        self.js = ''
        return self.response

    def get_response_headers(self):
        """
        :return: 返回响应的Headers
        """
        return self.response.headers

    def get_response_text(self):
        """
        :return: 返回响应的文本结果
        """
        return self.response.text

    def get_res_by_json_path(self, json_path):
        """
        以jsonpath提取响应body中的数据
        :param json_path: jsonpath
        :return: body中的数据
        """
        js = json.loads(self.response.text)
        result = jsonpath.jsonpath(js, json_path)
        return result



