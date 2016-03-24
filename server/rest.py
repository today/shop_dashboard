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
        return getCount()

def getCount():
    # 打开数据库连接
    db = MySQLdb.connect("localhost","root","","eshop" )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    cursor.execute("SELECT count(*) as onlineCount from nbt_customer_activity")
    # 使用 fetchone() 方法获取一条数据库。
    data = cursor.fetchone()
    print "Database version : %s " % data
    # 关闭数据库连接
    db.close()
    return "%s" % data



if __name__ == "__main__":
    app = web.application(urls, globals())
    #session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
    app.run()
