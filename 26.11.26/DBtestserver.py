import socket


HOST = "127.0.0.1"
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

client, addr = server.accept()

while True:
    data = client.recv(1024)

    if not data:
        break

    value = data.decode("utf-8")

    print("수신 :", value)

client.close()
server.close()