# -*- coding:utf-8 -*-

import datetime, random, time
import sys

from utils.log import Log,log


class DataUtil:

    today = datetime.datetime.now().strftime('%Y%m%d')  # 获取当前日期

    def str_to_time(self, time_to_str='1970-01-01 00:00:00'):  # 字符串转换为时间戳
        try:
            d = datetime.datetime.strptime(time_to_str, "%Y-%m-%d %H:%M:%S")
            t = d.timetuple()
            timeStamp = int(time.mktime(t))
            return timeStamp
        except:
            d = datetime.datetime.strptime(time_to_str, "%Y-%m-%d")
            t = d.timetuple()
            timeStamp = int(time.mktime(t))
            return timeStamp

# 将时间转换成13位
    def yunlizhi(self, data):
        now = str(data)
        return self.str_to_time(now) * 1000

    # 字符串转换为时间戳,支持调整
    def string_toTimestamp_adjust(self, type: int = 2, num: int = 0, isTimestamp_second: bool = False):
        time_to_str = self.adjust_time(type=type, num=num)
        timestamp = self.string_toTimestamp(time_to_str, isTimestamp_second=isTimestamp_second)
        return timestamp

    # 时间调整
    def adjust_time(self, type: int = 2, num: int = 0):
        '''days seconds microseconds milliseconds minutes hours weeks fold'''
        '''type: 周 天 时 分 秒
        isDate: 是否是日期， 默认否'''
        strTime = datetime.datetime.now()  # 默认取当前时间
        if type == 1:
            day = strTime + datetime.timedelta(weeks=num)
        elif type == 2:
            day = strTime + datetime.timedelta(days=num)
        elif type == 3:
            day = strTime + datetime.timedelta(hours=num)
        elif type == 4:
            day = strTime + datetime.timedelta(minutes=num)
        elif type == 5:
            day = strTime + datetime.timedelta(seconds=num)
        else:
            log.info("暂不支持的调整单位")
            sys.exit()
        # 将当前时间转换后时间戳，然后在将时间戳转换为时间字符串
        day = self.timestamp_toString(
            self.datetime_toTimestamp(day)
        )
        return day

    # 把字符串转成时间戳形式
    def string_toTimestamp(self, strTime='1970-01-01 00:00:00', isTimestamp_second: bool = False):
        '''isTimestamp_second:是否输出时间为秒，默认为false即13位时间戳，true：返回10位时间戳'''
        try:
            if strTime == '1970-01-01 00:00:00':
                strTime = self.timestamp_toString(timeStamp=0)
            timeStamp = int(time.mktime(self.string_toDatetime(strTime).timetuple()))
            if not isTimestamp_second:
                timeStamp *= 1000
            return timeStamp
        except Exception as error:
            log.exception("数据处理失败，原因为:\n%s" % (error))

    # 把时间戳转成字符串形式
    def timestamp_toString(self, timeStamp):
        try:
            timeStamp = int(timeStamp)
            if len(str(timeStamp)) >= 13:
                timeStamp /= 1000
            if not timeStamp and timeStamp != 0:
                timeStamp = time.time()
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp))
        except Exception as error:
            log.exception("数据处理失败，原因为:\n%s" % (error))

    # 把datetime类型转外时间戳形式
    def datetime_toTimestamp(self, dateTime):
        return int(time.mktime(dateTime.timetuple()))

    # 把字符串转成datetime
    def string_toDatetime(self, string):
        return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


    # 随机日期格式生成数据
    def create_number(self):
        num = random.randint(1000, 9999)
        now_time = datetime.datetime.now().strftime('%Y%m%d')
        show = now_time + str(num)
        return show

    # 随机生成号码
    def create_phone(self):
        lists = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                 "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
                 "186", "187", "188", "189", "199"]
        return random.choice(lists) + "".join(random.choice("0123456789") for i in range(8))

    def regiun(self):
        '''生成身份证前六位'''
        # 列表里面的都是一些地区的前六位号码
        first_list = ['362402', '362421', '362422', '362423', '362424', '362425', '362426', '362427', '362428',
                      '362429',
                      '362430', '362432', '110100', '110101', '110102', '110103',
                      '513825', '110104', '110105', '110106', '110107', '110108', '110109', '110111', '5101052',
                      '520142']
        first = random.choice(first_list)
        return first

    def year(self):
        '''生成年份'''
        now = time.strftime('%Y')
        # now-60大于60岁的不在内,now-18直接过滤掉小于18岁出生的年份
        second = random.randint(int(now) - 60, int(now) - 18)
        # age = int(now) - second
        # log.exception('随机生成的身份证人员年龄为：'+str(age))
        return second

    def month(self):
        '''生成月份'''
        three = random.randint(1, 12)
        # 月份小于10以下，前面加上0填充
        if three < 10:
            three = '0' + str(three)
            return three
        else:
            return three

    def day(self):
        '''生成日期'''
        four = random.randint(1, 31)
        # 日期小于10以下，前面加上0填充
        if four < 10:
            four = '0' + str(four)
            return four
        else:
            return four

    def randoms(self):
        '''生成身份证后四位'''
        # 后面序号低于相应位数，前面加上0填充
        five = random.randint(1, 9999)
        if five < 10:
            five = '000' + str(five)
            return five
        elif 10 < five < 100:
            five = '00' + str(five)
            return five
        elif 100 < five < 1000:
            five = '0' + str(five)
            return five
        else:
            return five

    # 随机生成身份证
    def randomID(self):
        first = self.regiun()
        second = self.year()
        three = self.month()
        four = self.day()
        last = self.randoms()
        IDcard = str(first) + str(second) + str(three) + str(four) + str(last)
        return IDcard

    # 随机生成银行卡号
    def cardNum_generator(self):
        cardNum = '6214'  # 可以更改，银行卡号前四位
        for i in range(11):
            cardNum = cardNum + str(random.randint(0, 9))
        summation = 0
        for i in range(16):
            if i == 0:
                continue
            tmp1 = int(cardNum[15 - i: 16 - i])
            if ((i + 1) % 2 == 0):
                if tmp1 < 5:
                    summation = summation + tmp1 * 2
                else:
                    tmp2 = str(tmp1 * 2)
                    summation = summation + int(tmp2[0]) + int(tmp2[1])
            else:
                summation = summation + tmp1
        check = str(10 - (summation % 10))
        if check == '10':
            check = '0'
        return cardNum + check
