import MySQLdb
import traceback

date_name = 'world'


def connect_db():
    conn = MySQLdb.connect(db=date_name, host='127.0.0.1', user='root', passwd='a2319779', port=3306, charset='utf8')
    #conn = MySQLdb.connect(db='wechat_service_test', host='192.168.8.90', user='root', passwd='XMlianluoyimysql!!!', port=32098, charset='utf8')
    return conn


def get_table_list_map():
    return {'tableList':  get_table_list()}


def get_table_list():
    cursor = connect_db().cursor()

    table_list = []
    sql = """SELECT
             TABLE_NAME 
             FROM
                information_schema.TABLES 
             WHERE
                TABLE_SCHEMA = """ + "'" + date_name + "'"

    try:
        # 执行sql语句获取队列类型及备注
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            table_list.append(row[0])
        return table_list
    except Exception:
        print('traceback.format_exc():\n%s' % traceback.format_exc())

3