import pymysql


#  pymysql.connect를 통한 DB 연결 수행
#  연결 성공 및 실패 시 로그 출력
#  SHOW DATABASES 목록 출력 후 커넥션 반환
def connection_server():
    try:
        conn = pymysql.connect(
            host="127.0.0.1",  # IP 주소
            port=3306,  # 포트 번호
            user="root",  # 사용자
            password="0842",  # 비밀번호
            database="testdb4",
        )  # 데이터 베이스
    except:
        print("Log : DB connection fail!")  # 연결 실패 시 로그, 리턴으로 함수 종료
        return
    else:
        print("Log : DB connection complete!")  # 성공 시 로그

    databases = query_command(
        conn, "SHOW DATABASES;"
    )  # 쿼리문으로 데이터 베이스 목룍 변수에 대입
    for i, db in enumerate(databases, start=1):  # 데이터 베이스 목록 출력
        print(f"{i}. {db[0]}")

    return conn  # 커넥션 주소? 반환


# SELECT / SHOW 쿼리 자동 판별 및 실행
# fetchall() 결과를 통한 데이터 반환
# INSERT / DELETE 등 변경 쿼리 commit 처리
def query_command(conn, command, is_method=None):

    # is_method = None일 시 command안 쿼리문에 SELECT, SHOW가 있는지 확인 후 있다면 True, 없다면 False를 반환
    if is_method is None:
        is_method = "SELECT" in command or "SHOW" in command

    with conn.cursor() as cur:
        cur.execute(command)

        # is_method = True라면 fetchall 을 반환
        if is_method:
            return cur.fetchall()

    # is_method = False라면 커밋 후 로그 출력
    conn.commit()
    print("Log : complete commit!")


def main():
    try:
        conn = connection_server()  # 커넥션 주소 대입
        if conn is None:
            return
            # 커넥션 주소 유무에 대한 방어코드

        print(query_command(conn, "SHOW TABLES;"))  # 테이블 목록 프린트

        # 현재 값, 상태 컬럼 추가
        query_command(
            conn,
            "ALTER TABLE tbl_test4 "
            "ADD COLUMN IF NOT EXISTS current_value INT, "
            "ADD COLUMN IF NOT EXISTS current_state VARCHAR(10);",
        )

        # 추가 한 컬럼 초기화
        query_command(
            conn,
            "INSERT INTO tbl_test4(current_value, current_state) VALUES (1, 'Normal'), (2, 'Warning'), (3, 'Error');",
        )

        # 컬럼 명 프린트
        for row in query_command(conn, "SELECT * FROM tbl_test4;"):
            print(row)
        del row

        #
        query_command(
            conn, "DELETE FROM tbl_test4 WHERE current_state IN ('Normal', 'Warning');"
        )

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
