# coding:utf8

from TestCore.TestSuit import TestSuit


ts = TestSuit('./testcase/Case.xlsx', 'Sheet2')
suit = ts.get_sheet_suits()
for s in suit:
    print(s)