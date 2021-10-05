# 1.导入包

import pandas as pd
import re
import os
import pymysql

# 2：建立连接
conn = pymysql.connect(
    host='localhost',  # mysql服务端的IP，默认127.0.0.1/localhost-或输入真实Ip
    user='root',  # 默认root用户
    password='123456',  # sql密码
    database='imagedata',  # 库名
    port=3306,  # 端口号
    charset='utf8',  # 编码格式
    autocommit='true')

# 3.创建游标对象
cursor = conn.cursor()


# 4.初始化SQL函数
def Initialize_database():
    try:
        cursor.execute('DROP TABLE table_1')
    except:
        print('没有table_1,创建table_1')
    else:
        print('原存在table_1,已被删除并重新创建table_1')
    finally:
        cursor.execute('CREATE TABLE table_1(title LONGTEXT,address VARCHAR(200) '
                       'PRIMARY KEY,information LONGTEXT,classification INT)')


#  5.写入数据函数
def WirTe_toSql(path):
    # 外层遍历
    for root, dirs, files in os.walk(path):
        # 创建dataFrame对象，整体导入mysql
        data = {
            'title': [],
            'address': [],
            'information': [],
            'Tag': []
        }
        data = pd.DataFrame(data)

        # 对pic进行排序，确保title和excel中标签一致对应
        files.sort(key=lambda x: len(x))
        data['title'] = files

        # 内层循环计数初始化
        a = 0

        # 内层文件遍历
        for file in files:
            filename = os.path.join(root, file)
            filename = filename.replace('\\', "\\\\")
            # 正则表达式获取文件后缀，判断是jpg还是xlsx
            suffix = (re.search(".([a-z|A-Z]*?)$", filename).group(1))

            if suffix == 'jpg':
                data.loc[a, 'address'] = filename
                a = a + 1
            else:
                data_excel = pd.read_excel(filename)

                #  文本信息提取
                data['information'] = data_excel['figure related information']
                # 替换information中的'，避免与mysql语句发生冲突

                # 将information中的float转换成str，只有str才能使用replace函数
                data['information'] = data['information'].astype(str)
                # 对information中每一个元素进行replace
                data['information'] = data['information'].map(lambda x: x.replace("'", " \" "))

                # 标签
                data['Tag'] = data_excel['figure classification']

        # 如果data为空，不进行删除最后一项操作
        if len(data.title):
            data.drop(len(data.title) - 1, axis=0, inplace=True)

        for i in data.index:
            data_ = data.loc[i, :]
            sql_insert = """INSERT INTO table_1(title,address,information, classification) 
                                               VALUES ('%s', '%s', '%s', '%s' )""" % (
                data_.title, data_.address, data_.information, str(data_.Tag))
            try:
                cursor.execute(sql_insert)
                # values = (pymysql.mysql_real_escape_string(data_.title),
                #           pymysql.escape_string(data_.address),
                #           pymysql.escape_string(data_.information),
                #           pymysql.escape_string(data_.Tag))
                # values = (data_.title,data_.address,data_.information,data_.Tag)
                # cursor.execute(sql_insert, value)
            except Exception as e:
                print('错误位置为：', filename)
                print('错误类型为：', e)


# 6：sql查询函数
def search():
    sql_find = "select * from table_1;"
    try:
        # 使用游标对象，调用SQL语句
        cursor.execute(sql_find)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            title = row[0]
            address = row[1]
            information = row[2]
            classification = row[3]
            # 打印结果
            print('-' * 50,
                  "\ntitle：%s\n"
                  "address：%s\n"
                  "information：%s\n"
                  "classification：%s\n" % (title, address, information, classification),
                  '-' * 50, )
    except Exception as e:
        print("Error: unable to fecth data")
        print('错误类型为：', e)


# 7.主函数
if __name__ == '__main__':
    # 文件夹路径
    paths = r"E:\MyData\DataWithImage"
    # 初始化
    Initialize_database()
    # 写入mysql
    WirTe_toSql(paths)
    # 遍历显示数据
    search()

# 8. 关闭游标对象
cursor.close()

# 9.关闭连接
conn.close()
# %%
