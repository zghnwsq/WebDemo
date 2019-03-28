# coding:utf8

from TestCore.Excel import Excel


class TestCase:

    def __init__(self, excel, sheet_name):
        self.excel = excel
        self.sheet_name = sheet_name

    def get_test_case(self):
        case = Excel.read_sheet(self.excel, self.sheet_name)
        case.pop(0)
        return case

