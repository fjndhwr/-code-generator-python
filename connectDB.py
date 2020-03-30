import MySQLdb


def connect_db():
    conn = MySQLdb.connect(db='sakila', host='127.0.0.1', user='root', passwd='a2319779', port=3306, charset='utf8')
    return conn


