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
            k = key.replace('${', '').replace('}', '')
            if k in self.vars:
                return self.vars[k]
            else:
                return 'No such Var!'
        else:
            return key.strip()

    def clear(self):
        """
        清空变量字典
        :return:
        """
        self.vars.clear()
