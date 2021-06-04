# -*- coding: utf-8 -*-

import datetime
from typing import List, Callable

from elasticsearch import Elasticsearch, helpers
from urllib3.connectionpool import xrange
from utils.Constants import *

from utils.log import log
from utils.wrapper_util.wrappers import catch_and_print_exception

es_host = ""
port = ""
timeout = ""

index_result = []


class EsConnectionConfig:
    def __init__(self, es_index: str, doc_type: str, host: str = "localhost", port: int = 9200):
        self.es_index = es_index
        self.doc_type = doc_type
        self.client = Elasticsearch([f"{host}:{port}"], maxsize=25)


DEFAULT_ES_CONFIG = EsConnectionConfig(es_index="sca-tag-client", doc_type="client")


class EsUtil:
    """ES的增删改查"""

    def __init__(self, es_config: EsConnectionConfig):
        super().__init__(name="es")
        self.index = es_config.es_index
        self.doc_type = es_config.doc_type
        self.client = es_config.client
        log.info("当前要执行的 索引是 %s , 类型是 %s" % (self.index, self.doc_type))

    @catch_and_print_exception
    def batch_insert_or_update_by_bulk(self, data_list: List[dict], is_only_print_sql: bool = False,
                                       id_column: str = "id"):
        action_list = []
        if data_list:
            for data in data_list:
                new_action = {"_index": self.index, "_type": self.doc_type, "_id": data[id_column], "_op_type": 'index',
                              "_source": data}
                if is_only_print_sql:
                    log.info("将要执行的批量插入或更新的语句是: %s" % new_action)
                else:
                    action_list.append(new_action)
            if action_list:
                result = helpers.bulk(self.client, action_list)
                log.info("批量执行的插入或更新的结果是: %s" % result)

    def batch_insert_or_update_es(self, result_list: List[dict], is_only_print_sql: bool = False,
                                  batch_size: int = 5000, id_column: str = "id"):
        """
        批量插入或更新es
        """
        num = 0
        temp_res_list = []
        if result_list:
            for result in result_list:
                num += 1
                temp_res_list.append(result)
                if num % batch_size == 0:
                    self.batch_insert_or_update_by_bulk(
                        temp_res_list
                        , is_only_print_sql=is_only_print_sql
                        , id_column=id_column
                    )
                    temp_res_list.clear()
                    log.info("完成第 %d 个" % num)
            else:
                self.batch_insert_or_update_by_bulk(
                    temp_res_list
                    , is_only_print_sql=is_only_print_sql
                    , id_column=id_column
                )
                temp_res_list.clear()
                log.info("完成第 %d 个" % num)
        else:
            log.info("没有查询到符合条件的数据")

    @catch_and_print_exception
    def batch_part_update_by_bulk(self, data_list: List[dict], is_only_print_sql: bool = False, id_column: str = "id"):
        action_list = []
        if data_list:
            for data in data_list:
                new_action = {"_index": self.index, "_type": self.doc_type, "_id": data[id_column],
                              "_op_type": 'update',
                              "doc": data}
                if is_only_print_sql:
                    log.info("将要执行的批量插入或更新的语句是: %s" % new_action)
                else:
                    action_list.append(new_action)
            if action_list:
                result = helpers.bulk(self.client, action_list)
                log.info("批量执行的批量部分更新的结果是: %s" % result)

    def batch_update_es(self
                        , result_list: List[dict]
                        , batch_size: int = 5000
                        , is_only_print_sql: bool = False
                        , id_column: str = "id"
                        ):
        num = 0
        temp_res_list = []
        if result_list:
            for result in result_list:
                num += 1
                temp_res_list.append(result)
                if num % batch_size == 0:
                    self.batch_part_update_by_bulk(
                        temp_res_list
                        , is_only_print_sql=is_only_print_sql
                        , id_column=id_column
                    )
                    temp_res_list.clear()
                    log.info("完成第 %d 个" % num)
            else:
                self.batch_part_update_by_bulk(
                    temp_res_list
                    , is_only_print_sql=is_only_print_sql
                    , id_column=id_column
                )
                temp_res_list.clear()
                log.info("完成第 %d 个" % num)
        else:
            log.info("没有查询到符合条件的数据")

    @catch_and_print_exception
    def batch_insert_by_bulk(self, data_list: List[dict], is_only_print_sql: bool = False, id_column: str = "id"):
        action_list = []
        if data_list:
            for data in data_list:
                if data.get(id_column):
                    new_action = {"_index": self.index, "_type": self.doc_type, "_id": data[id_column],
                                  "_op_type": 'create',
                                  "_source": data}
                    if is_only_print_sql:
                        log.info("将要执行的批量插入的语句是: %s" % new_action)
                    else:
                        action_list.append(new_action)
                else:
                    self.client.index(index=self.index, doc_type=self.doc_type, body=data)

            if action_list:
                result = helpers.bulk(self.client, action_list)
                log.info("批量执行的批量插入的结果是: %s" % result)

    def batch_insert_es(self
                        , result_list: List[dict]
                        , batch_size: int = 5000
                        , is_only_print_sql: bool = False
                        , id_column: str = "id"
                        ):
        num = 0
        temp_res_list = []
        if result_list:
            for result in result_list:
                num += 1
                temp_res_list.append(result)
                if num % batch_size == 0:
                    self.batch_insert_by_bulk(
                        temp_res_list
                        , is_only_print_sql=is_only_print_sql
                        , id_column=id_column
                    )
                    temp_res_list.clear()
                    log.info("完成第 %d 个" % num)
            else:
                self.batch_insert_by_bulk(
                    temp_res_list
                    , is_only_print_sql=is_only_print_sql
                    , id_column=id_column
                )
                temp_res_list.clear()
                log.info("完成第 %d 个" % num)
        else:
            log.info("没有查询到符合条件的数据")

    @catch_and_print_exception
    def batch_delete_by_bulk(self, data_list: List[dict], is_only_print_sql: bool = False, id_column: str = "id"):
        action_list = []
        if data_list:
            for data in data_list:
                new_action = {"_index": self.index, "_type": self.doc_type, "_id": data[id_column],
                              "_op_type": 'delete'}
                if is_only_print_sql:
                    log.info("将要执行的删除语句是: %s" % new_action)
                else:
                    action_list.append(new_action)
            if action_list:
                result = helpers.bulk(self.client, action_list)
                log.info("批量执行的删除的结果是: %s" % result)

    def batch_delete_es(self
                        , result_list: List[dict]
                        , batch_size: int = 5000
                        , is_only_print_sql: bool = False
                        , id_column: str = "id"
                        ):
        num = 0
        temp_res_list = []
        if result_list:
            for result in result_list:
                num += 1
                temp_res_list.append(result)
                if num % batch_size == 0:
                    self.batch_delete_by_bulk(
                        temp_res_list
                        , is_only_print_sql=is_only_print_sql
                        , id_column=id_column
                    )
                    temp_res_list.clear()
                    log.info("完成第 %d 个" % num)
            else:
                self.batch_delete_by_bulk(
                    temp_res_list
                    , is_only_print_sql=is_only_print_sql
                    , id_column=id_column
                )
                temp_res_list.clear()
                log.info("完成第 %d 个" % num)
        else:
            log.info("没有查询到符合条件的数据")

    def query_by_id(self, id_str):
        res = self.client.get(index=self.index, doc_type=self.doc_type, id=id_str)
        if res and res["hits"]["total"] > 0:
            return res["hits"]["hits"]

    def query_by_scroll(self, query_body: dict, handle_func: Callable[[List[dict], int], object] = None):
        page = self.client.search(
            index=self.index,
            doc_type=self.doc_type,
            scroll='2m',
            size=10000,
            body=query_body)

        total = 0
        scroll_index = 0
        log.info("Scrolling...")
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']
        page_result = page['hits']['hits']
        result_list = [hits["_source"] for hits in page_result]
        if handle_func:
            handle_func(result_list, scroll_index)
            total += scroll_size
            log.info(f"scroll size: {len(result_list)} ")

        # Start scrolling
        while scroll_size > 0:
            scroll_index += 1
            page = self.client.scroll(scroll_id=sid, scroll='2m')
            sid = page['_scroll_id']
            page_result = page['hits']['hits']
            result_list = [hits["_source"] for hits in page_result]
            scroll_size = len(result_list)
            if handle_func:
                handle_func(result_list, scroll_index)
                log.info(f"scroll size: {scroll_size} ")
        else:
            log.info(f" total size: {total} ")

    @staticmethod
    def get_result_by_index(index, **kwargs):
        """根据索引全名获取所有数据"""
        es = Elasticsearch(
            hosts=es_host if kwargs.get('host') is None else kwargs.get('host'),
            port=port if kwargs.get('port') is None else kwargs.get('port'),
            timeout=timeout if kwargs.get('timeout') is None else kwargs.get('timeout'))
        count = es.count(index=index)['count']
        # 每页显示条数
        page_line = 2
        # 显示多少页
        if count % page_line == 0:
            page = int(count / page_line)
        else:
            page = int(count / page_line + 1)

        for x in xrange(0, page):
            rs = es.search(index=index, body={
                "query": {
                    "match_all": {}
                },
                "from": x * page_line,
                "size": page_line
            })
            for hit in rs['hits']['hits']:
                log.info(hit)
                index_result.append(hit)
        return index_result

    @staticmethod
    def get_total_result_by_index_prefix(prefix_index, **kwargs):
        """根据索引前缀获取所有数据"""
        for e in range(0, -3650, -1):
            date = (datetime.datetime.now() + datetime.timedelta(days=e)).strftime("%Y.%m.%d")
            index = prefix_index + "-" + str(date)
            try:
                EsUtil.get_result_by_index(index, **kwargs)
            except:
                break
        return index_result


