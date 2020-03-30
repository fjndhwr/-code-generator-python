import os
import json
import time
import tarfile
from flask import Flask, render_template, send_from_directory, request
import connectDB
db = connectDB.connect_db()
app=Flask(__name__)


@app.route('/index')
def index():
    get_column();
    return render_template('create_class.html')


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
    fields = request.form['fields']
    if len(fields) <= 0:
        msg='request data json is null!'
    print(fields)
    j = json.loads(fields, encoding='utf-8')
    class_name = j['class']
    package = j['package']
    db_type = j['type']
    if len(class_name) <= 0 :
        msg = 'className is null!'
    if len(package) <= 0:
        msg = 'package is null'
    if len(db_type) <= 0:
        msg = 'type is null'
    print(class_name + '\n' + package)
    if not msg or len(msg) <= 0:
        d = time.strftime("%Y-%m-%d", time.localtime())
        entity = request.form.get('entity')
        if entity and len(entity) >= 1:
            print('--- create entity class')
            create_entity(class_name, package, j['table'], j['column'], db_type, d)
        dao = request.form.get('dao')
        if dao and len(dao) >= 1:
            print('--- create dao class')
            create_dao(class_name, package, d)
        service = request.form.get('service')
        if service and len(service) >= 1:
            print('--- create service class')
            create_service(class_name, package, d)
        controller = request.form.get('controller')
        if controller and len(controller) >= 1:
            print('--- create controller class')
            create_controller(class_name, package, d)
            file_name = make_targz()
    return render_template('create_class.html', msg=msg, file_name=file_name)


# 创建entity
def create_entity(class_name, package, table_name, columns, db_type, date):
    propertys = ''
    if columns:
        for key in columns.keys():
            propertys += 'private %s %s;' % (columns[key], key) + '\n\n'
    c = {'package': package + '.entity',
         'entity_package': package + '.entity.' + class_name,
         'class_name': class_name,
         'table_name': table_name,
         'propertys': propertys,
         'date': date}
    if db_type == 'mongodb':
        s = render_template('entity_mongodb_templates.html', **c)
        create_java_file(class_name, package + '.entity', s)
    elif db_type == 'mysql':
        s = render_template('entity_mysql_templates.html', **c)
        create_java_file(class_name, package + '.entity', s)
        s = render_template('entity_mysql_mapper_templates.html', **c)
        create_java_file(class_name, package + '.entity', s, 'Mapper.xml')


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
    dirs = 'D:/temp/python/'+package.replace('.', '/')+'/'
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


def get_column():
    cursor = db.cursor()
    sql = """SHOW COLUMNS FROM address"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row[0])
    except:
        print("Error: unable to fecth data")
        # Rollback in case there is any error
        #db.rollback()


if __name__ == '__main__':
    app.run()