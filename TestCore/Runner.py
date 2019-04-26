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
            for_run_step_flag = 0
            p1, p2, p3 = '', '', ''
            for i in range(0, len(self.tc), 1):
                # 从for循环的第二轮开始到结束
                if for_flag and for_run_step_flag:
                    v = list(for_range.keys())
                    for_rg = for_range[v[0]]
                    for j in range(1, len(for_rg)):
                        k.var_map.set_var(v[0], for_rg[j])
                        for step in for_steps:
                            action = step[0]
                            p1 = step[1]
                            p1 = var_map.get_var(p1)
                            p2 = step[2]
                            p2 = var_map.get_var(p2)
                            p3 = step[3]
                            p3 = var_map.get_var(p3)
                            params = [p1, p2, p3]
                            if 'exit' not in action:
                                self.log.write('info', 'Step: %s, %s, %s, %s' % (action, p1, p2, p3))
                                r = k.exec(action, params)
                                result = r and result
                                if not k.msg:
                                    self.log.write('info', 'Message: ' + k.msg)
                                if not r:
                                    self.log.write('error', 'xxxxxxxxxStep Fail And Stop Running This Case!xxxxxxxxx')
                                    k.var_map.remove(v[0])
                                    break
                            else:
                                try:
                                    condition = k.evaluate(p1)
                                except Exception as e:
                                    self.log.write('error', 'Invalid If Condition : %s' % p1)
                                    self.log.write('error', e.__str__())
                                    result = False
                                    break
                                if condition: continue
                                else:
                                    for_range = []
                                    for_flag = 0
                                    for_steps = []
                                    for_run_step_flag = 0
                                    self.log.write('info', 'End of for loop')
                                    continue
                        k.var_map.remove(v[0])
                # 执行本次步骤
                action = self.tc[i][2].strip()
                if 'if' in action:
                    if_flag = i + 1
                    p1 = self.tc[i][3].strip()
                    try:
                        condition = k.evaluate(p1)
                    except Exception as e:
                        self.log.write('error', 'Invalid If Condition : %s' % p1 )
                        self.log.write('error', e.__str__())
                        result = False
                        break
                    if condition:
                        self.log.write('info', 'If condition: TRUE')
                        continue
                    else:
                        if_flag = 0
                        self.log.write('info', 'If condition: FALSE therefor pass')
                        continue
                elif 'for' in action:
                    self.log.write('info', 'Start of for loop')
                    for_flag = 1
                    p1 = self.tc[i][3].strip()
                    for_range = self.for_condition(p1, k.var_map)
                    continue
                elif 'do' in action and (if_flag or for_flag):
                    action = self.tc[i][3].strip()
                    p1 = self.tc[i][4].strip()
                    # p1 = k._handle_variables_in_param(p1, k.var_map)
                    p1 = var_map.get_var(p1)
                    temp = self.tc[i][5].strip().split(',')
                    # p2 = k._handle_variables_in_param(temp[0], k.var_map)
                    p2 = var_map.get_var(p2)
                    if len(temp) > 0:
                        # p3 = k._handle_variables_in_param(temp[1], k.var_map)
                        p3 = var_map.get_var(p3)
                    if for_flag:
                        for_steps.append([action, p1 or '', p2 or '', p3 or ''])
                        next_step_action = self.tc[i+1][2].strip()
                        if 'do' not in next_step_action and 'exit' not in next_step_action:
                            for_run_step_flag = 1
                elif 'exit' in action:
                    p1 = self.tc[i][3].strip()
                    p1 = var_map.get_var(p1)
                    try:
                        condition = k.evaluate(p1)
                    except Exception as e:
                        self.log.write('error', 'Invalid If Condition : %s' % p1)
                        self.log.write('error', e.__str__())
                        result = False
                        break
                    if condition:
                        for_range = []
                        for_flag = 0
                        for_steps = []
                        for_run_step_flag = 0
                        continue
                    else:
                        for_steps.append([action, p1 or '', p2 or '', p3 or ''])
                        next_step_action = self.tc[i + 1][2].strip()
                        if 'do' not in next_step_action and 'exit' not in next_step_action:
                            for_run_step_flag = 1
                else:
                    p1 = self.tc[i][3].strip()
                    p1 = var_map.get_var(p1)
                    p2 = self.tc[i][4].strip()
                    p2 = var_map.get_var(p2)
                    p3 = self.tc[i][5].strip()
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

    @staticmethod
    def for_condition(conditon, var_map):
        if 'in' in conditon:
            if 'range' not in conditon:
                var_name = conditon[conditon.find('{')+1:conditon.find('}')]
                val = var_map.get_var(var_name)
                temp = conditon.split(' ')
                key = temp[0]
                return {key: val}
            elif 'range' in conditon:
                temp = conditon[conditon.find('range(')+1:conditon.find(')')]
                list = temp.split(',')
                tmp = conditon.split(' ')
                key = tmp[0]
                if len(list) == 1:
                    return {key: range(int(list[0]))}
                elif len(list) == 2:
                    return {key: range(int(list[0]), int(list[1]))}
                elif len(list) == 3:
                    return {key: range(int(list[0]), int(list[1]), int(list[2]))}
                else:
                    return None
            else:
                return None
        else:
            return None




