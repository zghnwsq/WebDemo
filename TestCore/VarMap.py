# coding:utf8


class VarMap:

    def __init__(self):
        self.vars = dict()

    def set_var(self, key, value):
        """
        设置变量
        :param key: 变量键
        :param value: 变量值
        :return:
        """
        if key=='':
            raise Exception('Empty var name!')
        else:
            k = key.replace('${', '').replace('}', '')
            self.vars[k] = value

    def remove_var(self, key):
        """
        移除变量
        :param key: 变量键
        :return:
        """
        k = key.replace('${', '').replace('}', '')
        if k in self.vars:
            return self.vars.pop(key)
        else:
            return 'No such Var!'

    def get_var(self, key):
        """
        返回变量值，如不是变量格式${}则返回首尾去空格的原值, 如无此变量则返回提示
        :param key: 变量键
        :return:
        """
        if key.find('${') != -1:
            # k = key.replace('${', '').replace('}', '')
            # if k in self.vars:
            #     return self.vars[k]
            # else:
            #     return 'No such Var!'
            return self._handle_variables_in_param(key, self.vars)
        else:
            return key.strip()

    @staticmethod
    def _handle_variables_in_param(param, v):
        p = param
        beg = 0
        end = 0
        if '{' in param:
            while p.find('{', beg) != -1:
                beg = p.find('{', beg) + 1
                end = p.find('}', end + 1)
                k = p[beg: end].strip()
                if k in v:
                    val = v[k]
                else:
                    return 'No such Var!'
                p = p.replace(k, str(val))
            p = p.replace('${', '').replace('}', '')
        return p

    def clear(self):
        """
        清空变量字典
        :return:
        """
        self.vars.clear()
