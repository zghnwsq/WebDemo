# coding:utf8

import xlwt, xlrd
from xlutils.copy import copy


class Excel:

    @staticmethod
    def read_sheet(path, sheet_name):
        """
        按sheet_name读取excel
        :param path: excel路径
        :param sheet_name: sheet_name
        :return: 返回数组
        """
        try:
            row = []
            sheet = xlrd.open_workbook(path).sheet_by_name(sheet_name)
            for i in range(sheet.nrows):
                r = sheet.row_values(i)
                rr = []
                for j in range(sheet.ncols):
                    rr.append(r[j])
                row.append(rr)
            return row
        except Exception as e:
            print(e)
            return None


    @staticmethod
    def read_sheets(path):
        """
        读取整个excel
        2019.3.22: 为配合excel写入的方法，改为以sheet_index为key存储
        :param path: excel路径
        :return: 返回一个以sheet_index(x sheet_name x)为key的字典
        """
        try:
            excel = xlrd.open_workbook(path)
            # sheets = excel.sheets()
            sheet = {}
            # for sht in sheets:
            for no in range(excel.nsheets):
                sht = excel.sheet_by_index(no)
                row = []
                for i in range(sht.nrows):
                    r = sht.row_values(i)
                    rr = []
                    for j in range(sht.ncols):
                        rr.append(r[j])
                    row.append(rr)
                # sheet[sht.name] = row
                sheet[no] = row
            return sheet
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def write_excel(path, suffix, sheet_index, msg):
        """
        修改excel
        :param path: 源文件路径
        :param suffix: 加在源文件名后的后缀
        :param sheet_index: 要写入sheet的序号
        :param msg: 要写入文档的信息[行， 列， 信息]
        :return:
        """
        try:
            excel = xlrd.open_workbook(path)
            writable_excel = copy(excel)
            sheet = writable_excel.get_sheet(sheet_index)
            sheet.write(msg[0], msg[1], msg[2])
            if path.find('.xlsx') != -1:
                writable_excel.save(path.replace('.xlsx', suffix+'.xls'))
            elif path.find('.xls') != -1:
                writable_excel.save(path.replace('.xls', suffix + '.xls'))
            else:
                raise Exception(u'错误文件类型或扩展名!!')
        except Exception as e:
            print(e)





