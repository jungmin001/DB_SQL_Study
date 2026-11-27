import socket
import pymysql
import os


# TCP 연결 정보
#HOST = "192.168.219.48"
HOST = "127.0.0.1"
PORT = 1234


# DB 연결 함수
def connection_server():

    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="0842",
            database="testdb4"
        )

        print("DB 연결 성공!")
        return conn

    except Exception as e:
        print(f"DB 연결 실패 : {e}")
        return None


# SQL 쿼리 실행 함수
def query_command(conn, command, is_method=None, params=None):

    # SELECT / SHOW 쿼리 자동 판별
    if is_method is None:
        is_method = command.strip().upper().startswith(
            ("SELECT", "SHOW")
        )

    with conn.cursor() as cur:

        # SQL 쿼리 실행
        cur.execute(command, params)

        # 조회 결과 반환
        if is_method:
            return cur.fetchall()

    # 변경 쿼리 Commit
    conn.commit()


# 테이블 생성 함수
def create_table(conn):

    query_command(conn, """
        CREATE TABLE IF NOT EXISTS tbl_test5(
            id INT AUTO_INCREMENT PRIMARY KEY,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            col_sensor01 INT,
            col_sensor02 INT,
            col_sensor03 INT
        );
    """)

    print("테이블 준비 완료!")


# 센서 데이터 DB 저장 함수
def insert_sensor(conn, sensor01, sensor02, sensor03):

    query_command(
        conn,
        """
        INSERT INTO tbl_test5(
            col_sensor01,
            col_sensor02,
            col_sensor03
        )
        VALUES (%s, %s, %s);
        """,
        params=(sensor01, sensor02, sensor03)
    )


# 전체 데이터셋 출력 함수
def print_dataset(conn):

    # 전체 데이터 조회
    dataset = query_command(
        conn,
        "SELECT * FROM tbl_test5 ORDER BY id;"
    )

    # 터미널 화면 초기화
    os.system("cls" if os.name == "nt" else "clear")

    # 연결 상태 출력
    print("==== Real-Time Sensor Dataset ====")
    print(f"TCP Server : {HOST}:{PORT}")
    print("Database   : testdb4")
    print("Table      : tbl_test5")
    print(f"Total Rows : {len(dataset)}")

    print("-" * 76)

    # 컬럼명 출력
    print(
        f"{'ID':<8}"
        f"{'Time':<24}"
        f"{'Sensor01':<12}"
        f"{'Sensor02':<12}"
        f"{'Sensor03':<12}"
    )

    print("-" * 76)

    # 전체 데이터셋 출력
    for row in dataset:

        print(
            f"{row[0]:<8}"
            f"{str(row[1]):<24}"
            f"{row[2]:<12}"
            f"{row[3]:<12}"
            f"{row[4]:<12}"
        )

    print("-" * 76)


# TCP 데이터 수신 함수
def receive_sensor(conn):

    client = None

    try:

        # TCP 소켓 생성
        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        # 연결 제한 시간 설정
        client.settimeout(5.0)

        print(f"TCP 연결 시도 : {HOST}:{PORT}")

        # 서버 연결
        client.connect((HOST, PORT))

        print("TCP 연결 성공!")

        # 수신 시간 제한 해제
        client.settimeout(None)

        # 줄바꿈 단위 데이터 수신
        with client.makefile("r", encoding="utf-8") as stream:

            for line in stream:

                # 줄바꿈 제거
                text = line.strip()

                if text == "종료":
                    break

                try:

                    # 센서 데이터 분리 및 정수 변환
                    sensor01, sensor02, sensor03 = map(
                        int, text.split(",")
                    )

                except ValueError as e:

                    print(f"데이터 변환 실패 : {e}")
                    continue

                # DB에 센서 데이터 저장
                insert_sensor(
                    conn,
                    sensor01,
                    sensor02,
                    sensor03
                )

                # 전체 데이터셋 갱신
                print_dataset(conn)

                # 최근 수신 데이터 출력
                print(f"최근 수신 : {text}")
                print("DB 저장 완료!")

        print("서버 연결 종료")

    except socket.timeout:
        print("TCP 연결 시간 초과")

    except ConnectionRefusedError:
        print("TCP 연결 거부")

    except Exception as e:
        print(f"TCP 또는 DB Error : {e}")

    finally:

        if client is not None:
            client.close()

        print("TCP 연결 종료")


# 메인 함수
def main():

    conn = None

    try:

        # DB 연결
        print("\n==== DB Connecting ====")

        conn = connection_server()

        if conn is None:
            return

        # 테이블 생성
        print("\n==== CREATE TABLE ====")

        create_table(conn)

        # TCP 연결 및 데이터 수신
        print("\n==== TCP Connecting ====")

        receive_sensor(conn)

    except KeyboardInterrupt:

        print("\n프로그램 종료 요청")

    except Exception as e:

        print(f"Main Function Error : {e}")

    finally:

        if conn is not None:

            conn.close()

            print("\n==== Shutdown ====")
            print("DB 연결 종료")


if __name__ == "__main__":
    main()