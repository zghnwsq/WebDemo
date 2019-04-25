# coding:utf8

from TestCore.WebEle import WebEle
import time

# locator = 'xpath=//dfdfdf'
# print('find_element_by_' + locator.split('=')[0])
# print(time.mktime(time.localtime()))

# print('dd${fff}'.find('}'))

var_map = {'a': [2,3,4,5], 'b': [2,2]}

def _handle_variables_in_expression(expression, namespace):
    expr = expression
    beg = 0
    end = 0
    while expr.find('{', beg) != -1:
        beg = expr.find('{', beg) + 1
        end = expr.find('}', end+1)
        varname = expr[beg: end]
        # print(varname)
        val = var_map[varname]
        # expr = expr.replace(varname, val)
        namespace[varname] = val
        print(namespace)
        # expr = expr.replace('${', '', 1).replace('}', '', 1)
    return namespace

expr = 'len(${a})>len(${b})'
ns = _handle_variables_in_expression(expr, {})
print(ns)
expression = expr.replace('${', '').replace('}', '')
print(expression)
print(eval(expression, ns))