# coding:utf8

from TestCore.InterfaceKeywords import InterfaceKeywords
from TestCore.WebKeywords import WebKeywords


class Keyword:

    def __init__(self, log, var_map):
        self.log = log
        self.var_map = var_map
        self.msg = ''
        self.ik = None
        self.wk = None

    def exec(self, action, params):
        self.msg = ''
        if action.find('http') != -1:
            if not self.ik:
                self.ik = InterfaceKeywords(self.log, self.var_map)
            if hasattr(self.ik, action.strip()):
                fun = getattr(self.ik, action.strip(), None)
                res = fun(params)
                self.msg = self.ik.res
                return res
            else:
                self.log.write('error', 'No such keyword of http:' + action)
                return False
        elif action.find('web') != -1:
            if not self.wk:
                self.wk = WebKeywords(self.log, self.var_map)
            if hasattr(self.wk, action.strip()):
                fun = getattr(self.wk, action.strip(), None)
                res = fun(params)
                self.msg = self.wk.res
                return res
            else:
                self.log.write('error', 'No such keyword of web:' + action)
                return False
        else:
            if hasattr(self, action.strip()):
                fun = getattr(self, action.strip(), None)
                res = fun(params)
                return res
            else:
                self.log.write('error', 'No such keyword:' + action)
                return False

    # 以下公共关键字

    def echo(self, params):
        self.log.write('info', 'Log info:' + self.var_map.get_var(params[0].strip()))
        return True

    @staticmethod
    def is_string(item):
        return isinstance(item, str)

    def _handle_variables_in_expression(self, expression, namespace):
        expr = expression
        beg = 0
        end = 0
        while expr.find('{', beg) != -1:
            beg = expr.find('{', beg) + 1
            end = expr.find('}', end + 1)
            varname = expr[beg: end]
            if self.ik:
                val = self.ik.var_map.get_var(varname)
            elif self.wk:
                val = self.wk.var_map.get_var(varname)
            else:
                val = self.var_map.get_var(varname)
            namespace[varname] = val
        return namespace

    def evaluate(self, params):
        try:
            expression = params[0].strip()
            if len(params) > 1:
                modules = params[1].strip()
            else:
                modules = None
            if len(params) > 2:
                var_name = params[2].strip()
            else:
                var_name = None
            namespace = {}
            if self.is_string(expression) and '${' in expression:
                namespace = self._handle_variables_in_expression(expression, namespace)
                expression = expression.replace('${', '').replace('}', '')
            if modules:
                modules = modules.replace(' ', '').split(',') if modules else []
                namespace.update((m, __import__(m)) for m in modules if m)
            if not self.is_string(expression):
                raise TypeError("Expression must be string")
            if not expression:
                raise ValueError("Expression cannot be empty.")
            val = eval(expression, namespace)
            if var_name:
                self.var_map.set_var(var_name, val)
            self.log.write('info', 'Evaluate of : | %s = %s |---Success!' % (expression, val))
            if type(val) == bool:
                return val
            else:
                return True
        except Exception as e:
            self.log.write('error', 'Evaluate of : | %s |---Fail!' % expression)
            self.log.write('error', e.__str__())
            return False

    @staticmethod
    def _handle_variables_in_param(param, var_map):
        expr = param
        beg = 0
        end = 0
        if '{' in param:
            while expr.find('{', beg) != -1:
                beg = expr.find('{', beg) + 1
                end = expr.find('}', end + 1)
                varname = expr[beg: end]
                val = var_map.get_var(varname)
                expr = expr.replace(varname, val)
            expr = expr.replace('${', '').replace('}', '')
        return expr