class Es2File(EsUtil):

    def __init__(self, es_config: EsConnectionConfig, export_file_name: str = "从es中导出"):
        super().__init__(es_config=es_config)
        self.export_file_name = export_file_name

    @abstractmethod
    def handle_export_data_list(self, item_list: List[dict], scroll_index: int) -> list:
        raise NotImplementedError

    def export_file(self, item_list: List[dict], scroll_index: int):
        line_list = self.handle_export_data_list(item_list, scroll_index)
        write_file_quick(line_list, export_file_name=self.export_file_name, write_type="append")

    def export_es_data_2_file(self, query_body: dict):
        self.query_by_scroll(query_body=query_body, handle_func=self.export_file)


class Es2MySql(object):

    def __init__(self, es_config: EsConnectionConfig, db_config: mysql_config):
        super().__init__()
        self.es = Es(es_config)
        self.mysql = MySql
        self.start_end_tuple_list = None
        self.update_key_prefix = None
        self.condition = None
        self.end = None
        self.start = None
        self.exclude_properties = None
        self.is_only_print_sql = None
        self.optional = None
        self.batch_size = None
        self.table_name = None

    @abstractmethod
    def handle_export_data_list(self, item_list: List[dict]) -> List[dict]:
        pass

    def import_mysql(self, item_list: List[dict]):
        handle_item_list = self.handle_export_data_list(item_list)
        self.mysql.batch_update_by_item_list(handle_item_list, self.table_name, batch_size=self.batch_size,
                                             optional=self.optional,
                                             is_only_print_sql=self.is_only_print_sql,
                                             exclude_properties=self.exclude_properties,
                                             start=self.start, end=self.end, condition=self.condition,
                                             update_key_prefix=self.update_key_prefix,
                                             start_end_tuple_list=self.start_end_tuple_list)

    def export_es_data_2_mysql(self
                               , query_body: dict
                               , table_name: str
                               , batch_size=100
                               , optional: str = None
                               , is_only_print_sql: bool = False
                               , exclude_properties: list = None
                               , start: int = None
                               , end: int = None
                               , condition: dict = None
                               , start_end_tuple_list: list = None
                               , update_key_prefix: str = None
                               ):
        self.start_end_tuple_list = start_end_tuple_list
        self.update_key_prefix = update_key_prefix
        self.condition = condition
        self.end = end
        self.start = start
        self.exclude_properties = exclude_properties
        self.is_only_print_sql = is_only_print_sql
        self.optional = optional
        self.batch_size = batch_size
        self.table_name = table_name
        self.es.query_by_scroll(query_body=query_body, handle_func=self.import_mysql)



