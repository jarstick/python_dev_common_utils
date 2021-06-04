# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import collections
import decimal
import os
import random
import re
import string
import uuid
from collections.abc import Iterable
import unicodedata

from utils.regular_util.regualar import Constant, ContentStat

first_name = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨", "朱", "秦", "尤", "许", "何",
              "吕",
              "施", "张", "孔", "曹", "严", "华", "金", "魏", "陶", "姜", "戚", "谢", "邹", "喻", "柏", "水", "窦", "章", "云", "苏", "潘",
              "葛",
              "奚", "范", "彭", "郎", "鲁", "韦", "昌", "马", "苗", "凤", "花", "方", "俞", "任", "袁", "柳", "酆", "鲍", "史", "唐", "费",
              "廉",
              "岑", "薛", "雷", "贺", "倪", "汤", "滕", "殷", "罗", "毕", "郝", "邬", "安", "常", "乐", "于", "时", "傅", "皮", "卞", "齐",
              "康",
              "伍", "余", "元", "卜", "顾", "孟", "平", "黄", "和", "穆", "萧", "尹", "姚", "邵", "湛", "汪", "祁", "毛", "禹", "狄", "米",
              "贝",
              "明", "臧", "计", "伏", "成", "戴", "谈", "宋", "茅", "庞", "熊", "纪", "舒", "屈", "项", "祝", "董", "粱", "杜", "阮", "蓝",
              "闵",
              "席", "季", "麻", "强", "贾", "路", "娄", "危", "江", "童", "颜", "郭", "梅", "盛", "林", "刁", "钟", "徐", "邱", "骆", "高",
              "夏",
              "蔡", "田", "樊", "胡", "凌", "霍", "虞", "万", "支", "柯", "昝", "管", "卢", "莫", "经", "房", "裘", "缪", "干", "解", "应",
              "宗",
              "丁", "宣", "贲", "邓", "郁", "单", "杭", "洪", "包", "诸", "左", "石", "崔", "吉", "钮", "龚", "程", "嵇", "邢", "滑", "裴",
              "陆",
              "荣", "翁", "荀", "羊", "於", "惠", "甄", "麴", "家", "封", "芮", "羿", "储", "靳", "汲", "邴", "糜", "松", "井", "段", "富",
              "巫",
              "乌", "焦", "巴", "弓", "牧", "隗", "山", "谷", "车", "侯", "宓", "蓬", "全", "郗", "班", "仰", "秋", "仲", "伊", "宫", "宁",
              "仇",
              "栾", "暴", "甘", "钭", "厉", "戎", "祖", "武", "符", "刘", "景", "詹", "束", "龙", "叶", "幸", "司", "韶", "郜", "黎", "蓟",
              "薄",
              "印", "宿", "白", "怀", "蒲", "邰", "从", "鄂", "索", "咸", "籍", "赖", "卓", "蔺", "屠", "蒙", "池", "乔", "阴", "欎", "胥",
              "能",
              "苍", "双", "闻", "莘", "党", "翟", "谭", "贡", "劳", "逄", "姬", "申", "扶", "堵", "冉", "宰", "郦", "雍", "舄", "璩", "桑",
              "桂",
              "濮", "牛", "寿", "通", "边", "扈", "燕", "冀", "郏", "浦", "尚", "农", "温", "别", "庄", "晏", "柴", "瞿", "阎", "充", "慕",
              "连",
              "茹", "习", "宦", "艾", "鱼", "容", "向", "古", "易", "慎", "戈", "廖", "庾", "终", "暨", "居", "衡", "步", "都", "耿", "满",
              "弘",
              "匡", "国", "文", "寇", "广", "禄", "阙", "东", "殴", "殳", "沃", "利", "蔚", "越", "夔", "隆", "师", "巩", "厍", "聂", "晁",
              "勾",
              "敖", "融", "冷", "訾", "辛", "阚", "那", "简", "饶", "空", "曾", "毋", "沙", "乜", "养", "鞠", "须", "丰", "巢", "关", "蒯",
              "相",
              "查", "後", "荆", "红", "游", "竺", "权", "逯", "盖", "益", "桓", "公", "万俟", "司马", "上官", "欧阳", "夏侯", "诸葛"]

