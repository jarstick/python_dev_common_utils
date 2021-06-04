# -*- coding: utf-8 -*-

import xlrd

from utils.log import log


class ReadExcel:
    """	读取Excel"""

    def __init__(self, path, sheet_name='Sheet1'):

        self._case_path = path
        self.data = xlrd.open_workbook(self._case_path)
        self.table = self.data.sheet_by_name(sheet_name)

        self.row = self.table.row_values(0)
        # 获取第一行作为key值
        self.keys = self.table.row_values(0)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols
        # 当前行
        self.curRowNo = 1
        self.cases_data = self.read_cases_data()

    # 解析excel，返回一个包含所有case的嵌套list,eg:[{case1_data},{case2_data}]
    def read_cases_data(self):
        global total_cases_data
        if self.rowNum <= 1:
            log.info("总行数小于1")
        else:
            total_cases_data = []
            j = 1
            for i in range(self.rowNum - 1):
                single_case_data = {}
                # 从第二行取对应values值
                values = self.table.row_values(j)
                for x in range(self.colNum):
                    single_case_data[self.keys[x]] = values[x]
                total_cases_data.append(single_case_data)
                j += 1
        return total_cases_data

    def next(self):
        r = []
        while self.has_next():
            temp_dict = {}
            col = self.table.row_values(self.curRowNo)
            i = self.colNum
            for x in range(i):
                temp_dict[self.row[x]] = col[x]
            r.append(temp_dict)
            self.curRowNo += 1
        log.info(r)
        return r

    def has_next(self):
        if self.rowNum <= self.curRowNo:
            return False
        else:
            return True

    def return_test_data(self, key):
        for i in self.cases_data:
            if isinstance(i, dict):
                if key in i.values():
                    return i
            else:
                log.error("%s 不是字典" % i)
