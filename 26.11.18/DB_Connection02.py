
import pymysql
from getpass import getpass

# DB 연결 변수 선언 및 초기화
conn = None

def Connection_Server():
    global conn # 전역변수 설정

    # pymysql.connect() = 서버 연결을 위한 함수
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=getpass("DB 비밀번호: "),
    )

    print("서버 연결 실패" if conn is None else "서버 연결 성공")

# DB 선택
def Select_DB():
    global conn

    databases = Query_Commend("SHOW DATABASES;")
    
    print("\n=== DB 목록 ===")

    for i, db in enumerate(databases, start=1):
        print(f"{i}. {db[0]}")

    while True:
        choice = int(input("\nDB 번호 선택: "))

        if 1 <= choice <= len(databases):
            break

    db_name = databases[choice - 1][0]
    conn.select_db(db_name)

# DB 닫기
def Close_DB():
    if conn is not None:
        conn.close()

# 테이블 확인
def Open_Table():
    tables = Query_Commend("SHOW TABLES;")

    print("\n === 테이블 목록 ===")

    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table[0]}")

    while True:
        tbl_choice = int(input("\n 테이블 번호 선택: "))
        if 1 <= tbl_choice <= len(tables):
               break

    table_name = tables[tbl_choice - 1][0]

    Query_Commend(f"SELECT * FROM {table_name};")

# 쿼리문 입력 조회 함수
def Query_Commend(Commend, Method = None):
    if Method is None:
        if  "SELECT" in Commend or "SHOW" in Commend:
            Method = True
        else:
            Method = False

    with conn.cursor() as cursor:
        cursor.execute(Commend)
        answer = cursor.fetchall()

        if type(answer) == tuple or type(answer) == list and Method:
            for i in answer:
                print(i)
            return answer
        elif type(answer) == str or Method == False:
            conn.commit()
            print("커밋 완료")



def Main():
    # 서버 연결
    Connection_Server()

    # DB 조회
    Query_Commend("SHOW DATABASES;")
    Select_DB()

    # Table 조회
    Query_Commend("SHOW TABLES;")
    Open_Table()

    # 쿼리 명령어
    Query_Commend("SELECT col_timestemp FROM tbl_test2;") # timestemp 컬럼 출력
    Query_Commend("ALTER TABLE tbl_test2 ADD COLUMN IF NOT EXISTS col_PythonTestCol VARCHAR(10);") # 테스트 컬럼 추가
    Query_Commend("ALTER TABLE tbl_test2 DROP COLUMN IF EXISTS col_PythonTestCol;") # 테스트 컬럼 삭제

    # DB 종료
    Close_DB()

Main()