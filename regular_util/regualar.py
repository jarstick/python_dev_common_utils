# -*- coding: utf-8 -*-

import datetime
import re
import warnings
from datetime import *


province_areas = {
    "11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
    "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南",
    "42": "湖北", "43": "湖南",
    "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏",
    "61": "陕西",
    "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"
}

license_plate_number_regex = r'([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼]{1}[A-Z]{1}(([A-HJ-NP-Z0-9]{5}[DF]{1})|([DF]{1}[' \
                             r'A-HJ-NP-Z0-9]{5})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼]{1}[A-Z]{1}[A-HJ-NP-Z0-9]{4}[' \
                             r'A-HJ-NP-Z0-9挂]{1}) '


def check_phone(phone):
    """正则匹配电话号码"""
    p2 = re.compile(r'^1[3-9]\d{9}$')
    phonematch = p2.match(phone)
    if phonematch:
        return True
    else:
        return False


def check_idCard(idCard):
    """验证身份证号是否合法"""
    errors = ['验证通过!', '身份证号码位数错误!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!']

    idCard = str(idCard)
    idCard = idCard.strip()
    idCard_list = list(idCard)
    # 地区校验
    key = idCard[0: 2]
    if key in province_areas.keys():
        if not province_areas[idCard[0:2]]:
            return errors[4]
    else:
        return errors[4]
    # 15位身份号码检测
    if len(idCard) == 15:
        return errors[1]
    # 18位身份号码检测
    elif len(idCard) == 18:
        # 出生日期的合法性检查
        if int(idCard[6:10]) % 4 == 0 or (int(idCard[6:10]) % 100 == 0 and int(idCard[6:10]) % 4 == 0):
            ereg = re.compile(
                r'[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')  # //闰年出生日期的合法性正则表达式
        else:
            ereg = re.compile(
                r'[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')  # //平年出生日期的合法性正则表达式
        # //测试出生日期的合法性
        if re.match(ereg, idCard):
            # //计算校验位
            S = (int(idCard_list[0]) + int(idCard_list[10])) * 7 + (int(idCard_list[1]) + int(
                idCard_list[11])) * 9 + (int(idCard_list[2]) + int(idCard_list[12])) * 10 + (int(
                idCard_list[3]) + int(idCard_list[13])) * 5 + (int(idCard_list[4]) + int(idCard_list[14])) * 8 + (
                    int(idCard_list[5]) + int(idCard_list[15])) * 4 + (
                    int(idCard_list[6]) + int(idCard_list[16])) * 2 + int(
                idCard_list[7]) * 1 + int(idCard_list[8]) * 6 + int(idCard_list[9]) * 3
            Y = S % 11
            M = "F"
            JYM = "10X98765432"
            M = JYM[Y]  # 判断校验位
            if M == idCard_list[17]:
                return errors[0]
            else:
                return errors[3]
        else:
            return errors[2]
    else:
        return errors[1]


def is_adult(birthday):
    """判断是否成年"""
    current = datetime.datetime.now()
    if current.year - birthday.year < 18:
        return False
    elif current.year - birthday.year == 18:
        if current.month > birthday.month:
            return False
        elif current.month == birthday.month:
            if current.day > birthday.day:
                return False
    return True


def get_province(idCard):
    """根据身份证获取省份"""
    idCard = str(idCard).replace(' ', '')
    key = idCard[0: 2]
    return province_areas[key]


def get_age(idCard, birthday=None):
    """根据身份证获取年龄"""
    idCard = str(idCard).replace(' ', '')
    if not birthday:
        birthday = datetime.datetime.strptime(str(idCard[6:10]) + '-' + str(idCard[10:12]) + '-' + str(idCard[12:14]),
                                              '%Y-%m-%d')
    else:
        birthday = datetime.datetime.strptime(str(birthday), '%Y-%m-%d')
    current = datetime.datetime.now()
    age = current.year - birthday.year
    if current.month < birthday.month:
        age = age - 1
    else:
        if current.month == birthday.month:
            if current.day < birthday.day:
                age = age - 1
    return age


def get_birthday(idCard):
    """根据身份证获取生日"""
    idCard = str(idCard).replace(' ', '')
    birthday = datetime.datetime.strptime(str(idCard[6:10]) + '-' + str(idCard[10:12]) + '-' + str(idCard[12:14]),
                                          '%Y-%m-%d')
    return birthday


