# coding:utf8
from TestCore.Excel import Excel


class TestSuit:

    def __init__(self, excel, sheet_name=None):
        """
        初始化
        excel_sheets: 整个excel的读取结果 dict key:sheet_index
        excel_suits: 整个excel的用例信息集 dict key:sheet_index
        excel_sheet: 指定sheet的读取结果 list
        sheet_suits: 指定sheet的用例信息集 list
        :param excel: excel路径
        :param sheet_name: 指定某个sheet
        """
        self.excel = excel
        if not sheet_name:
            self.sheet_name = None
            self.excel_sheets = {}
            self.excel_suits = {}
        else:
            self.sheet_name = sheet_name
            self.excel_sheet = []
            self.sheet_suits = []

    def get_sheet_suits(self):
        if self.sheet_name:
            self.excel_sheet = Excel.read_sheet(self.excel, self.sheet_name)
            self.sheet_suits = self.__get_suit_from_sheet(self.excel_sheet)
        return self.sheet_suits

    def get_excel_suits(self):
        if not self.sheet_name:
            self.excel_sheets = Excel.read_sheets(self.excel)
            for i in self.excel_sheets.keys():
                sheet = self.excel_sheets[i]
                suit = self.__get_suit_from_sheet(sheet)
                self.excel_suits[i] = suit
        return self.excel_suits


    @staticmethod
    def __get_suit_from_sheet(sheet):
        """
        从单个sheet中提取suit信息
        :param sheet:
        :return:
        """
        suit = []
        current_suit = ''
        current_case = ''
        init_row_num = 0
        end_row_num = 0
        for i in range(1, len(sheet)):
            row = sheet[i]
            if i == 1:
                if row[0] == '':
                    raise Exception(u'用例首行测试集名称不能为空!')
                elif row[1] == '':
                    raise Exception(u'用例首行测试用例名称不能为空!')
            # suit有 case有
            if row[0] and row[1]:
                #如果是步骤第一行
                if i == 1:
                    current_suit = row[0]
                    current_case = row[1]
                    init_row_num = i
                    end_row_num = i
                # 不是第一行
                elif i != 1 and i != len(sheet)-1:
                    suit.append([current_suit,
                                 current_case,
                                 init_row_num,
                                 end_row_num,
                                 'initTime',
                                 'endTime',
                                 'result'])
                    current_suit = row[0]
                    current_case = row[1]
                    init_row_num = i
                    end_row_num = i
                    # 是最后一行
                    if i == len(sheet)-1:
                        suit.append([current_suit,
                                     current_case,
                                     init_row_num,
                                     end_row_num,
                                     'initTime',
                                     'endTime',
                                     'result'])
            # suit没有 case有
            elif not row[0] and row[1]:
                suit.append([current_suit,
                             current_case,
                             init_row_num,
                             end_row_num,
                             'initTime',
                             'endTime',
                             'result'])
                # 不是最后一行
                if i != len(sheet)-1:
                    current_case = row[1]
                    init_row_num = i
                    end_row_num = i
                # 是最后一行
                elif i == len(sheet)-1:
                    current_case = row[1]
                    init_row_num = i
                    end_row_num = i
                    suit.append([current_suit,
                                 current_case,
                                 init_row_num,
                                 end_row_num,
                                 'initTime',
                                 'endTime',
                                 'result'])
            # suit没有 case没有
            elif not row[0] and not row[1]:
                # 不是最后一行
                if i != len(sheet) - 1:
                    end_row_num = i
                # 是最后一行
                elif i == len(sheet) - 1:
                    end_row_num = i
                    suit.append([current_suit,
                                 current_case,
                                 init_row_num,
                                 end_row_num,
                                 'initTime',
                                 'endTime',
                                 'result'])
            else:
                raise Exception(u'错误的用例格式, 请检查!')
        return suit



