# coding:utf8

import time
from TestCore.Keyword import Keyword
from TestCore.VarMap import VarMap
from TestCore.Excel import Excel


class Runner:

    def __init__(self, tc, log):
        self.tc = tc
        self.log = log
        self.case_res = []  # [[scene, initTime, endTime, result],...]

    def run(self, ds=None, ds_sheet_name=None, rg=None):
        var_map = VarMap()
        scene_range = []
        data = []
        # 选定数据源范围，获取数据源变量值
        if ds or ds_sheet_name or rg:
            # 1-3 类型
            if rg.find('-') != -1:
                li = rg.strip().split('-')
                for i in range(int(li[0]), int(li[1])+1, 1):
                    scene_range.append(i)
            # 2,3,4 or 2 类型
            elif rg.find(',') != -1:
                li = rg.strip().split(',')
                for i in li:
                    scene_range.append(int(i))
            elif len(rg) == 1:
                scene_range.append(int(rg.strip()))
            else:
                self.log.write('error', 'Error data range! Correct format: "2" or "1-3" or "2,3,5"')
                raise Exception('Error data range! Correct format: "2" or "1-3" or "2,3,5"')
            data = Excel.read_sheet(ds, ds_sheet_name)
        else:
            scene_range = [1]
        # 根据数据源范围，遍历执行用例
        for sc in scene_range:
            if data:
                for row in data:
                    var_map.set_var(row[0], row[sc])
            k = Keyword(self.log, var_map)
            beg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            scene_res = [str(sc), 'initTime', 'endTime', 'result']  # [scene, initTime, endTime, result]
            self.log.write('info', '=========Case Start, Scene:' + str(sc) + '=========')
            scene_res[1] = beg_time
            result = True
            for step in self.tc:
                # print(step)
                action = step[2].strip()
                p1 = step[3].strip()
                p1 = var_map.get_var(p1)
                p2 = step[4].strip()
                p2 = var_map.get_var(p2)
                p3 = step[5].strip()
                p3 = var_map.get_var(p3)
                params = [p1, p2, p3]
                self.log.write('info', 'Step: %s, %s, %s, %s' % (action, p1, p2, p3))
                r = k.exec(action, params)
                result = r and result
                if not k.msg:
                    self.log.write('info', 'Message: ' + k.msg)
                if not r:
                    self.log.write('error', 'xxxxxxxxxStep Fail And Stop Running This Case!xxxxxxxxx')
                    break
            end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            scene_res[2] = end_time
            if result:
                scene_res[3] = 'PASS'
            else:
                scene_res[3] = 'FAIL'
            self.log.write('info', '=========Case End, Scene:' + str(sc) + ' ' + scene_res[3] + '=========')
            self.case_res.append(scene_res)
        return self.case_res

    def run2(self, ds=None, ds_sheet_name=None, rg=None):
        var_map = VarMap()
        scene_range = []
        data = []
        # 选定数据源范围，获取数据源变量值
        if ds or ds_sheet_name or rg:
            # 1-3 类型
            if rg.find('-') != -1:
                li = rg.strip().split('-')
                for i in range(int(li[0]), int(li[1])+1, 1):
                    scene_range.append(i)
            # 2,3,4 or 2 类型
            elif rg.find(',') != -1:
                li = rg.strip().split(',')
                for i in li:
                    scene_range.append(int(i))
            elif len(rg) == 1:
                scene_range.append(int(rg.strip()))
            else:
                self.log.write('error', 'Error data range! Correct format: "2" or "1-3" or "2,3,5"')
                raise Exception('Error data range! Correct format: "2" or "1-3" or "2,3,5"')
            data = Excel.read_sheet(ds, ds_sheet_name)
        else:
            scene_range = [1]
        # 根据数据源范围，遍历执行用例
        for sc in scene_range:
            if data:
                for row in data:
                    var_map.set_var(row[0], row[sc])
            k = Keyword(self.log, var_map)
            beg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            scene_res = [str(sc), 'initTime', 'endTime', 'result']  # [scene, initTime, endTime, result]
            self.log.write('info', '=========Case Start, Scene:' + str(sc) + '=========')
            scene_res[1] = beg_time
            result = True
            if_flag = 0
            for_range = []
            for_flag = 0
            for_steps = []
            p1, p2, p3 = '', '', ''
            for i in range(0, len(self.tc), 1):
                p1=p2=p3=''
                # 执行本次步骤
                action = self.tc[i][2].strip()
                if 'if' in action and 'exit' not in action:
                    if_flag = i + 1
                    p1 = self.tc[i][3].strip()
                    try:
                        condition = k.evaluate([p1])
                    except Exception as e:
                        self.log.write('error', 'Invalid If Condition : %s' % p1)
                        self.log.write('error', e.__str__())
                        result = False
                        break
                    if condition:
                        self.log.write('info', 'If condition: TRUE therefor do:')
                        continue
                    else:
                        if_flag = 0
                        self.log.write('info', 'If condition: FALSE therefor pass do')
                        continue
                elif 'for' in action:
                    self.log.write('info', '|---Start of for loop---|')
                    for_flag = 1
                    p1 = self.tc[i][3].strip()
                    for_range = self.for_condition(p1, k.var_map)
                    first = list(for_range.keys())[0]
                    k.var_map.set_var(first, for_range[first][0])
                    k.log.write('info', '---For loop: %d' % for_range[first][0])
                    continue
                elif 'do' in action and (if_flag or for_flag):
                    action = self.tc[i][3].strip()
                    p1 = self.tc[i][4].strip()
                    # p1 = k.var_map.get_var(p1)
                    cell5 = self.tc[i][5].strip()
                    if cell5:
                        temp = cell5.split(',')
                        # p2 = k.var_map.get_var(temp[0])
                        p2 = temp[0]
                        if len(temp) > 1:
                            # p3 = var_map.get_var(temp[1])
                            p3 = temp[1]
                    if for_flag:
                        for_steps.append([action, p1 or '', p2 or '', p3 or ''])
                elif 'exit' in action:
                    p1 = self.tc[i][3].strip()
                    for_steps.append([action, p1 or '', p2 or '', p3 or ''])
                    p1 = k.var_map.get_var(p1)
                    k.log.write('info', 'Exit for loop if: %s' % p1)
                    try:
                        condition = k.evaluate([p1])
                    except Exception as e:
                        self.log.write('error', 'Invalid If Condition : %s' % p1)
                        self.log.write('error', e.__str__())
                        result = False
                        break
                    if condition:
                        for_range = []
                        for_flag = 0
                        for_steps = []
                        k.log.write('info', 'Exit for loop : %s is True' % p1)
                        k.log.write('info', '|---End of for loop---|')
                        continue
                    else:
                        # k.log.write('info', 'Exit for loop : %s is False' % p1)
                        action = 'echo'
                        p1 = 'Exit for loop : %s is False' % p1
                        # if len(self.tc) >= i+1:
                        #     next_step_action = self.tc[i + 1][2].strip()
                        #     if 'do' not in next_step_action and 'exit' not in next_step_action:
                        #         for_run_step_flag = 1
                else:
                    p1 = self.tc[i][3].strip()
                    p1 = k.var_map.get_var(p1)
                    p2 = self.tc[i][4].strip()
                    p2 = k.var_map.get_var(p2)
                    p3 = self.tc[i][5].strip()
                    p3 = k.var_map.get_var(p3)
                params = [p1, p2, p3]
                self.log.write('info', 'Step: %s, %s, %s, %s' % (action, p1, p2, p3))
                r = k.exec(action, params)
                result = r and result
                if k.msg:
                    self.log.write('info', 'Message: ' + k.msg)
                if not r:
                    self.log.write('error', 'xxxxxxxxxStep Fail And Stop Running This Case!xxxxxxxxx')
                    break
                if for_flag or if_flag:
                    # 还有后续步骤
                    if len(self.tc) > i + 1:
                        next_step_action = self.tc[i + 1][2].strip()
                        # 后一步不是do 也不是exit则if/for到此结束，开始执行循环体
                        if 'do' not in next_step_action and 'exit' not in next_step_action:
                            if for_flag:
                                result = self.for_loop(for_range, for_steps, k, result)
                                for_range = []
                                for_flag = 0
                                for_steps = []
                            else:
                                if_flag = 0
                    # 没有后续步骤，则执行循环体
                    else:
                        result = self.for_loop(for_range, for_steps, k, result)
                        for_range = []
                        for_flag = 0
                        for_steps = []
                        if_flag = 0
            end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            scene_res[2] = end_time
            if result:
                scene_res[3] = 'PASS'
            else:
                scene_res[3] = 'FAIL'
            self.log.write('info', '=========Case End, Scene:' + str(sc) + ' ' + scene_res[3] + '=========')
            self.case_res.append(scene_res)
        return self.case_res

    @staticmethod
    def for_condition(condition, var_map):
        if 'in' in condition:
            if 'range' not in condition:
                var_name = condition[condition.find('{')+1:condition.find('}')]
                val = var_map.get_var(var_name)
                temp = condition.split(' ')
                key = temp[0]
                return {key: val}
            elif 'range' in condition:
                temp = condition[condition.find('(')+1:condition.find(')')]
                lst = temp.split(',')
                tmp = condition.split(' ')
                key = tmp[0]
                if len(lst) == 1:
                    return {key: list(range(int(lst[0])))}
                elif len(lst) == 2:
                    return {key: list(range(int(lst[0]), int(lst[1])))}
                elif len(lst) == 3:
                    return {key: list(range(int(lst[0]), int(lst[1]), int(lst[2])))}
                else:
                    return None
            else:
                return None
        else:
            return None


    @staticmethod
    def for_loop(for_range, for_steps, k, result):
        # 从for循环的第二轮开始到结束
        v = list(for_range.keys())
        for_rg = for_range[v[0]]
        condition = True
        for j in range(1, len(for_rg)):
            k.log.write('info', '---For loop: %d' % for_rg[j])
            k.var_map.set_var(v[0], for_rg[j])
            for step in for_steps:
                action = step[0]
                p1 = step[1]
                p1 = k.var_map.get_var(p1)
                p2 = step[2]
                p2 = k.var_map.get_var(p2)
                p3 = step[3]
                p3 = k.var_map.get_var(p3)
                params = [p1, p2, p3]
                k.log.write('info', 'Step: %s, %s, %s, %s' % (action, p1, p2, p3))
                if 'exit' not in action:
                    r = k.exec(action, params)
                    result = r and result
                    if k.msg:
                        k.log.write('info', 'Message: ' + k.msg)
                    if not r:
                        k.log.write('error', 'xxxxxxxxxStep Fail And Stop Running This Case!xxxxxxxxx')
                        k.var_map.remove(v[0])
                        break
                else:
                    try:
                        condition = k.evaluate([p1])
                    except Exception as e:
                        k.log.write('error', 'Invalid If Condition : %s' % p1)
                        k.log.write('error', e.__str__())
                        result = False
                        break
                    if not condition:
                        continue
                    else:
                        # for_range = []
                        # for_flag = 0
                        # for_steps = []
                        # for_run_step_flag = 0
                        k.log.write('info', 'Exit for loop : %s is True' % p1)
                        k.var_map.remove_var(v[0])
                        break
            if condition: break
            k.var_map.remove_var(v[0])
        k.log.write('info', '|---End of for loop---|')
        return result
