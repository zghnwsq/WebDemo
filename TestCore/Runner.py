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