class Constant:
    PHONE_REGEX = r"^((13[0-9])|(15[^4])|(18[0-9])|(17[0-8])|(147,145))\\d{8}$"
    # 是否是http或者https开头
    IS_HTTP_OR_HTTPS_REGEX = r"^(http|https)([\\s\\S])*$"
    # 邮箱正则
    EMAIL_REGEX = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](" \
                  r"?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$ "
    # url
    URL_REGEX = r"^(?:(?:(?:https?):)?\\/\\/)(?:\\S+(?::\\S*)?@)?(?:(?!(?:10|127)(?:\\.\\d{1,3}){3})(?!" \
                "(?:169\\.254|192\\.168)(?:\\.\\d{1,3}){2})(?!172\\.(?:1[6-9]|2\\d|3[0-1])(?:\\.\\d{1,3}){2})" \
                "(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\." \
                "(?:[1-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))|(?:(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)" \
                "(?:\\.(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-z\\u00a1-\\uffff]{2," \
                "})).?)(?::\\d{2,5})?(?:[/?#]\\S*)? "
    # 特殊符号正则
    SPECIAL_SYMBOL_REGEX = "[\\pP+~$`^=|<>～｀＄＾＋＝｜＜＞￥×]|\\s+"
    # 出生日期正则 没有考虑闰年
    BIRTH_REGEX = r"(1[8|9]\\d{2}|2\\d{3})(((0[1|3|5|7|8]|1[0,2])(0[1-9]|[1-2][0-9]|3[0-1]))|(02(0[1-9]|[1-2][" \
                  r"0-9]))|((0[4|6|9]|11)(0[1-9]|[1-2][0-9]|30))) "
    # 中国身份证正则
    ID_CHINESE_REGEX = r"(11|12|13|14|15|21|22|23|31|32|33|34|35|36|37|41|42|44|45|46|51|52|53|54|50|61|62|63|64|65" \
                       r"|71|81|82)\\d{4}%s\\d{2}[0-5])(\\d|x|X)" % BIRTH_REGEX
    # 空白行
    BLANK_REGEX = r"^\s*$"
    # 非空白 匹配任何可见字符
    NOT_BLANK_REGEX = r"\\S*"
    # 匹配大写
    UPPERCASE_REGEX = r"^[A-Z]+$"
    # 匹配小写
    LOWERCASE_REGEX = r"^[a-z]+$"
    # 非汉字
    NOT_CHINESE_REGEX = r"[^\u4e00-\u9fa5]"
    # 包含汉字
    CHINESE_REGEX = r"[\u4e00-\u9fa5]"
    # 纯汉字
    PURE_CHINESE_REGEX = r"^[\u4e00-\u9fa5]$"
    # 单行注释
    LINE_NOTE_REGEX = r"(\\s*#.*)|(\\s*\"{3,5}.*\"{3,5}\\s*|\\s*'{6,}\\s*)|(\\s*'{3,5}[^']+'{3,5}\\s*|\\s*'{6,}\\s*)"
    # 多行注释1 开始
    DOC_NOTE_ONE_REGEX_START = r"\\s*'{3,5}[^']*"
    # 多行注释1 结束
    DOC_NOTE_ONE_REGEX_END = r"[^']*'{3,5}\\s*"
    # 多行注释2 开始
    DOC_NOTE_TWO_REGEX_START = r"\\s*\"{3,5}[^\"]*"
    # 多行注释2 结束
    DOC_NOTE_TWO_REGEX_END = r"[^\"]*\"{3,5}\\s*"

    class ConstError(PermissionError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__.keys():
            raise self.ConstError("常量不能被改变!")
        if not key.isupper():
            warnings.warn("常量应该为大写字母")
        self.__dict__[key] = value


class ContentStat:
    """
    文件内容统计
    """

    def __init__(self, row_count, note_count, space_count, code_count, file_name, path, size):
        """
        文件内容统计初始化
        :param row_count: 总行数
        :param note_count: 注释行数
        :param space_count: 空白行数
        :param code_count:代码行数
        :param file_name:文件名称
        :param path: 文件所在路径
        :param size: 文件大小(KB)
        """
        self.row_count = row_count
        self.note_count = note_count
        self.space_count = space_count
        self.code_count = code_count
        self.file_name = file_name
        self.path = path
        self.size = size

    def __str__(self):
        return "{'文件名称':'%s','文件所在路径':'%s','文件大小(KB)':%s,'总行数':%s,'注释行数':%s,'代码行数':%s,'空白行数':%s}" % (
            self.file_name, self.path, self.size, self.row_count, self.note_count, self.code_count, self.space_count)