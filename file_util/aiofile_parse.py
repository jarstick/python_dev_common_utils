# -*- coding: utf-8 -*-

import hashlib
import os
import shutil
import time

import aiofiles as aiofiles
import yaml
from ruamel.yaml.loader import SafeLoader


async def yaml_load(dir_abspath=None, file_abspath=None):
    """
    :param dir_abspath: 文件夹绝对路径
    :param file_abspath: 文件绝对路径
    :return: 1.如果入参是dir_abspath,则解析此路径下所有的文件,以文件名为key,文件内容为value,返回 {'文件名1':'内容1','文件名2':'内容2'};
             2.如果入参是file_path,则解析当前文件内容,返回{'内容'};
             3.入参格式不正确,抛出KeyError;
    """
    data_dict = dict()
    if dir_abspath and file_abspath is None:
        for root, dirs, files in os.walk(dir_abspath):
            for file in files:
                file_path = ''.join([root, os.sep, file])
                async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    data = yaml.load(await f.read(), Loader=SafeLoader)
                    data_dict.setdefault(file, data)
        return data_dict
    elif not dir_abspath and file_abspath:
        async with aiofiles.open(file_abspath, 'r', encoding='utf-8', errors='ignore') as f:
            data = yaml.load(await f.read(), Loader=SafeLoader)
        return data
    else:
        raise KeyError('请确认参数dir_abspath、file_abspath是否正确!')


def get_suffix(filename, has_dot=False):
    """获取文件扩展名"""
    pos = filename.rfind('.')
    if 0 < pos < len(filename) - 1:
        index = pos if has_dot else pos + 1
        return filename[index:]
    else:
        return ''


def file_classification(path, save_path=None, recursion=True, mode='m'):
        """
        文件分类处理,相同拓展名的文件放在同一个目录下
        :param path: 需要分类处理的路径
        :param save_path: 分类后文件保存路径 为空时默认保存在当前路径
        :param recursion: 是否递归处理,默认True
        :param mode: 模式 c 复制 m 移动 默认值
        :return:None
        """

        if not save_path:
            save_path = path

        if os.path.isdir(path):
            files = os.listdir(path)

            for file in files:
                file = "%s%s%s" % (path, os.sep, file)
                # 如果是目录 并且recursion=True 递归统计
                if os.path.isdir(file) and recursion:
                    file_classification(file, save_path, recursion, mode)

                if os.path.isfile(file):
                    suffix = get_suffix(file)
                    if not suffix:
                        suffix = "other"
                    save_dir = "%s%s%s" % (save_path, os.sep, suffix)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    with open(file, encoding="UTF-8") as f:
                        if mode == 'c':
                            try:
                                shutil.copy2(file, save_dir)
                            except Exception:
                                fname = os.path.basename(file)
                                if os.path.exists(save_dir + "/" + fname):
                                    save_dir += "/" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + fname
                                shutil.copy2(file, save_dir)
                        else:
                            f.close()
                            try:
                                shutil.move(file, save_dir)
                            except Exception:
                                pass


def rm_empty_dir(dir_path):
    """删除空目录"""
    for root, dirs, files in os.walk(dir_path):
        if not os.listdir(root):
            os.rmdir(root)


def get_file_md5(file_path):
    """获取文件的MD5值
    :param file_path: 文件地址
    :return: MD5校验值
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'{file_path}文件不存在或者不是文件')
    hash_ = hashlib.md5()
    f = open(file_path, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        else:
            hash_.update(b)
    f.close()
    data = hash_.hexdigest()
    if data and isinstance(data, str):
        return data.upper()
    return ''