class MySql2Es(object):
    def __init__(self, es_config: EsConnectionConfig, db_config: MysqlConnectionConfig):
        super().__init__()
        self.es = Es(es_config)
        self.mysql = MySql(db_config)
        self.id_column = "id"
        self.batch_size = 10000
        self.is_only_print_sql = False
        self.optional = "Update"

    def sync_from_mysql_2_es(self
                             , table_name: str
                             , where: str = None
                             , column: list = None
                             , column_str: str = None
                             , batch_size: int = 10000
                             , distinct: bool = False
                             , datetime_formatter: str = None
                             , is_fixed_start: bool = False
                             , optional: str = "Update"
                             , id_column: str = "id"
                             , is_only_print_sql: bool = False
                             ):
        self.optional = optional
        self.id_column = id_column
        self.batch_size = batch_size
        self.is_only_print_sql = is_only_print_sql
        self.mysql.batch_handle_db_data_by_generator(table_name
                                                     , where=where
                                                     , column=column
                                                     , column_str=column_str
                                                     , batch_size=batch_size
                                                     , distinct=distinct
                                                     , datetime_formatter=datetime_formatter
                                                     , is_fixed_start=is_fixed_start
                                                     , handle_func=self.handle_query_result
                                                     )

    def handle_query_result(self, one_generator_return_list):
        result_list_init = self.pre_handle_db_query_result_list(one_generator_return_list)
        result_list = [item for item in result_list_init if item]
        if "Update" == self.optional:
            self.es.batch_update_es(
                result_list
                , is_only_print_sql=self.is_only_print_sql
                , batch_size=self.batch_size
                , id_column=self.id_column
            )
        elif "Insert" == self.optional:
            self.es.batch_insert_es(
                result_list
                , is_only_print_sql=self.is_only_print_sql
                , batch_size=self.batch_size
                , id_column=self.id_column
            )
        elif "InsertOrUpdate" == self.optional:
            self.es.batch_insert_or_update_es(
                result_list
                , is_only_print_sql=self.is_only_print_sql
                , batch_size=self.batch_size
                , id_column=self.id_column
            )
        elif "Delete" == self.optional:
            self.es.batch_delete_es(
                result_list
                , is_only_print_sql=self.is_only_print_sql
                , batch_size=self.batch_size
                , id_column=self.id_column
            )
        else:
            msg = f"只支持[Update, Delete, Insert, InsertOrUpdate]操作, 不支持当前操作{self.optional}"
            raise RuntimeError(msg)

    @abstractmethod
    def pre_handle_db_query_result_list(self, pre_result_list: List[dict]) -> List[dict]:
        raise NotImplementedError



