#! /usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import logging
# logger = logging.getLogger('django.redis')
logger = logging
class Redis_pool(object):
    def __init__(self,host='127.0.0.1',port=6379,db=1,pool=1000):
        self.host=host
        self.port=port
        self.db=db
        self.pool = pool

    # @classmethod
    def get_redis_conn(self):
        conn_pool = redis.ConnectionPool(host=self.host,port=self.port,db=self.db)
        conn = redis.Redis(connection_pool=conn_pool)
        return conn

    @staticmethod
    def lpush(redisKey, data):
        try:
            redisConn = Redis_pool().get_redis_conn()
            redisConn.lpush(redisKey, data)
            redisConn = None
        except Exception, ex:
            logger.warn(msg="Lpush  redis data failed: {ex}".format(ex=str(ex)))
            return False

    @staticmethod
    def rpop(redisKey):
        try:
            redisConn = Redis_pool().get_redis_conn()
            data = redisConn.rpop(redisKey)
            redisConn = None
            return data
        except Exception, ex:
            logger.warn(msg="Rpop redis data failed: {ex}".format(ex=str(ex)))
            return False

    @staticmethod
    def get(redisKey):
        try:
            redisConn = Redis_pool().get_redis_conn()
            data = redisConn.get(redisKey)
            redisConn = None
            return data
        except Exception, ex:
            logger.warn(msg="get redis data failed: {ex}".format(ex=str(ex)))
            return False

    @staticmethod
    def set(redisKey,value):
        try:
            redisConn = Redis_pool().get_redis_conn()
            redisConn.set(redisKey, value)
            redisConn = None
            return value
        except Exception, ex:
            logger.warn(msg="set redis data failed: {ex}".format(ex=str(ex)))
            return False

    @staticmethod
    def delete(redisKey):
        try:
            redisConn = Redis_pool().get_redis_conn()
            data = redisConn.delete(redisKey)
            redisConn = None
            return data
        except Exception, ex:
            logger.warn(msg="Delete redis key failed: {ex}".format(ex=str(ex)))
            return False

if __name__ == '__main__':
    red = Redis_pool.lpush(u'test1234',u'i am a test data')
    print Redis_pool.rpop(u'test1234')
    # Redis_pool.lpush(u'606e9f00-37b6-437c-99c8-8995060fe461', "[Start] Ansible Model: {model}  ARGS:{args}")
    print Redis_pool.rpop(u'938c9f99-df22-4cdc-8bf1-c2a371be6af0')
