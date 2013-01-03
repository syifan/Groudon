#-*- coding:utf-8 -*-
import MySQLdb
import sys
#连接MySQL数据库函数

def connMysql():
    try:
        conn =\
        MySQLdb.connect(host='localhost',user='root',passwd='chensi',db='gr')
        return conn
    except Exception,e:
        print e
        sys.exit()
