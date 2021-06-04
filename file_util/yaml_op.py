# -*- coding: utf-8 -*-
import yaml

from utils.log import log


class YamlUtil:
    """使用ruamel对yaml文件的读和写操作"""

    def __init__(self, yaml_path, data=None):

        self.yaml_path = yaml_path
        if data:
            self.data = data

    def read(self):
        """读取yaml里面里面的数据,返回的时字典类型数据"""
        try:
            data = yaml.load(open(self.yaml_path, "r", encoding='utf-8').read(), Loader=yaml.FullLoader)
            return data
        except Exception as e:
            log.error('yaml文件读取失败:%s' % e)

    def write(self):
        """往yaml里面写入数据 """
        try:
            with open(self.yaml_path, "w", encoding="utf-8") as f:
                yaml.dump(self.data, f, Dumper=yaml.Dumper)
                return True
        except Exception as e:
            log.error('yaml文件写入失败:%s' % e)
