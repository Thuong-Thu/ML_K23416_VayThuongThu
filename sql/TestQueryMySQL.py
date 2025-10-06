import mysql.connector

sever = "localhost"
port=3306
databases= "studentmanagement"
username = "root"
password = "thuvt23406@"

conn = mysql.connector.connect(
    host=sever,
    port=port,
    user=username,
    passwd=password,
    database=databases)

cursor = conn.cursor()

# sql = "select * from student"
# sql = "SELECT * FROM student where Age>=22 and AGe <=26"
# sql = "SELECT * FROM student order by Age asc"
# sql = "SELECT * FROM student where Age>=22 and Age<=26 order by Age desc"
# sql = "SELECT * FROM student where ID = 1"
# sql = "SELECT * FROM student LIMIT 3 OFFSET 3"
# cursor.execute(sql)
#
#
# dataset = cursor.fetchall()
# align = '{0:<3} {1:<6} {2:<15} {3:<10}'
# print(align.format("ID", "Code", "Name", "Age"))
# for item in dataset:
#     id=item[0]
#     code=item[1]
#     name=item[2]
#     age=item[3]
#     avatar=item[4]
#     intro=item[5]
#     print(align.format(id, code, name, age))
#
# cursor.close()
#
# print("PAGING!!!!")
# cursor = conn.cursor()
# sql = "SELECT count(*) FROM student"
# cursor.execute(sql)
# dataset = cursor.fetchone()
# rowcount=dataset[0]
#
# limit = 3
# step = 3
# for offset in range(0, rowcount, step):
#     sql = f"SELECT * FROM student LIMIT {limit} OFFSET {offset}"
#     cursor.execute(sql)
#
#     dataset = cursor.fetchall()
#     align = '{0:<3} {1:<6} {2:<15} {3:<10}'
#     print(align.format("ID", "Code", "Name", "Age"))
#     for item in dataset:
#         id = item[0]
#         code = item[1]
#         name = item[2]
#         age = item[3]
#         avatar = item[4]
#         intro = item[5]
#         print(align.format(id, code, name, age))
#
# cursor.close()

#(3.1) Thêm mới 1 Student
cursor = conn.cursor()

sql="insert into student (code,name,age) values (%s,%s,%s)"

val=("sv07","Trần Duy Thanh",45)

cursor.execute(sql,val)

conn.commit()

print(cursor.rowcount," record inserted")

cursor.close()

#(3.2) Thêm mới nhiều Student:
cursor = conn.cursor()

sql="insert into student (code,name,age) values (%s,%s,%s)"

val=[
    ("sv08","Trần Quyết Chiến",19),
    ("sv09","Hồ Thắng",22),
    ("sv10","Hoàng Hà",25),
     ]

cursor.executemany(sql,val)

conn.commit()

print(cursor.rowcount," record inserted")

cursor.close()

#(4.1) Cập nhật tên Sinh viên có Code=’sv09′ thành tên mới “Hoàng Lão Tà”
cursor = conn.cursor()
sql="update student set name='Hoàng Lão Tà' where Code='sv09'"
cursor.execute(sql)

conn.commit()

print(cursor.rowcount," record(s) affected")

#(4.2) Cập nhật tên Sinh viên có Code=’sv09′ thành tên mới “Hoàng Lão Tà” như viết dạng SQL Injection:
cursor = conn.cursor()
sql="update student set name=%s where Code=%s"
val=('Hoàng Lão Tà','sv09')

cursor.execute(sql,val)

conn.commit()

print(cursor.rowcount," record(s) affected")

# (5.1) Xóa Student có ID=14
conn = mysql.connector.connect(
                host=sever,
                port=port,
                database=databases,
                user=username,
                password=password)
cursor = conn.cursor()
sql="DELETE from student where ID=14"
cursor.execute(sql)

conn.commit()

print(cursor.rowcount," record(s) affected")


#(5.2) Xóa Student có ID=13 với SQL Injection
conn = mysql.connector.connect(
                host=sever,
                port=port,
                database=databases,
                user=username,
                password=password)
cursor = conn.cursor()
sql = "DELETE from student where ID=%s"
val = (13,)

cursor.execute(sql, val)

conn.commit()

print(cursor.rowcount," record(s) affected")