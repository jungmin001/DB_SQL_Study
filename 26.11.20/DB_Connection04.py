import pymysql

def connection_server():
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="0842",
            database="testdb4")
    except:
        print("Log : DB connection fail!")
        return;
    else:
        print("Log : DB connection complete!")

    databases = query_command(conn, "SHOW DATABASES;")
    for i, db in enumerate(databases, start=1):
        print(f"{i}. {db[0]}")

    return conn

def query_command(conn, command, is_method = None):
    """
    conn : DB 연결 객체
    command : SQL 쿼리문
    is_method : 반환값 
    > None : 자동
    > True : fetchall | tuple 
    > False : 반환 없이 commit
    """

    if is_method is None:
        is_method = "SELECT" in command or "SHOW" in command

    with conn.cursor() as cur:
        cur.execute(command)

        if is_method:
            return cur.fetchall()
    
    conn.commit()
    print("Log : complete commit!")


def main():
    try:
        conn = connection_server()
        if conn is None: return;

        print(query_command(conn, "SHOW TABLES;"))

        query_command(
            conn,
            "ALTER TABLE tbl_test4 "
            "ADD COLUMN IF NOT EXISTS current_value INT, "
            "ADD COLUMN IF NOT EXISTS current_state VARCHAR(10);"
        )
        
        query_command(conn, "INSERT INTO tbl_test4(current_value, current_state) VALUES (1, 'Normal'), (2, 'Warning'), (3, 'Error');")

        for row in query_command(conn, "SELECT * FROM tbl_test4;"):
            print(row)
        del row

        query_command(conn, "DELETE FROM tbl_test4 WHERE current_state IN ('Normal', 'Warning');")

        print("\n")

        for row in query_command(conn, "SELECT * FROM tbl_test4;"):
            print(row)

    except:
        print("Log : Eerror!")

    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()