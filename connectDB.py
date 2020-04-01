import MySQLdb
import traceback

#date_name = 'world'
date_name = 'wechat_service_test'

def connect_db():
#    conn = MySQLdb.connect(db=date_name, host='127.0.0.1', user='root', passwd='a2319779', port=3306, charset='utf8')
    conn = MySQLdb.connect(db=date_name, host='192.168.8.90', user='root', passwd='XMlianluoyimysql!!!', port=32098, charset='utf8')
    return conn


def get_table_list_map():
    table_list = get_table_list()
    return {'tableList':  table_list,
            'len': [x for x in range(len(table_list))]}


def get_table_list():
    size = 10
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
        return list_of_groups(table_list, 20)
    except Exception:
        print('traceback.format_exc():\n%s' % traceback.format_exc())


def list_of_groups(init_list, childern_list_len):
    list_of_group = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list
