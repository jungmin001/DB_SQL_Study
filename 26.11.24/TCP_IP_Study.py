# -*- coding: utf-8 -*-
"""
TCP/IP 스터디 (2026-11-24)

목차
  1. 계층 구조: OSI 7계층 vs TCP/IP 4계층
  2. IP 주소와 서브넷 (ipaddress 모듈)
  3. TCP 특징: 연결 지향, 3-way handshake, 4-way 종료
  4. TCP 소켓 실습: 에코 서버 / 클라이언트
  5. UDP 소켓 실습: 비연결형
  6. TCP vs UDP 비교
  7. 연습 문제

실행: python3 TCP_IP.py
"""

import ipaddress
import socket


# ---------------------------------------------------------------------------
# 1. 계층 구조
# ---------------------------------------------------------------------------
# OSI 7계층            TCP/IP 4계층           대표 프로토콜 / 데이터 단위
# ------------------   --------------------   ---------------------------
# 7. 응용 (Application)  \
# 6. 표현 (Presentation)  > 응용 계층          HTTP, FTP, SMTP, DNS  / 메시지
# 5. 세션 (Session)      /
# 4. 전송 (Transport)    전송 계층            TCP, UDP              / 세그먼트
# 3. 네트워크 (Network)  인터넷 계층          IP, ICMP              / 패킷
# 2. 데이터링크 (Data Link) 네트워크 접근 계층 Ethernet, Wi-Fi        / 프레임
# 1. 물리 (Physical)     (네트워크 접근 계층)


# ---------------------------------------------------------------------------
# 2. IP 주소와 서브넷
# ---------------------------------------------------------------------------
print("=== [2] IP / 서브넷 ===")
net = ipaddress.ip_network("192.168.10.0/24")
print("네트워크 주소 :", net.network_address)      # 192.168.10.0
print("브로드캐스트  :", net.broadcast_address)    # 192.168.10.255
print("호스트 수     :", net.num_addresses - 2)    # 네트워크/브로드캐스트 제외 -> 254
print("서브넷 마스크 :", net.netmask)              # 255.255.255.0

addr = ipaddress.ip_address("192.168.10.37")
print("192.168.10.37 이 이 네트워크에 속하나?", addr in net)

# 같은 네트워크인지 판단 = 라우팅 여부 판단의 기본
other = ipaddress.ip_address("192.168.20.5")
print("192.168.20.5 는 같은 네트워크?", other in net)  # False -> 게이트웨이 경유
print()


# ---------------------------------------------------------------------------
# 3. TCP 특징 (주석으로 정리)
# ---------------------------------------------------------------------------
# - 연결 지향(connection-oriented): 데이터 전송 전에 연결을 먼저 수립
# - 신뢰성: 순서 보장, 재전송, 중복 제거, 흐름 제어(수신 윈도우), 혼잡 제어
#
# [3-way handshake] 연결 수립
#   Client --SYN(seq=x)------------->  Server
#   Client <-SYN+ACK(seq=y, ack=x+1)-  Server
#   Client --ACK(ack=y+1)----------->  Server
#   -> 이후 데이터 전송 시작
#
# [4-way handshake] 연결 종료
#   A --FIN------------>  B
#   A <-----------ACK--  B   (B는 아직 보낼 데이터가 남아 있을 수 있음)
#   A <-----------FIN--  B
#   A --ACK------------>  B
#
# TCP 상태: LISTEN, SYN_SENT, SYN_RECEIVED, ESTABLISHED, FIN_WAIT, TIME_WAIT 등
# 확인 명령: macOS/Linux 에서 `netstat -an | grep -i tcp`


