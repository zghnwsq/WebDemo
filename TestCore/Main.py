# coding:utf8

import threading, time
from TestCore.Runner import Runner
from TestCore.Log import Log
from TestCore.TestCase import TestCase


class MainThread(threading.Thread):

    def __init__(self, log_path, case_path, case_sheet, ds_path=None, ds_sheet=None, rg=None):
        threading.Thread.__init__(self)
        self.log = Log(log_path, 'info')
        self.tc = TestCase(case_path, case_sheet).get_test_case()
        self.runner = Runner(self.tc, self.log)
        self.ds_path = ds_path
        self.ds_sheet = ds_sheet
        self.rg = rg
        self.res = None

    def run(self):
        if self.ds_path or self.ds_sheet or self.rg:
            self.res = self.runner.run2(ds=self.ds_path, ds_sheet_name=self.ds_sheet, rg=self.rg)
        else:
            self.res = self.runner.run()

    def get_res(self):
        try:
            return self.res
        except Exception as e:
            print(e.__str__())
            return None




