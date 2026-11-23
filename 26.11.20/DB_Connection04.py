import pymysql


#  pymysql.connect를 통한 DB 연결 수행
#  연결 성공 및 실패 시 로그 출력
#  연결 객체 반환
def connection_server():
    try:
        conn = pymysql.connect(
            host="127.0.0.1",                   # IP 주소
            port=3306,                          # 포트 번호
            user="root",                        # 사용자
            password="0842",                    # 비밀번호
            database="testdb4",                 # 데이터 베이스
        )  
    except:
        print("\033[91mLog : DB connection fail!\033[0m")      # 연결 실패 시 로그, 리턴으로 함수 종료
        return None
    else:
        print("\033[92mLog : DB connection complete!\033[0m")  # 성공 시 로그

    return conn  # 연결 객체 반환


# SELECT / SHOW 쿼리 자동 판별 및 실행
# fetchall() 결과를 통한 데이터 반환
# INSERT / DELETE 등 변경 쿼리문 commit 처리
def query_command(conn, command, is_method=None):

    # is_method = None일 시 command안 쿼리문에 SELECT, SHOW가 있는지 확인 후 있다면 True, 없다면 False를 반환
    if is_method is None:
        is_method = "SELECT" in command or "SHOW" in command

    with conn.cursor() as cur:
        cur.execute(command)

        if is_method:               # is_method = True라면 fetchall 을 반환
            return cur.fetchall()

    conn.commit()                   # is_method = False라면 커밋 후 로그 출력
    print("\033[92mLog : complete commit!\033[0m")


def main():
    try:
        conn = connection_server()  # 연결 객체 대입
        if conn is None:
            return                  # 연결 객체 유무에 대한 방어코드


        # current_value, current_state 컬럼 추가
        print("\n==== ADD COLUMN ====")
        query_command(              
            conn,
            "ALTER TABLE tbl_test4 "
            "ADD COLUMN IF NOT EXISTS current_value INT, "
            "ADD COLUMN IF NOT EXISTS current_state CHAR(10);",
        )

        # 추가 한 컬럼 초기화
        print("\n==== INSERT ====")
        query_command(conn, """INSERT INTO tbl_test4(
                    current_value, 
                    current_state) 
                    VALUES 
                    (1, 'Normal'), 
                    (2, 'Warning'), 
                    (3, 'Error');""")


        # 기존 컬럼 col_numbers1~9 1~9값으로 업데이트
        print("\n==== UPDATE ====")
        update_value = ", ".join(f"col_numbers{i} = {i}" for i in range(1, 10)) # str 형태로 col_numbers1...9 까지 생성
        query_command(conn, f"UPDATE tbl_test4 SET {update_value};")            # UPDATE 실행
        for row in query_command(conn, "SELECT * FROM tbl_test4;"):             # UPDATE 결과 확인
            print(row)
        del row
        
        print("\n==== DELETE ====")
        query_command(conn, "DELETE FROM tbl_test4 WHERE current_state IN ('Normal', 'Warning');") # current_state == Error를 제외한 행 제거
        for row in query_command(conn, "SELECT * FROM tbl_test4;"):                                # DELETE결과 확인
            print(row)
        del row

    except:
        print("\033[91mLog : Main Function Error!\033[0m")

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
