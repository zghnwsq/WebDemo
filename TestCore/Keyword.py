# coding:utf8

from TestCore.InterfaceKeywords import InterfaceKeywords


class Keyword:

    def __init__(self, log, var_map):
        self.log = log
        self.var_map = var_map
        self.msg = ''
        self.ik = InterfaceKeywords(self.log, self.var_map)

    def exec(self, action, params):
        if action.find('http') != -1:
            if hasattr(self.ik, action.strip()):
                fun = getattr(self.ik, action.strip(), None)
                res = fun(params)
                self.msg = self.ik.res
                return res
            else:
                self.log.write('error', 'No such keyword:' + action)
                return False
        elif action.find('web') != -1:
            pass
        else:
            self.log.write('error', 'No such keyword:' + action)
            return False