last_name = ["澄邈", "德泽", "海超", "海阳", "海荣", "海逸", "海昌", "瀚钰", "瀚文", "涵亮", "涵煦", "明宇", "涵衍", "浩皛", "浩波", "浩博", "浩初", "浩宕",
             "浩歌",
             "浩广", "浩邈", "浩气", "浩思", "浩言", "鸿宝", "鸿波", "鸿博", "鸿才", "鸿畅", "鸿畴", "鸿达", "鸿德", "鸿飞", "鸿风", "鸿福", "鸿光", "鸿晖",
             "鸿朗", "鸿文", "鸿轩", "鸿煊", "鸿骞", "鸿远", "鸿云", "鸿哲", "鸿祯", "鸿志", "鸿卓", "嘉澍", "光济", "澎湃", "彭泽", "鹏池", "鹏海", "浦和",
             "浦泽", "瑞渊", "越泽", "博耘", "德运", "辰宇", "辰皓", "辰钊", "辰铭", "辰锟", "辰阳", "辰韦", "辰良", "辰沛", "晨轩", "晨涛", "晨濡", "晨潍",
             "鸿振", "吉星", "铭晨", "起运", "运凡", "运凯", "运鹏", "运浩", "运诚", "运良", "运鸿", "运锋", "运盛", "运升", "运杰", "运珧", "运骏", "运凯",
             "运乾", "维运", "运晟", "运莱", "运华", "耘豪", "星爵", "星腾", "星睿", "星泽", "星鹏", "星然", "震轩", "震博", "康震", "震博", "振强", "振博",
             "振华", "振锐", "振凯", "振海", "振国", "振平", "昂然", "昂雄", "昂杰", "昂熙", "昌勋", "昌盛", "昌淼", "昌茂", "昌黎", "昌燎", "昌翰", "晨朗",
             "德明", "德昌", "德曜", "范明", "飞昂", "高旻", "晗日", "昊然", "昊天", "昊苍", "昊英", "昊宇", "昊嘉", "昊明", "昊伟", "昊硕", "昊磊", "昊东",
             "鸿晖", "鸿朗", "华晖", "金鹏", "晋鹏", "敬曦", "景明", "景天", "景浩", "俊晖", "君昊", "昆琦", "昆鹏", "昆纬", "昆宇", "昆锐", "昆卉", "昆峰",
             "昆颉", "昆谊", "昆皓", "昆鹏", "昆明", "昆杰", "昆雄", "昆纶", "鹏涛", "鹏煊", "曦晨", "曦之", "新曦", "旭彬", "旭尧", "旭鹏", "旭东", "旭炎",
             "炫明", "宣朗", "学智", "轩昂", "彦昌", "曜坤", "曜栋", "曜文", "曜曦", "曜灿", "曜瑞", "智伟", "智杰", "智刚", "智阳", "昌勋", "昌盛", "昌茂",
             "昌黎", "昌燎", "昌翰", "晨朗", "昂然", "昂雄", "昂杰", "昂熙", "范明", "飞昂", "高朗", "高旻", "德明", "德昌", "德曜", "智伟", "智杰", "智刚",
             "智阳", "瀚彭", "旭炎", "宣朗", "学智", "昊然", "昊天", "昊苍", "昊英", "昊宇", "昊嘉", "昊明", "昊伟", "鸿朗", "华晖", "金鹏", "晋鹏", "敬曦",
             "景明", "景天", "景浩", "景行", "景中", "景逸", "景彰", "昆鹏", "昆明", "昆杰", "昆雄", "昆纶", "鹏涛", "鹏煊", "景平", "俊晖", "君昊", "昆琦",
             "昆鹏", "昆纬", "昆宇", "昆锐", "昆卉", "昆峰", "昆颉", "昆谊", "轩昂", "彦昌", "曜坤", "曜文", "曜曦", "曜灿", "曜瑞", "曦晨", "曦之", "新曦",
             "鑫鹏", "旭彬", "旭尧", "旭鹏", "旭东", "浩轩", "浩瀚", "浩慨", "浩阔", "鸿熙", "鸿羲", "鸿禧", "鸿信", "泽洋", "泽雨", "哲瀚", "胤运", "佑运",
             "允晨", "运恒", "运发", "云天", "耘志", "耘涛", "振荣", "振翱", "中震", "子辰", "晗昱", "瀚玥", "瀚昂", "瀚彭", "景行", "景中", "景逸", "景彰",
             "绍晖", "文景", "曦哲", "永昌", "子昂", "智宇", "智晖", "晗日", "晗昱", "瀚昂", "昊硕", "昊磊", "昊东", "鸿晖", "绍晖", "文昂", "文景", "曦哲",
             "永昌", "子昂", "智宇", "智晖", "浩然", "鸿运", "辰龙", "运珹", "振宇", "高朗", "景平", "鑫鹏", "昌淼", "炫明", "昆皓", "曜栋", "文昂", "治汇",
             "恨桃", "依秋", "依波", "香巧", "紫萱", "涵易", "忆之", "幻巧", "美倩", "安寒", "白亦", "惜玉", "碧春", "怜雪", "听南", "念蕾", "紫夏", "凌旋",
             "芷梦", "凌寒", "梦竹", "千凡", "丹蓉", "慧贞", "思菱", "平卉", "笑柳", "雪卉", "南蓉", "谷梦", "巧兰", "绿蝶", "飞荷", "佳蕊", "芷荷", "怀瑶",
             "慕易", "若芹", "紫安", "曼冬", "寻巧", "雅昕", "尔槐", "以旋", "初夏", "依丝", "怜南", "傲菡", "谷蕊", "笑槐", "飞兰", "笑卉", "迎荷", "佳音",
             "梦君", "妙绿", "觅雪", "寒安", "沛凝", "白容", "乐蓉", "映安", "依云", "映冬", "凡雁", "梦秋", "梦凡", "秋巧", "若云", "元容", "怀蕾", "灵寒",
             "天薇", "翠安", "乐琴", "宛南", "怀蕊", "白风", "访波", "亦凝", "易绿", "夜南", "曼凡", "亦巧", "青易", "冰真", "白萱", "友安", "海之", "小蕊",
             "又琴", "天风", "若松", "盼菡", "秋荷", "香彤", "语梦", "惜蕊", "迎彤", "沛白", "雁彬", "易蓉", "雪晴", "诗珊", "春冬", "晴钰", "冰绿", "半梅",
             "笑容", "沛凝", "映秋", "盼烟", "晓凡", "涵雁", "问凝", "冬萱", "晓山", "雁蓉", "梦蕊", "山菡", "南莲", "飞双", "凝丝", "思萱", "怀梦", "雨梅",
             "冷霜", "向松", "迎丝", "迎梅", "雅彤", "香薇", "以山", "碧萱", "寒云", "向南", "书雁", "怀薇", "思菱", "忆文", "翠巧", "书文", "若山", "向秋",
             "凡白", "绮烟", "从蕾", "天曼", "又亦", "从语", "绮彤", "之玉", "凡梅", "依琴", "沛槐", "又槐", "元绿", "安珊", "夏之", "易槐", "宛亦", "白翠",
             "丹云", "问寒", "易文", "傲易", "青旋", "思真", "雨珍", "幻丝", "代梅", "盼曼", "妙之", "半双", "若翠", "初兰", "惜萍", "初之", "宛丝", "寄南",
             "小萍", "静珊", "千风", "天蓉", "雅青", "寄文", "涵菱", "香波", "青亦", "元菱", "翠彤", "春海", "惜珊", "向薇", "冬灵", "惜芹", "凌青", "谷芹",
             "雁桃", "映雁", "书兰", "盼香", "梅致", "寄风", "芳荷", "绮晴", "映之", "醉波", "幻莲", "晓昕", "傲柔", "寄容", "以珊", "紫雪", "芷容", "书琴",
             "美伊", "涵阳", "怀寒", "易云", "代秋", "惜梦", "宇涵", "谷槐", "怀莲", "英莲", "芷卉", "向彤", "新巧", "语海", "灵珊", "凝丹", "小蕾", "迎夏",
             "慕卉", "飞珍", "冰夏", "亦竹", "飞莲", "秋月", "元蝶", "春蕾", "怀绿", "尔容", "小玉", "幼南", "凡梦", "碧菡", "初晴", "宛秋", "傲旋", "新之",
             "凡儿", "夏真", "静枫", "芝萱", "恨蕊", "乐双", "念薇", "靖雁", "菊颂", "丹蝶", "元瑶", "冰蝶", "念波", "迎翠", "海瑶", "乐萱", "凌兰", "曼岚",
             "若枫", "傲薇", "雅芝", "乐蕊", "秋灵", "凤娇", "觅云", "依伊", "恨山", "从寒", "忆香", "香菱", "静曼", "青寒", "笑天", "涵蕾", "元柏", "代萱",
             "紫真", "千青", "雪珍", "寄琴", "绿蕊", "荷柳", "诗翠", "念瑶", "兰楠", "曼彤", "怀曼", "香巧", "采蓝", "芷天", "尔曼", "巧蕊"]


