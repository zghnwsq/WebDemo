# coding:utf8

from . import Http, Log, VarMap
import json

class InterfaceKeywords:

    def __init__(self, log, var_map):
        self.log = log
        self.res = ''
        self.http = None
        self.var_map = var_map

    def http_set(self):
        self.http = Http()
        self.log.write('info', 'New Http Object Set')
        return True

    def http_get(self, params):
        self.res = ''
        try:
            url = self.var_map.get_var(params[0])
            self.http.get(url)
            self.res = self.http.get_response_text()
            self.log.write('info', 'Sent GET request:|'+ url + '|---Success!')
            self.log.write('info', 'Response:--->|' + self.res + '|<---')
            return True
        except Exception as e:
            self.res = ''
            self.log.write('error', 'Try to Get: ' + url + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def http_post(self, params):
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
        try:
            if params[1] != '':
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
        try:
            if params[0] != '':
                self.http.remove_headers(params[0])
            self.log.write('info', 'Try to remove headers: ' + params[0] + '|---Success!')
            return True
        except Exception as e:
            self.log.write('error', 'Try to remove headers: ' + params[0]+ '|---Fail!')
            self.log.write('error', e.__str__())
            return False

