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

HOST = "127.0.0.1"
PORT = 1234

try:
    log("Try Connecting Server...", color.green)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

except Exception as e:
    log(f"Server Connecting fail!! {e}", color.red)

else:
    log("Server Connecting Complete!! :D", color.green)

    while True:
        machine = clinput()
        data = bytes(machine)
        client.sendall(data)

        for name, dtype in machinedata._fields_:
            print(name, ":", getattr(machine, name))

        time.sleep(1)

finally:
    client.close()
    log("Client Close", color.pink)