class StringUtils:
    """
    封装了一些字符串的常用操作
    """

    _special = ".#$%&@"

    @staticmethod
    def is_chinese(string) -> bool:
        """判断是否是中文"""
        for ch in string:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    @staticmethod
    def is_string(string) -> bool:
        """
        判断是不是一个字符串
        :param string: 需要判断的字符串
        :return: 是字符串返回True 否则返回False
        """
        return isinstance(string, str)

    @staticmethod
    def get_uuid() -> str:
        """
        获取uuid值
        return: 返回获取到的uuid字符串
        """
        return str(uuid.uuid1()).replace("-", '')

    @staticmethod
    def get_surname_letter(string) -> str:
        """获取中文名姓氏首字母"""
        str1 = string.encode('gbk')
        try:
            ord(str1)
            return str1
        except:
            asc = str1[0] * 256 + str1[1] - 65536
            if -20319 <= asc <= -20284:
                return 'a'
            if -20283 <= asc <= -19776:
                return 'b'
            if -19775 <= asc <= -19219:
                return 'c'
            if -19218 <= asc <= -18711:
                return 'd'
            if -18710 <= asc <= -18527:
                return 'e'
            if -18526 <= asc <= -18240:
                return 'f'
            if -18239 <= asc <= -17923:
                return 'g'
            if -17922 <= asc <= -17418:
                return 'h'
            if -17417 <= asc <= -16475:
                return 'j'
            if -16474 <= asc <= -16213:
                return 'k'
            if -16212 <= asc <= -15641:
                return 'l'
            if -15640 <= asc <= -15166:
                return 'm'
            if -15165 <= asc <= -14923:
                return 'n'
            if -14922 <= asc <= -14915:
                return 'o'
            if -14914 <= asc <= -14631:
                return 'p'
            if -14630 <= asc <= -14150:
                return 'q'
            if -14149 <= asc <= -14091:
                return 'r'
            if -14090 <= asc <= -13119:
                return 's'
            if -13118 <= asc <= -12839:
                return 't'
            if -12838 <= asc <= -12557:
                return 'w'
            if -12556 <= asc <= -11848:
                return 'x'
            if -11847 <= asc <= -11056:
                return 'y'
            if -11055 <= asc <= -10247:
                return 'z'
            return ''

    @staticmethod
    def get_full_name_letter(string):
        """获取全名首字母,如'张翔',返回zx"""
        if not string:
            return None
        lst = list(string)
        char_lst = []
        for l in lst:
            char_lst.append(StringUtils.get_surname_letter(l))
        return ''.join(char_lst)

    @staticmethod
    def to_lowercase_first(first_str) -> str:
        """
        字符串首字母小写
        :param first_str: 需要首字母小写的字符串
        :return: 返回首字母小写后的字符串
        """
        return str(first_str[0:1]).lower() + first_str[1:]

    @staticmethod
    def is_phone(phone: str) -> bool:
        """
        手机号判断
        :param phone: 需要判断的手机号
        :return:是手机号返回True 否则返回False
        """
        result = re.match(Constant.PHONE_REGEX, phone)
        if result:
            return True
        return False

    @staticmethod
    def is_email(email) -> bool:
        """
        手机号判断
        :param email: 需要判断的邮箱
        :return:是邮箱返回True 否则返回False
        """
        result = re.match(Constant.EMAIL_REGEX, email)
        if result:
            return True
        return False

    @staticmethod
    def is_http_or_https_start(link) -> bool:
        """
        判断一个链接是否是http或https开头
        :param link: 需要判断的链接
        :return:是http或https开头返回True 否则返回False
        """
        result = re.match(Constant.IS_HTTP_OR_HTTPS_REGEX, link)
        if result:
            return True
        return False

    @staticmethod
    def is_url(url) -> bool:
        """
        判断URL是否合法
        :param url: 需要判断的链接
        :return:合法返回True 否则返回False
        """
        result = re.match(Constant.URL_REGEX, url)
        if result:
            return True
        return False

    @staticmethod
    def reverse(string) -> str:
        """
        字符串反转
        :param string: 需要反转的字符串
        :return: 反转以后的字符串
        """
        return string[len(string)::-1]

    @staticmethod
    def suffix(string) -> str:
        """
        获取文件后缀(拓展名)
        :param string: 需要获取的文件字符串
        :return: 返回拓展名 没有拓展名返回None
        """
        index = str(string).rfind(".")
        if index == -1:
            return None
        return str(string)[index + 1::]

    @staticmethod
    def random_number_str(num):
        """
        获取随机的数字字符串
        :param num: 获取的位数
        :return: 获取到的随机字符串
        """
        import random
        n = random.randint(10 ** (num - 1), 10 ** num - 1)

        return n

    @staticmethod
    def statistics_file_content(path, recursion=False, suffix=None):
        """
        统计文件的内容,注释是Python注释
        :param path: 需要统计的文件所在路径
        :param suffix: 拓展名
        :param recursion: 是否递归统计,默认False
        :return:返回统计好的文件字典对象
        """
        contents = []

        def file_content(path, recursion=False, suffix=None):

            files = os.listdir(path)
            for file in files:
                # 文件或文件夹名称
                file_name = file
                # 拼接文件全路径
                file = "%s%s%s" % (path, os.sep, file)
                # 判断文件或目录是否存在
                if os.path.exists(file):
                    # 如果是目录
                    if os.path.isdir(file):
                        # 如果recursion=False
                        if recursion:
                            # 递归操作
                            file_content(file, recursion, suffix)
                        else:
                            continue
                    # 如果是文件
                    if os.path.isfile(file):
                        # 如果拓展名不为空 并且拓展名不等于当前文件拓展名
                        if suffix and not (StringUtils.suffix(file_name) == suffix):
                            continue
                        with open(file, encoding="UTF-8") as f:
                            size = os.path.getsize(f.name)
                            row_count = 0
                            note_count = 0
                            space_count = 0
                            code_count = 0
                            file_name = file_name
                            path = path
                            size = round(size / 1024, 2)
                            try:
                                # 标记是不是多行注释开始1
                                flag = False
                                # 标记是不是多行注释开始2
                                flag2 = False
                                # 标记是否注释结束
                                flag_end = False
                                for line in f:
                                    # 总行数加1
                                    row_count += 1
                                    # 判断是不是多行注释开始
                                    if not flag and re.match(Constant.DOC_NOTE_ONE_REGEX_START, line):
                                        flag = True
                                    # 判断是不是多行注释结束
                                    elif flag and re.match(Constant.DOC_NOTE_ONE_REGEX_END, line):
                                        note_count += 1
                                        flag = False
                                        flag_end = True
                                    # 判断是不是多行注释开始
                                    elif not flag2 and re.match(Constant.DOC_NOTE_TWO_REGEX_START, line):
                                        flag2 = True
                                    # 判断是不是多行注释结束
                                    elif flag2 and re.match(Constant.DOC_NOTE_TWO_REGEX_END, line):
                                        note_count += 1
                                        flag2 = False
                                        flag_end = True

                                    if flag or flag2:
                                        note_count += 1

                                    # 判断是不是单行注释
                                    elif re.match(Constant.LINE_NOTE_REGEX, line):
                                        note_count += 1
                                        # 判断是不是空白行
                                    elif re.match(Constant.BLANK_REGEX, line):
                                        space_count += 1
                                    else:
                                        if not flag_end:
                                            code_count += 1
                                        flag_end = False
                            except:
                                # 如果是非文本文件 则跳出当前循环
                                break
                            content = ContentStat(row_count, note_count, space_count, code_count, file_name, path, size)
                            # print(content)
                            contents.append(content)
            return contents

        return file_content(path, recursion, suffix)

    @staticmethod
    def is_number(num):
        """
        判断一个字符串是不是数字,包含小数
        :param num: 要判断的字符串
        :return: 是数字字符串返回True,否则返回False
        """
        if re.match(r"^\d+(\\.\d+)?$", num):
            return True
        return False

    @staticmethod
    def round_up(num, scale=0):
        """
        四舍五入
        :param scale:精度 默认取整数
        :param num: 要四舍五入的字符串
        :return: 返回四舍五入后的数字
        """
        result = decimal.Decimal(num)
        decimal.getcontext().rounding = decimal.ROUND_UP
        return str(round(result, scale))

    @staticmethod
    def rmb_to_upper(money):
        """
        人民币转中文输出
        :param money: 需要转换的金额
        :return: 转换后的中文表现形式
        """
        # 判断是不是一个合法的数字
        if not StringUtils.is_number(money):
            raise ValueError("不是一个合法的数字")
        money = str(money)
        # 数字0-9中文大写表示形式
        num = ('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖')
        # 单位
        unit = ['', '拾', '佰', '仟']
        # 每四个分隔的单位
        unit_four = ['', '万', '亿', '万亿']
        # 数字分割
        moneys = money.split(".")
        # 取出整数部分
        integer_money = moneys[0]
        # 是否存在小数
        has_float = False
        float_money = None
        if len(moneys) > 1:
            # 取出小数部分
            float_money = moneys[1]
            has_float = True
        # 保存处理结果
        result = []
        # 处理整数部分
        length = len(integer_money)
        if length >= 0:
            # 取余4
            mod = length % 4
            # 取出从左边起4的倍数的最大位数
            max_num = integer_money[mod::]
            result_list = re.findall(r"\\d{4}", max_num)
            # 如果取余不为0 则把剩余位数放到列表最前面
            if mod:
                result_list.insert(0, integer_money[0:mod:])
            # 反转列表
            result_list.reverse()
            # 把获取到的列表索引序列并循环处理
            for r, res in enumerate(result_list):
                # 保存转换为大写的结果
                result_upper = ''
                length = len(res)
                # 取出列表里面的每一项
                for i, n in enumerate(res):
                    if n == '0':
                        # 单位拼接
                        result_upper += num[int(n)]
                    else:
                        # 单位拼接
                        result_upper += num[int(n)] + unit[length - 1 - i]
                        # 把两个以上零替换为一个
                        result_upper = re.sub("零{2,}", '零', result_upper)
                # 把结果插入列表
                while True:
                    if result_upper.endswith("零"):
                        result_upper = result_upper[0:len(result_upper) - 1:]
                    else:
                        break
                result.insert(0, result_upper + unit_four[r])

        # 把列表转换为字符串
        result = ''.join(result)
        # 处理小数部分
        if has_float:
            result += "元"
            #  转换小数部分
            float_money = StringUtils.round_up("0." + float_money, 2)
            if not float_money[2] == '0':
                result += num[int(float_money[2])] + "角"
            if not float_money[3] == '0':
                if float_money[2] == '0':
                    result += "零" + num[int(float_money[3])] + "分"
                else:
                    result += num[int(float_money[3])] + "分"
        else:
            result += "元整"
        if result.endswith("元"):
            result += "整"
        return result

    @staticmethod
    def random_char(number=1):
        """随机选择字母
        :param number: 生成的个数
        """
        ls = random.choices(string.ascii_letters, k=number)
        return ''.join(ls)

    @staticmethod
    def random_lower_char(number=1):
        """随机选择小写字母
        :param number: 生成的个数
        """
        ls = random.choices(string.ascii_lowercase, k=number)
        return ''.join(ls)

    @staticmethod
    def random_upper_char(number=1):
        """随机选择大写字母
        :param number: 生成的个数
        """
        ls = random.choices(string.ascii_uppercase, k=number)
        return ''.join(ls)

    @staticmethod
    def random_digits(number=1):
        """随机选择数字
        :param number: 生成个数
        """
        ls = random.choices(string.digits, k=number)
        return ''.join(ls)

    @staticmethod
    def random_special(number=1):
        """随机选择特殊字符
        :param number: 生成个数
        """
        ls = random.choices(StringUtils._special, k=number)
        return ''.join(ls)

    @staticmethod
    def flag_contain_subset(string: str, lst: list) -> bool:
        """输入一个字符串判断字符串的子集是否在ls列表中"""
        v = (True if subset in string else False for subset in lst)
        return any(v)

    @staticmethod
    def contain_subset(string: str, lst: list) -> (bool, list):
        """输入一个字符串判断字符串的子集是否在ls列表中,并且返回子集列表
        :param string: 字符串
        :param lst: 字符串列表
        :return: 存在返回True。不存在返回False。都会返回list列表
        """
        v = [subset for subset in lst if subset in string]
        return any(v), v

    @staticmethod
    def max_str(lst: list):
        """统计字符串列表出现字符串最多的字符串"""
        c = collections.Counter(lst)
        return max(c.keys(), key=c.get)

    @staticmethod
    def contain_list_subset(string: str, lst: list) -> (bool, list):
        """输入一个字符串判断字符串是否属于某个列表的子集
        例如：string：贵州，lst：[四川，成都市]，那么四川属于lst某个字符串的子集
        :param string: 字符串
        :param lst: 字符串列表
        :return: 存在返回True。不存在返回False。都会返回list列表
        """
        v = [subset for subset in lst if string in subset]
        return any(v), v

    @staticmethod
    def char_number_split(string: str, number: int):
        """根据字符串个数来分割字符串"""
        while string:
            yield string[:number]
            string = string[number:]

    @staticmethod
    def split(regex, string, flag=0, max_split=0) -> list:
        """支持正则分割
        :param string: 字符串
        :param regex: 正则表达式
        :param flag: re.search(re_, self.string, flag), 默认flag=0
        :param max_split: 最大分割数量
        """
        return re.split(pattern=regex, string=string, maxsplit=max_split, flags=flag)

    @staticmethod
    def replace(regex, repl, string, count=0, flags=0):
        """支持正则替换"""
        return re.sub(regex, repl, string, count, flags)

    @staticmethod
    def get_args_count(func) -> int:
        """获取函数对象的参数个数
        def sum(a,b):
            return(a+b)
        print(sum.__code__.co_argcount) # 2
        :param func: 函数对象
        :return: 函数对象的参数个数
        """
        return func.__code__.co_argcount

    @staticmethod
    def find_unicodedata_name(data: str) -> list:
        """查询Unicode编码中的名字
        :param data: 字符串
        :return: 字符的Unicode名字列表
        """
        ls = []
        for i in data:
            ls.append(unicodedata.name(i))
        return ls

    @staticmethod
    def join(chars: str, obj: Iterable) -> str:
        """同str.join函数一样，只不过数字会自动转为字符串
        :param chars: 要拼接的字符串
        :param obj: 拼接对象
        :return: 字符串
        """
        o = (str(i) for i in obj)
        return chars.join(o)

    @staticmethod
    def find(string: str, regex: str) -> list:
        """功能类似于str.find(),但是支持正则表达式
        :param string: 字符串
        :param regex: 正则
        :return: 返回列表，包含元组：（匹配正则对象，匹配正则的开始索引）
        """
        return [(v, v.start()) for v in re.finditer(regex, string)]

    @staticmethod
    def generate_name():
        """随机生成中文姓名"""
        first = random.choices(first_name)
        last = random.choices(last_name)
        name = ''.join([first[0], last[0]])

        return name

