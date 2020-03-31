import MySQLdb


def connect_db():
    #  conn = MySQLdb.connect(db='sakila', host='127.0.0.1', user='root', passwd='a2319779', port=3306, charset='utf8')
    conn = MySQLdb.connect(db='wechat_service_test', host='192.168.8.90', user='root', passwd='XMlianluoyimysql!!!', port=32098, charset='utf8')
    return conn


