#!/usr/bin/env python
#-*- coding: utf-8 -*- 

import MySQLdb
import time
import string
from DBUtils.PooledDB import PooledDB
import dbconfig
import datetime
import base64

DBConfig = dbconfig.Parser()

class DbManager():
    def __init__(self):
        kwargs = {}
        kwargs['host'] =  DBConfig.getConfig('database', 'dbhost')
        kwargs['port'] =  int(DBConfig.getConfig('database', 'dbport'))
        kwargs['user'] =  DBConfig.getConfig('database', 'dbuser')
        kwargs['passwd'] =  DBConfig.getConfig('database', 'dbpassword')
        kwargs['db'] =  DBConfig.getConfig('database', 'dbname')
        kwargs['charset'] =  DBConfig.getConfig('database', 'dbcharset')
        self._pool = PooledDB(MySQLdb, mincached=1, maxcached=5, maxshared=10, maxusage=10000, **kwargs)

    def getConn(self):
        return self._pool.connection()

_dbManager = DbManager()

def getConn():
    return _dbManager.getConn()

def NoLive(gid):
    con = getConn()
    cur =  con.cursor()
    sql = """update live set url = "http://vodcdn.southtv.cn/logo/no.jpg" where gid = "%s"  """%(gid)
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

def Live(gid):
    con = getConn()
    cur =  con.cursor()
    sql = """update live set url = "http://new.southtv.cn:9180/%s/live.m3u8" where gid = "%s"  """%(gid, gid)
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

if __name__ == '__main__':
    Live("gdty")
