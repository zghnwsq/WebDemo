# coding:utf8

from TestCore.Runner import Runner
from TestCore.Log import Log
from TestCore.TestCase import TestCase
from TestCore.Main import MainThread

# log = Log('./log/test.txt', 'info')
# # tc = TestCase('./testcase/Case.xlsx', 'Sheet2').get_test_case()
# # # print(tc)
# # r = Runner(tc, log)
# # res = r.run(ds='./testcase/Case.xlsx', ds_sheet_name='data', rg='1-2')

thd = MainThread('./log/test1.txt',
                 './testcase/Case3.xlsx',
                 'sheet1',
                 ds_path='./testcase/Case3.xlsx',
                 ds_sheet='data',
                 rg='1')
thd.start()
thd.join()
res = thd.get_res()

for r in res:
    print(r)


