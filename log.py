# -*- coding: utf-8 -*-

import os
import datetime
from loguru import logger


class Log:
    __instance = None
    DATE = datetime.datetime.now().strftime('%Y-%m-%d')

    logs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + 'logs'
    if not os.path.isdir(logs_path):
        os.makedirs(logs_path)
    logger.add('%s%s%s.log' % (logs_path, os.sep, DATE),
               format="{level} | {time:YY-MM-DD HH:mm:ss} | {message}",
               encoding='utf-8',
               retention='1 days',  # 设置历史保留时长
               backtrace=True,  # 回溯
               diagnose=True,  # 诊断
               enqueue=True,  # 异步写入
               rotation="1MB",  # 切割，设置文件大小，当日志文件达到500MB时就会重新生成一个文件
               # rotation="00:00", # 每天0点就会创建新的文件
               # filter="my_module"  # 过滤模块
               # compression="zip"   # 文件压缩
               )

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Log, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def info(self, msg, *args, **kwargs):
        return logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        return logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        return logger.exception(msg, *args, exc_info=True, **kwargs)


log = Log()