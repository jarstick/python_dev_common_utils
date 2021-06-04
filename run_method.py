# -*- coding:utf-8 -*-

import requests
from utils.log import log


class RunMethod:
    def __init__(self):
        self.log = log

    def get_main(self, url, params, headers, files=None):  # 封装get请求
        if headers:
            if files:
                res = requests.get(url=url, params=params, headers=headers, files=files, verify=False)
            else:
                res = requests.get(url=url, params=params, headers=headers, verify=False)
            return res
        else:
            if files:
                res = requests.get(url=url, params=params, files=files, verify=False)
            else:
                res = requests.get(url=url, params=params, verify=False)
            return res

    def post_main(self, url, data, headers, files=None):  # 封装post请求
        if headers:
            if files:
                res = requests.post(url=url, data=data, headers=headers, files=files, verify=False)
            else:
                res = requests.post(url=url, data=data, headers=headers, verify=False)
            return res
        else:
            if files:
                res = requests.post(url=url, data=data, files=files, verify=False)
            else:
                res = requests.post(url=url, data=data, verify=False)
            return res

    def put_main(self, url, data, headers, files=None):  # 封装put请求
        if headers:
            if files:
                res = requests.put(url=url, data=data, headers=headers, files=files, verify=False)
            else:
                res = requests.put(url=url, data=data, headers=headers, verify=False)
            return res
        else:
            if files:
                res = requests.put(url=url, data=data, files=files, verify=False)
            else:
                res = requests.put(url=url, data=data, verify=False)
            return res

    def delete_main(self, url, data, headers, files=None):  # 封装put请求
        if headers:
            if files:
                res = requests.delete(url=url, data=data, headers=headers, files=files, verify=False)
            else:
                res = requests.delete(url=url, data=data, headers=headers, verify=False)
            return res
        else:
            if files:
                res = requests.delete(url=url, data=data, files=files, verify=False)
            else:
                res = requests.delete(url=url, data=data, verify=False)
            return res

    def run_main(self, method, url, data=None, headers=None, files=None, res_format='json'):  # 封装主请求
        '''参数1：请求方式，参数2：请求data，参数3：请求信息头，参数4：返回的数据格式'''
        res = None
        if method.lower() == 'get' or method.upper() == 'GET':
            res = self.get_main(url=url, params=data, headers=headers, files=files)
        elif method.lower() == 'post' or method.upper() == 'POST':
            res = self.post_main(url=url, data=data, headers=headers, files=files)
        elif method.lower() == 'put' or method.upper() == 'PUT':
            res = self.put_main(url=url, data=data, headers=headers, files=files)
        elif method.lower() == 'delete' or method.upper() == 'DELETE':
            res = self.delete_main(url=url, data=data, headers=headers, files=files)
        else:
            self.log.info("暂不支持的请求方式")
            raise Exception("暂不支持的请求方式")
            # dumps方法:
            # sort_keys是告诉编码器按照字典排序(a到z)输出,indent参数根据数据格式缩进显示，读起来更加清晰:
            # separators参数的作用是去掉,,:后面的空格,skipkeys可以跳过那些非string对象当作key的处理,
            # 输出真正的中文需要指定ensure_ascii=False
        self.log.info("请求响应时间为：{}s".format(res.elapsed.total_seconds()))
        self.log.info("请求响应状态码：{}".format(res.status_code))
        if res:
            try:
                if res_format.lower() == 'json' or res_format.upper() == 'JSON':  # 以json格式返回数据
                    '''ensure_ascii:处理json编码问题（中文乱码），separators：消除json中的所有空格'''
                    response = res.json()
                elif res_format.lower() == 'text' or res_format.upper() == 'TEXT':  # 以文本格式返回数据
                    response = res.text
                elif res_format.lower() == 'str' or res_format.upper() == 'STR':  # 以文本格式返回数据
                    response = res.text
                elif res_format.lower() == 'content' or res_format.upper() == 'CONTENT':  # 以二进制形式返回响应数据
                    response = res.content
                else:  # 以json格式返回数据
                    response = res.json()
                # print(response)
                return response
            except BaseException as e:
                self.log.error('error:{}'.format(e))
                print(e)
                # print(res.text)
        else:
            return None
