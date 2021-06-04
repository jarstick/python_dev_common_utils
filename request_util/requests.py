# -*- coding: utf-8 -*-

from collections import OrderedDict
import re
import aiohttp
import logging.config
import asyncio
import jsonpath
import requests


async def dispatch(method, url, *args, **kwargs):
    async with aiohttp.ClientSession(headers=kwargs.get('headers', 'None')) as session:
        try:
            resp = await session.request(method, url, *args, **kwargs)
            result_text = await resp.text()
        except asyncio.TimeoutError as e:
            logging.error('POST 请求超时了!')
            raise e
        except Exception as e:
            logging.error(e)
            raise e
        return result_text


def concat(connector, params: dict):
    """使用拼接符，拼接字典的k、v"""
    if not isinstance(params, dict):
        raise ValueError('params不是字典')
    params = OrderedDict(sorted(params.items()))
    result = ""
    for key, value in params.items():
        result += f'{connector}{key}={value if value else ""}'
    if result.find(connector) == 0:
        result = result[1:]
    return result


def encode_to_dict(encoded_str):
    """ 将encode后的数据拆成dict
    1.encode_to_dict('name=foo') ,返回{'name': foo'}
    2.encode_to_dict('name=foo&val=bar') , 返回{'name': 'foo', 'val': 'var'}
    """
    pair_list = encoded_str.split('&')
    d = {}
    for pair in pair_list:
        if pair:
            key = pair.split('=')[0]
            val = pair.split('=')[1]
            d[key] = val
    return d


def parse_curl_str(curl: str):
    """接续curl命令,获取参数"""
    if not isinstance(curl, str):
        raise ValueError('curl参数必须是str类型!')

    pattern = re.compile(r"'(.*?)'")
    str_list = [i.strip() for i in re.split(pattern, curl)]
    url = ''
    headers_dict = dict()
    data = ''

    for i in range(0, len(str_list)-1, 2):
        arg = str_list[i]
        string = str_list[i+1]

        if arg.startswith('curl'):
            url = string

        elif arg.startswith('-H'):
            header_key = string.split(':', 1)[0].strip()
            header_val = string.split(':', 1)[1].strip()
            headers_dict[header_key] = header_val

        elif arg.startswith('--data'):
            data = string

    return url, headers_dict, data


def form_data_to_dict(form_data_str):
    """form_data_str是从chrome里边复制得到的form-data表单里的字符串，
    注意*必须*用原始字符串r""
    :param form_data_str: form-data string
    """
    arg_list = [line.strip() for line in form_data_str.split('\n')]
    d = dict()
    for i in arg_list:
        if i:
            k = i.split(':', 1)[0].strip()
            v = ''.join(i.split(':', 1)[1:]).strip()
            d[k] = v
    return d


class Response:
    """封装respons对象处理"""
    def __init__(self, resp: requests):
        self.res = resp

    @property
    def get_json(self):
        try:
            return self.res.json()
        except:
            return self.get_text

    @property
    def get_text(self):
        return self.res.text

    @property
    def get_context(self):
        return self.res.context

    def json_path(self, path):
        return jsonpath.jsonpath(self.get_json, path)