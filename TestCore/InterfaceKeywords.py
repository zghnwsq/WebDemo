# coding:utf8

from . import Http
import json
import lxml.etree as etree


class InterfaceKeywords:

    def __init__(self, log, var_map):
        """
        初始化类成员，res：响应的文本
        :param log:  传入log实例
        :param var_map: 传入var_map实例，变量集
        """
        self.log = log
        self.res = ''
        self.http = None
        self.var_map = var_map

    def http_set(self):
        """
        实例化Http
        :return: True
        """
        self.http = Http()
        self.log.write('info', 'New Http Object Set')
        return True

    def http_get(self, params):
        """
        Get方法，除url，其他参数通过set方法设定
        :param params: params[0]: url
        :return: 布尔值结果
        """
        self.res = ''
        try:
            url = self.var_map.get_var(params[0])
            self.http.get(url)
            self.res = self.http.get_response_text()
            self.log.write('info', 'Sent GET request:|' + url + '|---Success!')
            self.log.write('info', 'Response:--->|' + self.res + '|<---')
            return True
        except Exception as e:
            self.res = ''
            self.log.write('error', 'Try to Get: ' + url + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_post(self, params):
        """
        POST方法, 除url，其他参数通过set方法设定
        :param params: params[0]:url
        :return: 布尔值结果
        """
        self.res = ''
        try:
            url = self.var_map.get_var(params[0])
            self.http.post(url)
            self.res = self.http.get_response_text()
            self.log.write('info', 'Sent POST request:|' + url + '|---Success!')
            self.log.write('info', 'Response:--->|' + self.res + '|<---')
            return True
        except Exception as e:
            self.res = ''
            self.log.write('error', 'Try to POST: ' + url + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_add_headers(self, params):
        """
        添加请求头
        :param params: params[0]: dict/header_key params[1]: header_value
        :return: 布尔值结果
        """
        try:
            if params[1].strip() != '':
                value = self.var_map.get_var(params[1].strip())
                self.http.add_headers({params[0].strip(): value})
            else:
                hds = json.loads(params[0])
                self.http.add_headers(hds)
            self.log.write('info', 'Try to add headers: ' + params[0] + params[1] + '|---Success')
            return True
        except Exception as e:
            self.log.write('error', 'Try to add headers: ' + params[0] + params[1] + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_remove_header(self, params):
        """
        删除部分headers
        :param params: params[0]: 逗号分隔的header_key
        :return: 布尔值结果
        """
        try:
            if params[0].strip() != '':
                self.http.remove_headers(params[0])
            self.log.write('info', 'Try to remove headers: ' + params[0] + '|---Success!')
            return True
        except Exception as e:
            self.log.write('error', 'Try to remove headers: ' + params[0] + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_set_body(self, params):
        """
        设置POST请求Body
        :param params: params[0]: body
        :return: 布尔值结果
        """
        try:
            if params[0].strip() != '':
                self.http.set_body(params[0])
            self.log.write('info', 'Try to set body: ' + params[0] + '|---Success!')
            return True
        except Exception as e:
            self.log.write('error', 'Try to set body: ' + params[0] + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_set_json(self, params):
        """
        设置POST请求json格式body
        :param params: params[0]: json
        :return: 布尔值结果
        """
        try:
            if params[0].strip() != '':
                self.http.set_body(params[0])
            self.log.write('info', 'Try to set body: ' + params[0] + '|---Success!')
            return True
        except Exception as e:
            self.log.write('error', 'Try to set body: ' + params[0] + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_get_res_by_json_path(self, params):
        """
        以jsonpath获取响应中的值
        :param params: params[0]:json path params[1]:用来存储值的变量名
        :return: 布尔值结果
        """
        try:
            value = self.http.get_res_by_json_path(params[0])
            self.var_map[params[1]] = value
            self.log.write('info', 'Try to get value: ' + params[0] + ':' + value + '|---Success!')
            return True
        except Exception as e:
            self.log.write('error', 'Try to get value: ' + params[0] + ':' + value + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_get_res_by_xpath(self, params):
        """
        以Xpath获取响应中的值
        :param params: params[0]:Xpath params[1]:用来存储值的变量名
        :return: 布尔值结果
        """
        try:
            tree = etree.HTML(self.http.get_response_text())
            value = tree.xpath(params[0])
            self.var_map[params[1]] = value
            self.log.write('info', 'Try to get value: ' + params[0] + ':' + value + '|---Success!')
            return True
        except Exception as e:
            self.log.write('error', 'Try to get value: ' + params[0] + ':' + value + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_assert_res_by_json_path(self, params):
        """
        断言response json中的值是否符合预期
        :param params: params[0]:json path params[1]:期望值
        :return: 布尔值结果
        """
        try:
            value = self.http.get_res_by_json_path(params[0])
            if value.find(params[1].strip()) != -1:
                self.log.write('info', 'Assert json : ' + params[0] + ':' + value + '|---Success!')
                return True
            else:
                self.log.write('error', 'Assert json : ' + params[0] + ':' + value + 'expect:' + params[1]+'|---Fail!')
                return False
        except Exception as e:
            self.log.write('error', 'Assert json : ' + params[0] + ':' + value + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_assert_res_contain(self, params):
        """
        断言response中的值是否包含预期值
        :param params: params[0]:期望值
        :return: 布尔值结果
        """
        try:
            res = self.http.get_response_text()
            if res.find(params[0].strip()) != -1:
                self.log.write('info', 'Assert res contain : ' + params[0] + '|---Success!')
                return True
            else:
                self.log.write('error', 'Assert res contain : ' + params[0] + 'expect:' + params[1]+'|---Fail!')
                return False
        except Exception as e:
            self.log.write('error', 'Assert res contain : ' + params[0]  + '|---Fail!')
            self.log.write('error', e.__str__())
            return False





