# -*- coding: utf-8 -*-

import time
import datetime
from typing import Union

from dateutil import rrule

from utils.log import log


class DateTimeUtil:
    YEAR_FORMAT = "%Y"
    MONTH_FORMAT = "%Y.%m"
    DAY_FORMAT = "%Y.%m.%d"
    MINUTE_FORMAT = "%Y.%m.%d %H:%M"
    SECOND_FORMAT = "%Y.%m.%d %H:%M:%S"

    @staticmethod
    def timeStamp2date(timeStamp=''):
        if timeStamp == '':
            timeStamp = int(time.time())
        # # 使用time
        # timeArray = time.localtime(timeStamp)
        # date = time.strftime("%Y-%m-%d", timeArray)

        # 使用datetime
        datetimeArray = datetime.datetime.fromtimestamp(timeStamp)
        date = datetimeArray.strftime("%Y-%m-%d")
        return date

    @staticmethod
    def timeStamp2datetime(timeStamp=''):
        if timeStamp == '':
            timeStamp = int(time.time())
        # # 使用time
        # timeArray = time.localtime(timeStamp)
        # date_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        # 使用datetime
        datetimeArray = datetime.datetime.fromtimestamp(timeStamp)
        date_time = datetimeArray.strftime("%Y-%m-%d %H:%M:%S")
        return date_time

    @staticmethod
    def datetime2timeStamp(date_time=''):
        if date_time == '':
            date_time = str(datetime.datetime.now())[:19]
        # 转为时间数组
        timeArray = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        # 转为时间戳
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    @staticmethod
    def timeStamp10():
        return int(time.time())

    @staticmethod
    def timeStamp13():
        return int(round(time.time() * 1000))

    @staticmethod
    def now(**kwargs):
        return (datetime.datetime.now() + datetime.timedelta(
            days=0 if kwargs.get('add_days') is None else kwargs.get('add_days'))) \
            .strftime(DateTimeUtil.SECOND_FORMAT if kwargs.get('format') is None else kwargs.get('format'))

    @staticmethod
    def compare_months(begin, end):
        """比较两个日期相差几个月"""
        d1 = datetime.datetime.strptime(begin, '%Y-%m-%d')
        d2 = datetime.datetime.strptime(end, '%Y-%m-%d')
        months = rrule.rrule(rrule.MONTHLY, dtstart=d1, until=d2).count()
        return months

    @staticmethod
    def compare_days(begin, end):
        """比较两个日期相差多少天"""
        begin = begin.split('-')
        end = end.split('-')
        d = int(begin[2])
        m = int(begin[1])
        y = int(begin[0])
        dd = int(end[2])
        dm = int(end[1])
        dy = int(end[0])
        begind = datetime.date(y, m, d)
        endd = datetime.date(dy, dm, dd)
        return (endd - begind).days + 1

    @staticmethod
    def compare_years(begin, end):
        """比较两个日期相差多少年"""
        begin = int(begin)
        end = int(end)
        return end - begin + 1

    @staticmethod
    def generate_continuous_dates(begin, end):
        """生成两个日期之间连续的时间列表,包含边界"""
        ymd = "%Y-%m-%d"
        if len(begin) == 7:
            ymd = "%Y-%m"
        if len(begin) == 4:
            c = int(end) - int(begin) + 1
            year = []
            for i in range(c):
                year.append(str(int(begin) + i))
            return sorted(year)
        dates = []
        dt = datetime.datetime.strptime(begin, ymd)
        date = begin[:]
        while date <= end:
            dates.append(date)
            dt = dt + datetime.timedelta(1)
            date = dt.strftime(ymd)
        return sorted(set(dates))

    @staticmethod
    def date_up(begin, several):
        """时间增长 几天几个月几年,如传入'2021',1则表示需要增长1年;若入参为'2021-02',1,则表示需要增长个月,天同理"""
        if several == 0:
            return begin
        if len(begin) == 4:
            return int(begin) + several
        elif len(begin) == 7:
            b = begin.split('-')
            m = int(b[1]) + several
            y = int(b[0])
            if m > 12:
                y = int(b[0]) + int(m / 12)
                m = m % 12
            result_date = str(y) + '-' + str(m)
            return result_date
        else:
            b = begin.split('-')
            s = datetime.date(int(b[0]), int(b[1]), int(b[2]))
            result_date = s + datetime.timedelta(days=several)
            return result_date.strftime('%Y-%m-%d')

    @staticmethod
    def compare(start, end):
        """比较时间或日期,返回bool"""
        a = int(start.replace('-', ''))
        b = int(end.replace('-', ''))
        if a > b:
            return False
        return True

    @staticmethod
    def formatter_datetime_2_iso8601(t: Union[datetime.date, datetime.time, datetime.datetime]):
        """
        格式化 日期时间 为 iso8601 格式字符串
        :param t:
        :return:
        """
        return t.isoformat()

    @staticmethod
    def formatter_datetime_2_str(t: Union[datetime.date, datetime.time, datetime.datetime]):
        """
        根据不同的日期时间类型 格式化成常见的格式字符串
        :param t:
        :return:
        """
        if isinstance(t, datetime.datetime):
            return t.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(t, datetime.time):
            return t.strftime('%H:%M:%S')
        elif isinstance(t, datetime.date):
            return t.strftime("%Y-%m-%d")

    @staticmethod
    def formatter_datetime_2_timestamp(t: Union[datetime.date, datetime.time, datetime.datetime], unit: str):
        """
        将日期或时间格式化成时间戳
        :param t:
        :param unit:
        :return:
        """
        if "second" == unit:
            if t:
                if isinstance(t, datetime.date):
                    return datetime.datetime(t.year, t.month, t.day).timestamp()
                else:
                    return int(t.timestamp())
            else:
                return None
        elif "millisecond" == unit:
            if t:
                try:
                    if isinstance(t, datetime.date):
                        return int(datetime.datetime.fromordinal(t.toordinal()).timestamp() * 1000)
                    else:
                        return int(t.timestamp() * 1000)
                except OSError:
                    log.exception(msg="出问题的时间是%s" % t)
                    return None
            else:
                return None
        else:
            raise RuntimeWarning("暂只支持转换为秒或毫秒")

    @staticmethod
    def formatter_datetime(res, datetime_formatter: str = "datetime", unit: str = "millisecond"):
        """
        按照指定格式 格式化时间
        :param res:
        :param datetime_formatter:
        :param unit:
        :return:
        """
        if isinstance(res, datetime.date) \
            or isinstance(res, datetime.time) \
            or isinstance(res, datetime.datetime):

            if datetime_formatter not in ["datetime", "iso8601", "str", "long"]:
                error_msg = f"不支持当前时间格式化类型 {datetime_formatter}, 仅支持'datetime', 'iso8601', 'str', 'long'"
                raise RuntimeWarning(error_msg)
            if "datetime" == datetime_formatter:
                return res
            elif "iso8601" == datetime_formatter:
                return DateTimeUtil.formatter_datetime_2_iso8601(res)
            elif "str" == datetime_formatter:
                return DateTimeUtil.formatter_datetime_2_str(res)
            elif "long" == datetime_formatter:
                return DateTimeUtil.formatter_datetime_2_timestamp(res, unit)
            else:
                return res
        else:
            return res

    @staticmethod
    def formatter_line(result: list, datetime_formatter: str = None):
        new_result_list = []
        for res in result:
            new_res = DateTimeUtil.formatter_datetime(res, datetime_formatter)
            new_result_list.append(new_res)
        return new_result_list
