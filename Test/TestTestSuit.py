# coding:utf8

from TestCore.TestSuit import TestSuit


ts1 = TestSuit('./testcase/Case.xlsx', 'Sheet2')
suit1 = ts1.get_sheet_suits()
for s in suit1:
    print(s)

ts2 = TestSuit('./testcase/Case.xlsx')
suit2 = ts2.get_excel_suits()
for key in suit2.keys():
    print(key)
    for s in suit2[key]:
        print(s)

