import re
# 业务逻辑
import os
import pymysql
import urllib.parse

URL_FUN_LIST = {}


#
# def route(data):
#     def fun_out(fun):
#         URL_FUN_LIST[data] = fun
#
#         def fun_in():  #  这里有意思的是没有被最后执行
#             pass
#
#         return fun_in
#
#     return fun_out

def route(data):
    def fun_out(fun):
        URL_FUN_LIST[data] = fun

    return fun_out

database_name = "192.168.162.135"

@route(r'/index.html')  # index = fun_out(index)  fun_in
def index(ret):
    with open('./templates/index.html', 'r+') as f:
        content = f.read()

    # 连接数据库
    conn = pymysql.connect(
        host=database_name,
        port=3306,
        user="root",
        password="mysql",
        database="stock_db_2",
        charset="utf8"
    )
    cs = conn.cursor()
    cs.execute('select * from info')
    content_lists = cs.fetchall()
    cs.close()
    conn.close()
    html = """<tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s"></td>
                </tr>"""
    my_stock = ""
    for i in content_lists:

        my_stock += html % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[1])
    content = re.sub(r'{%content%}', my_stock, content)
    return content

@route(r'/add/(\d+)\.html')
def add_fun(ret):

    stock_code = ret.group(1)

    db = pymysql.connect(
        host=database_name, 
        port=3306, 
        user='root', 
        password='mysql', 
        database='stock_db_2',
        charset='utf8')

    cs = db.cursor()

    # 查看该股票是否关注过
    sql_str = 'select * from focus where id = ( select id from info where code = %s)'
    cs.execute(sql_str,[stock_code])
    stock_info = cs.fetchone()
    if stock_info:
        cs.close()
        db.close()
        return '此股票关注过了'
    
    sql_str = """insert into focus(id) (select id from info where code = %s) """
    cs.execute(sql_str,[stock_code])

    db.commit()

    cs.close()
    db.close()

    return '请求成功' + stock_code


@route(r'/center.html')
def center(ret):
    with open('./templates/center.html', 'r+') as f:
        content = f.read()
    conn = pymysql.connect(
        host=database_name,
        port=3306,
        user="root",
        password="mysql",
        database="stock_db_2",
        charset="utf8"
    )
    cs = conn.cursor()
    sql_str = """select * from info inner join focus on info.id = focus.id;"""
    cs.execute(sql_str)
    content_list = cs.fetchall()
    cs.close()
    conn.close()
    html = """<tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>
                        <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                    </td>
                    <td>
                        <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                    </td>
                </tr>"""

    my_stock = ""
    for i in content_list:
        my_stock += html % (i[1], i[2], i[3], i[4], i[5], i[6], i[9], i[1], i[1])

    content = re.sub(r'{%content%}', my_stock, content)

    return content
# "/del/" + code + ".html"
@route(r'/del/(\d+)\.html')
def del_fun(ret):

    stock_code = ret.group(1)
    db = pymysql.connect(
        host=database_name,
        port=3306,
        user="root",
        password="mysql",
        database="stock_db_2",
        charset="utf8"
    )
    cs = db.cursor()

    sql_str = """delete from focus where id = (select id from info where code = %s)"""

    cs.execute(sql_str,[stock_code])

    db.commit()
    cs.close()
    db.close()

    return '删除成功'

@route(r'/update/(\d+)\.html')
def update_fun(ret):

    stock_code = ret.group(1)
    db = pymysql.connect(
        host=database_name,
        port=3306,
        user="root",
        password="mysql",
        database="stock_db_2",
        charset="utf8"
    )
    cs = db.cursor()

    sql_str = """select note_info from focus where id = (select id from info where code = %s)"""

    cs.execute(sql_str,[stock_code])
    note_info = cs.fetchone()
    with open('./templates/update.html', 'r+') as f:

        content = f.read()

    content = re.sub(r"{%note_info%}",note_info[0],content)
    content = re.sub(r"{%code%}",stock_code,content)

    cs.close()
    db.close()

    return content
# /update/{%code%}/" + item + ".html
@route(r'/update/(\d+)/(.*)\.html')
def modify_fun(ret):

    stock_code = ret.group(1)
    stock_new_info = ret.group(2)
    # 使用模块进行url编码的解码
    # 
    stock_new_info = urllib.parse.unquote(stock_new_info)
    db = pymysql.connect(
        host=database_name,
        port=3306,
        user="root",
        password="mysql",
        database="stock_db_2",
        charset="utf8"
    )
    cs = db.cursor()

    sql_str = 'update focus set note_info= %s where id = (select id from info where code = %s)'

    cs.execute(sql_str,[stock_new_info, stock_code])

    db.commit()

    cs.close()
    db.close()
    return '修改成功'
# URL_FUN_LIST['index.py'] = index
# URL_FUN_LIST['center.py'] = center


# 接口
# def application(file_name):
#     file_name = file_name[1:]
#     if file_name == "index.py":
#
#         return index()
#
#     elif file_name == "center.py":
#
#         return center()
#
#     elif file_name == "login.py":
#
#         return login()
#     else:
#         return "dynamic2 is not found"

# 遵循wsgi 协议

def application(environ, start_response):
    file_name = environ['PATH-INFO']

    print(file_name)


    try:
        for key,values in URL_FUN_LIST.items():
            # r'/index.html'==> '/index.html'
            # r'/add/(\d+)\.html' ==> '/add/0007.html'
            ret = re.match(key,file_name)  # 获取匹配中的路径中的第一组或者整体
            print(ret)
            if ret:
                start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8'), ("Server", "zag-miniWeb")])
                # 执行对应的函数 并传入分组内容 并返回函数的执行结果
                return values(ret)
        else:
            start_response('404 Not Found', [('Content-Type', 'text/html;charset=utf-8'), ("Server", "zag-miniWeb")])
            return '404...'

    except Exception as e:
        print(e)
        return '异常异常'
        






