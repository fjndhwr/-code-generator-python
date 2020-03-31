import os
import json
import time
import tarfile
import traceback
from flask import Flask, render_template, send_from_directory, request
import connectDB
import discern_type

db = connectDB.connect_db()
app = Flask(__name__)
cursor = db.cursor()
table_list = connectDB.get_table_list_map()


@app.route('/index')
def index():
    return render_template('create_class.html', **table_list)


@app.route("/download/<filename>", methods=['GET'])
def downloader(filename):
    # 指定文件下载目录，默认为当前项目根路径
    dirpath = os.path.join(app.root_path, '')
    # as_attachment=True 表示下载
    return send_from_directory(dirpath, filename, as_attachment=True)


@app.route('/createClass', methods=['GET', 'POST'])
def create_class():
    file_name = msg = None
    # {'column': {'age': 'int', 'id': 'String', 'address': 'String', 'name': 'String'}, 'table': 'cc_user'}
    table = request.form['table']
    if len(table) <= 0:
        msg = 'request data json is null!'
    column = get_column(table)
    package = "com.hwr." + table  # 包名
    db_type = '1'
    if len(table) <= 0:
        msg = 'className is null!'
    if len(package) <= 0:
        msg = 'package is null'
    if len(db_type) <= 0:
        msg = 'type is null'
    print(table + '\n' + package)
    if not msg or len(msg) <= 0:
        d = time.strftime("%Y-%m-%d", time.localtime())
        entity = request.form.get('entity')
        if entity and len(entity) >= 1:
            print('--- create entity class')
            create_entity(table, package, column, d)
        dao = request.form.get('dao')
        if dao and len(dao) >= 1:
            print('--- create dao class')
            create_dao(table, package, d)
        service = request.form.get('service')
        if service and len(service) >= 1:
            print('--- create service class')
            create_service(table, package, d)
        controller = request.form.get('controller')
        if controller and len(controller) >= 1:
            print('--- create controller class')
            create_controller(table, package, d)
        file_name = make_targz()
    return render_template('create_class.html', msg=msg, file_name=file_name, **table_list)


# 创建entity
def create_entity(class_name, package, columns, date):
    propertys = ''
    if columns:
        for key in columns.keys():
            propertys += '/** \n *' + columns[key][1] + ' \n */ \n'
            propertys += 'private %s %s;' % (columns[key][0], key) + '\n\n'
    c = {'package': package + '.entity',
         'entity_package': package + '.entity.' + class_name,
         'class_name': class_name,
         'propertys': propertys,
         'date': date}
    s = render_template('entity_mongodb_templates.html', **c)
    create_java_file(class_name, package + '.entity', s)


# 创建Dao
def create_dao(class_name, package, date):
    c = {'package': package + '.dao',
         'class_name': class_name,
         'entity_package': package + '.entity.' + class_name,
         'date': date}
    s = render_template('dao_templates.html', **c)
    create_java_file(class_name + 'Dao', package + '.dao', s)


# 创建Service
def create_service(class_name, package, date):
    c = {'package': package + '.service',
         'class_name': class_name,
         'small_class_name': small_str(class_name),
         'entity_package': package + '.entity.' + class_name,
         'dao_package': package + '.dao.' + class_name + 'Dao',
         'date': date}
    s = render_template('service_templates.html', **c)
    create_java_file(class_name + 'Service', package + '.service', s)


# 创建controller
def create_controller(class_name, package, date):
    c = {'package': package + '.entity',
         'class_name': class_name,
         'small_class_name': small_str(class_name),
         'entity_package': package + '.entity.' + class_name,
         'dao_package': package + '.dao.' + class_name + 'Dao',
         'service_package': package + '.dao.' + class_name + 'Service',
         'date': date}
    s = render_template('controller_templates.html', **c)
    # print(s)
    create_java_file(class_name + 'Controller', package + '.controller', s)


# 将首字母转换为小写
def small_str(s):
    if len(s) <= 1:
        return s
    return (s[0:1]).lower() + s[1:]


# 创建java文件
def create_java_file(class_name, package, text, suffix='.java'):
    dirs = 'D:/temp/python/' + package.replace('.', '/') + '/'
    if not os.path.exists(dirs):
        os.makedirs(dirs, 0o777)
    fd = os.open(dirs + class_name + suffix, os.O_WRONLY | os.O_CREAT)
    os.write(fd, text.encode(encoding="utf-8", errors="strict"))
    os.close(fd)


def make_targz():
    file_name = 'com.tar.gz'
    source_dir = 'D:/temp/python/'
    with tarfile.open(file_name, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return file_name


def get_column(table_name):
    date = time.strftime("%Y-%m-%d", time.localtime())  # 时间
    columus = {}  # 列

    sql = """SELECT
                COLUMN_NAME,
                DATA_TYPE,
                COLUMN_COMMENT 
            FROM
                information_schema.COLUMNS 
            WHERE
                TABLE_SCHEMA = """ + "'" + connectDB.date_name + "' " + """AND TABLE_NAME = """ + "'" + table_name + "'"
    try:
        # 执行sql语句获取队列类型及备注
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            tuple = (discern_type.discern_type(row[1]), row[2])
            columus[row[0]] = tuple
        return columus
        # create_entity(table_name, package, columus, date)
    except Exception:
        print('traceback.format_exc():\n%s' % traceback.format_exc())


if __name__ == '__main__':
    app.run()
