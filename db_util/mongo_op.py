# -*- coding: utf-8 -*-

from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


class MongoConfig:
    """
    MongoConfig MongoDB配置类
    """

    host = 'mongodb'
    port = '27017'
    username = 'root'
    password = ''
    database = ''

    def get_url(self) -> str:
        if self.username and self.password:
            config = [
                'mongodb://',
                self.username,
                ':',
                self.password,
                '@',
                self.host,
                ':',
                self.port,
                '/',
                self.database,
                '?authSource=',
                self.database,
                '&authMechanism=SCRAM-SHA-256',
            ]
            return ''.join(config)
        raise ConnectionError('用户名和密码是必填项!')


class MongoUtils:
    """
    MongoUtils MongoDB工具类
    """

    _config: MongoConfig = None
    default_config: MongoConfig = None

    def __init__(self, config: MongoConfig = None):
        if config:
            self._config = config
        else:
            self._config = self.default_config

    def _get_client(self) -> MongoClient:
        """
        返回Mongo数据库连接，同步
        :return:
        """
        try:
            client = MongoClient(self._config.get_url())
            return client
        except Exception as e:
            raise str(e)

    def _get_db(self) -> Database:
        """
        返回Mongo数据库实例
        :param database:
        :return:
        """

        try:
            client = self._get_client()
            db = client[self._config.database]
            return db
        except Exception as e:
            raise str(e)

    def get_collection(self, collection_name) -> Collection:
        """
        返回输入的名称对应的集合
        :param collection_name:
        :return:
        """

        try:
            db = self._get_db()
            collection: Collection = db[collection_name]
            return collection
        except Exception as e:
            raise str(e)