# -*- coding:utf-8 -*-

import copy
from itertools import combinations, combinations_with_replacement, permutations


class ListUtils:
    """
    封装了一些list常用操作
    """

    @staticmethod
    def replaceAll(origin_list, old_element, new_element, deep=True) -> list:
        """
        替换list里面指定的全部的元素
        :param origin_list:需要替换的list
        :param old_element:需要被替换的元素
        :param new_element:替换的元素
        :param deep:是否深度替换 默认True
        :return:替换以后的list 原来的list不会改变
        """
        # 如果不是一个list 抛出异常
        if not isinstance(origin_list, list):
            raise ValueError("%s不是一个list" % origin_list)
        # 深拷贝
        target_list = copy.deepcopy(origin_list)

        def replace(target_list, old_element, new_element, deep):

            # 遍历列表
            for index, value in enumerate(target_list):
                # 如果是子列表且是深度替换 则递归
                if isinstance(value, list) and deep:
                    replace(value, old_element, new_element, deep)
                else:
                    # 如果去除的值为需要替换的值 则替换
                    if value == old_element:
                        target_list[index] = new_element
            return target_list

        return replace(target_list, old_element, new_element, deep)

    @staticmethod
    def remove_subset(lst: list):
        """去除列表中的子集
        比如：['aa','a','ab'] --> ['aa','ab']
        :param lst: 字符串列表
        :return: 返回去重后的结果
        """
        lst = sorted(lst, key=lambda x: len(x), reverse=True)
        total = []
        for subset in lst:
            if subset not in total:
                flag = True
                for word in total:
                    if subset in word:
                        flag = False
                        break
                if flag:
                    total.append(subset)
        return total

    @staticmethod
    def combination(lst: iter, number=2) -> list:
        """组合：不重复"""
        c = combinations(lst, number)
        return list(c)

    @staticmethod
    def combination_repeat(lst: iter, number=2) -> list:
        """组合：可重复"""
        c = combinations_with_replacement(lst, number)
        return list(c)

    @staticmethod
    def permutation(lst: iter, number=2) -> list:
        """排列"""
        c = permutations(lst, number)
        return list(c)

    @staticmethod
    def list2dict(column: list, result: list) -> dict:
        """列表转字典"""
        if not column or not result:
            raise RuntimeWarning("传入的参数不能为空")
        res_dict = dict()
        for index, col in enumerate(column):
            if " : " in col:
                arr = col.split(" : ")
                pre_col_name = arr[0].strip()
                col_type = arr[1].strip()
            else:
                pre_col_name = col
                col_type = None
            if " as " in pre_col_name:
                col_name = pre_col_name.split(" as ")[1].strip()
            else:
                col_name = pre_col_name
            if col_type:
                if "int" == col_type:
                    res_dict[col_name] = int(result[index]) if result[index] else 0
                elif "str" == col_type:
                    res_dict[col_name] = str(result[index]) if result[index] else ''
                elif "float" == col_type:
                    res_dict[col_name] = float(result[index]) if result[index] else 0.0
                else:
                    res_dict[col_name] = result[index]
            else:
                res_dict[col_name] = result[index]
        return res_dict

    @staticmethod
    def de_duplicate(dict_list) -> list:
        """[{}]结构列表去重"""
        return [dict(t) for t in set([tuple(d.items()) for d in dict_list])]

    @staticmethod
    def de_duplicate_orderly(dict_list) -> list:
        """[{}]去重+排序"""
        _set = set()
        new_list = []
        for d in dict_list:
            t = tuple(d.items())
            if t not in _set:
                _set.add(t)
                new_list.append(d)
        return new_list

