import socket

HOST = "127.0.0.1"
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4, tcp 소켓 생성
server.bind((HOST, PORT)) # ip, 포트 할당
server.listen() # 연결 요청
# client : 클라이언트 소켓 (즈나기)
# addr : 클라이언트 ip, port (즈나브노)
client, addr = server.accept() 

while True:
    # 클라이언트 메시지 수신 1024바이트까지만 받음
    data = client.recv(1024)

    if not data: # 송신 종료하믄 브레끼
        break

    text = data.decode("utf-8") # 여보세용
    print("수신 :", text)

    if text == "종료": # 종료를 외쳐도 브레끼
        break

    text = input("전송 : ") 
    client.sendall(text.encode("utf-8")) # 들리십니까

    if text == "종료": # 고마 끊소
        break

client.close()
server.close()