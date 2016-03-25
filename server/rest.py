# -*- coding: utf-8 -*-  

import codecs
import glob
import json
import os
import sys
import shutil
import web
import MySQLdb

web.config.debug = True

FLAG_SUCCESS = '{"flag":"successful"}'

FLAG_ERROR_FILE_NOT_FOUND = '{"flag":"error","error_no":"10001","msg":"File not found."}'
FLAG_ERROR_TYPE_INVALID = '{"flag":"error","error_no":"10002","msg":"Type invalid."}'

urls = (
    '/onlineCount', 'onlineCount',
    '/orderCount', 'orderCount',
    '/orderSum', 'orderSum',
    '/orderTop10', 'orderTop10',
    "/(.*)", "blankPage"
)

class blankPage:
    def GET(self, urls):
        print "blankPage get"
        return "hello"

class onlineCount:
    def GET(self, urls):
        print "get2"
        return getCount()
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return getOnlineCount()

class orderCount:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return getOrderCount()

class orderSum:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return getOrderSum()

class orderTop10:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return getOrderTop()

def getOnlineCount():
    db = getConnect()
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    cursor.execute("SELECT count(*) as onlineCount from nbt_customer_activity")
    # 使用 fetchone() 方法获取一条数据库。
    data = cursor.fetchone()
    print "Database : %s " % data
    # 关闭数据库连接
    db.close()
    return "%s" % data

def getOrderCount():
    db = getConnect()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) as orderCount from nbt_order")
    data = cursor.fetchone()
    print "Database : %s " % data
    db.close()
    return "%s" % data

def getOrderSum():
    db = getConnect()
    cursor = db.cursor()
    cursor.execute("SELECT sum(total) as orderCount from nbt_order")
    data = cursor.fetchone()
    print "Database : %s " % data
    db.close()
    return "%s" % data

def getOrderTop():
    db = getConnect()
    cursor = db.cursor()
    cursor.execute("SELECT name,total from nbt_order_product order by total desc limit 10")
    result = {}
    prod_names = []
    prod_totals = []
    for ( name, total ) in cursor:
        prod_names.append(name)
        prod_totals.append( str(total) )
        result['name'] = prod_names
        result['total'] = prod_totals
    #print result
    #print json.dumps(result, ensure_ascii=False,indent=2)
    db.close()
    return json.dumps(result, ensure_ascii=False,indent=2)

def getConnect():
    # 打开数据库连接 
    return MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,db='eshop', charset='utf8')


if __name__ == "__main__":
    app = web.application(urls, globals())
    #session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
    app.run()
