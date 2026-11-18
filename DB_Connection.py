
import pymysql
from getpass import getpass

# DB 연결 변수 선언 및 초기화
conn = None


try:
    # pymysql.connect() = DB 연결을 위한 함수
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=getpass("DB 비밀번호: "),
        database="testdb3"
    )
    print("conn 변수에 담긴 내용:", conn)

    print("DB 연결 성공!")

    # DB 연결 후 현재 DB 확인
    with conn.cursor() as cursor:
        cursor.execute("SELECT DATABASE();") # 현재 연결된 DB 확인
        print("현재 DB:", cursor.fetchone()) # 현재 DB 출력 / 튜플형태로 반환됨

    print(conn.open())

# DB 연결 실패 시 예외 처리
except pymysql.MySQLError as e:
    print("DB 연결 실패:", e)

# DB 연결 종료
finally:
    if conn is not None:
        conn.close()
