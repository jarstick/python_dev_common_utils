# -*- coding: utf-8 -*-

import xlrd
import xlwt
from xlutils.copy import copy


class ExcelUtil:
    """操作EXCEL用例表"""

    def __init__(self, file_name, sheet_index=0):
        self.case_file_name = file_name
        self.sheet_index = sheet_index
        self.table = self.get_table()

    def get_table(self):
        """获取sheets的内容"""
        work_book = xlrd.open_workbook(self.case_file_name)
        table = work_book.sheet_by_index(self.sheet_index)
        return table

    def get_lines(self):
        """获取sheet页的总行数"""
        return self.table.nrows

    def get_cell_value(self, row, col):
        """获取某一个单元格的内容"""
        return self.table.cell_value(row, col)

    def write_value(self, row, col, value):
        """写入数据"""
        read_file = xlrd.open_workbook(self.case_file_name)
        write_file = copy(read_file)
        sheet_data = write_file.get_sheet(0)
        font = xlwt.Font()
        font.name = u'微软雅黑'
        style = xlwt.XFStyle()
        style.font = font
        if value == "pass":
            # 0 黑色
            font.colour_index = 0
            sheet_data.write(row, col, "Pass", style)
        elif value == "fail":
            # 2 红色
            font.colour_index = 2
            sheet_data.write(row, col, "Fail", style)
        else:
            sheet_data.write(row, col, value)
        write_file.save(self.case_file_name)

    def get_rows_data(self, case_id):
        """根据对应的case_id 找到对应行的内容"""
        row_num = self.get_row_num(case_id)
        rows_data = self.get_row_values(row_num)
        return rows_data

    def get_row_num(self, case_id):
        """根据对应的case_id找到对应的行号"""
        num = 0
        clols_data = self.get_cols_data()
        for col_data in clols_data:
            if case_id in col_data:
                return num
            num += 1

    def get_row_values(self, row):
        """根据行号，找到该行的内容"""
        tables = self.table
        row_data = tables.row_values(row)
        return row_data

    def get_cols_data(self, col_id=None):
        """获取某一列的内容"""
        if col_id is not None:
            cols = self.table.col_values(col_id)
        else:
            cols = self.table.col_values(0)
        return cols
