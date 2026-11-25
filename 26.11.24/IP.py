import socket

HOST = "127.0.0.1"
PORT = 3306

# TCP 소켓 생성
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 연결 대기 시간 설정 (3초)
client.settimeout(3)

# 서버 연결 시도
result = client.connect_ex((HOST, PORT))

if result == 0:
    print("서버 연결 성공!")
else:
    print("서버 연결 실패!")

# 소켓 종료
client.close()