import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password= "0842",
    database="testdb2"
    )


with conn.cursor() as answer:
    answer.execute("INSERT INTO tbl_test2 (col_numbers1) VALUES (1);")
    conn.commit()

    answer.execute("SELECT * FROM tbl_test2;")
    result = answer.fetchall()
    for i in result:
        print(i)

print("\n")

with conn.cursor() as answer:
    answer.execute("DELETE FROM tbl_test2 WHERE col_numbers1 = 1;")
    conn.commit()

    answer.execute("SELECT * FROM tbl_test2;")
    result = answer.fetchall()
    for i in result:
        print(i)


conn.close()