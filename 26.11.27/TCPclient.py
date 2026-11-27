from ctypes import Structure, c_char, c_int8, c_int16, c_int, c_float, c_double, c_bool, sizeof
import socket
import random
import time
from DebugHelper import log, color

class machinedata(Structure):
    _fields_ = [
        ("type_bool",   c_bool),    # 1byte
        ("type_char",   c_char),    # 1byte
        ("type_int8",   c_int8),    # 1byte
        ("pd_int8",     c_int8),    # 1byte padding
        ("type_int16",  c_int16),   # 2byte
        ("pd_int16",    c_int16),   # 2byte padding
        ("type_int",    c_int),     # 4byte
        ("type_float",  c_float),   # 4byte
        ("type_double", c_double),  # 8byte
    ]


HOST = "127.0.0.1"
PORT = 1234


def clinput():
    machine = machinedata()

    machine.type_bool   = random.choice([True, False])
    machine.type_char   = random.choice("ABCDE").encode("utf-8")
    machine.type_int8   = random.randint(-128, 127)
    machine.pd_int8     = 0
    machine.type_int16  = random.randint(-32768, 32767)
    machine.pd_int16    = 0
    machine.type_int    = random.randint(0, 100000)
    machine.type_float  = random.uniform(0.0, 100.0)
    machine.type_double = random.uniform(0.0, 100000.0)

    return machine


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    log("Try Connecting Server...", color.green)

    client.connect((HOST, PORT))

except:
    log("Server Connecting fail!!", color.red)

else:
    log("Server Connecting Complete!! :D", color.green)

    while True:
        # 랜덤 구조체 데이터 생성
        machine = clinput()

        # 구조체를 바이너리 데이터로 변환
        data = bytes(machine)

        # 서버에 데이터 전송
        client.sendall(data)

        # 전송한 데이터 출력
        for name, dtype in machinedata._fields_:
            print(name, ":", getattr(machine, name))

        print("Send Size:", len(data), "Byte")
        print("----------------------------")

        time.sleep(1)

finally:
    client.close()
    log("Client Close", color.pink)