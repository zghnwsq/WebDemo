# encoding:utf8

from TestCore.Excel import Excel

# sht = Excel.read_sheet('./testcase/Case.xlsx', 'Sheet2')
# if sht is not None:
#     for i in sht:
#         print(i)

sht = Excel.read_sheets('./testcase/Case.xlsx')
if sht is not None:
    # print(sht)
    for i in sht.keys():
        # print(sht[i])
        for j in sht[i]:
            print(j)

# msg = [2, 6, 'pass']
# Excel.write_excel('./testcase/Case.xlsx', '_result', 0, msg)

