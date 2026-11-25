import socket

HOST = "127.0.0.1"
PORT = 1234

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    text = input("전송 : ")
    client.sendall(text.encode("utf-8"))  # 들리십니까

    if text == "종료":  # 고마 끊소
        break

    data = client.recv(1024)  # 받는건 1024바이트만

    if not data:  # 통신불량 브레끼
        break

    text = data.decode("utf-8")  # 여보세요
    print("수신 :", text)

    if text == "종료":  # 어이 고마 브레끼 밟소
        break

client.close()
