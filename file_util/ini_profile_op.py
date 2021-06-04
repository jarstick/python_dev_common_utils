# -*- coding: utf-8 -*-

import configparser


class IniUtil:
    """
    解析ini配置文件
    """

    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def add_section(self, section):
        """
        添加section节点
        """
        sections = self.config.sections()
        if section in sections:
            return
        else:
            self.config.add_section(section)

    def remove_section(self, section):
        """
        移除指定的节
        """
        return self.config.remove_section(section)

    def get(self, section, option):
        """
        根据section和option取值
        """
        return self.config.get(section, option)

    def set(self, section, option, value):
        """
        新增配置项
        """
        if self.config.has_section(section):
            self.config.set(section, option, value)

    def remove_option(self, section, option):
        """
        移除指定节内的指定选项

        """
        if self.config.has_section(section):
            self.config.remove_option(section, option)
            return True

        return False

    def get_items(self, section):
        """
        返回节点内的键值列表
        """
        return self.config.items(section)

    def get_sections(self):
        """
        返回所有节的列表
        """
        return self.config.sections()

    def get_options(self, section):
        """
        返回节内的键列表
        """
        return self.config.options(section)


config_parse = IniUtil()
