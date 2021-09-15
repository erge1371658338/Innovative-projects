import os
import pymysql

db = pymysql.connect(host='localhost',
                             user='root',
                             password='0221',
                             database='imagedata',
                             autocommit='true')
cursor = db.cursor()
path ='D:\\study\\project\\DataWithImage'
def get_filelist(path):
    # Filelist = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            # 文件名列表，包含完整路径
            if os.path.isfile(os.path.join(root, filename)):
               title=root.strip(path)
               address=os.path.join(root, filename)
               # print(title)
               # print(address)
               # 文件名列表，只包含文件名
               # Filelist.append(filename)

               sql_insert= """INSERT INTO table_1(title,address,information, classification)
               VALUES ('%s', '%s', '%s', '%d' )""" % (title, address, pymysql.NULL, 0)
               cursor.execute(sql_insert)
# sql_insert = """INSERT INTO table_1(title,
#          address, information, classification)
#          VALUES ('467-hong1976', 'D:\\study\\project\\DataWithImage\\467-hong1976\\pic1.jpg','info', '3')"""


get_filelist(path) 

sql_find="SELECT * FROM table_1"
try:
   # 执行SQL语句
   cursor.execute(sql_find)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      title = row[0]
      address = row[1]
      information = row[2]
      classification = row[3]
       # 打印结果
      # print ("title=%s,address=%s,information=%s,classification=%d" %(title, address, information, classification))
except:
   print ("Error: unable to fecth data")
# %%