# ---------------------------------------------------------------------------
# 4. TCP 소켓 실습: 에코 서버 / 클라이언트
# ---------------------------------------------------------------------------
# 한 스레드에서 서버/클라이언트 역할을 순서대로 수행한다.
# (listen 큐 덕분에 connect() 는 accept() 호출 전에도 3-way handshake 가 끝난다)
print("=== [4] TCP 에코 실습 ===")
# 포트 0 -> OS가 빈 포트를 골라 준다 (포트 충돌 방지)
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(("127.0.0.1", 0))
server_sock.listen(1)                        # LISTEN 상태 진입
host, port = server_sock.getsockname()
print(f"[server] {host}:{port} 에서 대기")

client = socket.create_connection((host, port))   # connect() = 3-way handshake
conn, peer = server_sock.accept()                 # 3-way handshake 가 끝나면 반환
print("[server] 연결됨:", peer)
print("[client] 연결 성공 (ESTABLISHED)")

for msg in ["안녕", "TCP 스터디", "bye"]:
    # client -> server
    client.sendall(msg.encode("utf-8"))
    # server: 받아서 그대로 돌려준다
    data = conn.recv(1024)                   # 바이트 스트림 -> 메시지 경계는 없음
    print("[server] 받음:", data.decode("utf-8"))
    conn.sendall(data)                       # 전부 보낼 때까지 보장
    # client: 에코 응답 수신
    reply = client.recv(1024).decode("utf-8")
    print("[client] 에코 응답:", reply)

client.close()                               # client FIN 전송
if not conn.recv(1024):                      # 빈 바이트 = 상대가 연결 종료(FIN)
    print("[server] 클라이언트 FIN 수신")
conn.close()
server_sock.close()
print()


# ---------------------------------------------------------------------------
# 5. UDP 소켓 실습: 비연결형 (핸드셰이크 없음, 순서/재전송 보장 없음)
# ---------------------------------------------------------------------------
print("=== [5] UDP 실습 ===")
receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(("127.0.0.1", 0))
addr = receiver.getsockname()

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# connect 없이 바로 전송 가능 (연결 수립 과정이 없다)
sender.sendto("UDP 메시지".encode("utf-8"), addr)

data, peer = receiver.recvfrom(1024)         # 메시지 단위로 수신 (경계 보존)
print("[receiver] 받음:", data.decode("utf-8"), "from", peer)

sender.close()
receiver.close()
print()


# ---------------------------------------------------------------------------
# 6. TCP vs UDP 비교
# ---------------------------------------------------------------------------
# 항목          TCP                          UDP
# -----------   --------------------------   -------------------------
# 연결          연결 지향 (handshake)        비연결
# 신뢰성        보장 (재전송, 순서)          보장 안 함
# 전송 단위     바이트 스트림                데이터그램 (메시지 경계 보존)
# 속도/오버헤드 상대적으로 느림, 헤더 큼    빠름, 헤더 작음 (8바이트)
# 용도          HTTP/HTTPS, SSH, DB, 파일   DNS, 스트리밍, 게임, QUIC 기반 통신


# ---------------------------------------------------------------------------
# 7. 연습 문제
# ---------------------------------------------------------------------------
# Q1. 192.168.1.0/26 의 호스트 수, 브로드캐스트 주소는?
#     -> ipaddress.ip_network("192.168.1.0/26") 로 확인해 보기
# Q2. TCP 에코 서버를 여러 클라이언트가 동시에 쓰려면 어떻게 바꿔야 할까?
#     -> 스레드 또는 select/asyncio 사용
# Q3. 3-way handshake 에서 ACK 가 유실되면 무슨 일이 생길까?
#     -> 서버는 SYN_RECEIVED 상태에서 재전송/타임아웃을 기다린다
# Q4. TIME_WAIT 상태가 존재하는 이유는?
#     -> 마지막 ACK 유실 대비 + 지연된 이전 세그먼트가 새 연결에 섞이는 것 방지
# Q5. recv(1024) 한 번에 메시지 전체가 온다고 보장할 수 있나?
#     -> 아니오. TCP 는 바이트 스트림이므로 메시지 경계를 직접 구현해야 한다
#        (길이 헤더 또는 구분자 사용)
