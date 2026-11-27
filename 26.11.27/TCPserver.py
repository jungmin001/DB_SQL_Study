from ctypes import Structure, c_char, c_int8, c_int16, c_int, c_float, c_double, c_bool, sizeof
import socket
import time
import pymysql
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

def query_command(conn, command, is_method = None, params  =None):
    if is_method is None:
        is_method = "SELECT" in command or "SHOW" in command

    with conn.cursor() as cur:
        cur.execute(command, params)
        if is_method:
            return cur.fetchall()

    conn.commit()

try:
    log("Try Connecting Server...", color.green)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    cli, adr = server.accept()

except:
    log("Server Connecting fail!!", color.red)

else:
    log("Server Connecting Complete!! :D", color.green)

    try:
        log("Try Connecting DB...")

        conn = pymysql.connect(
            host    = "127.0.0.1",
            port    = 3306,
            user    = "root",
            password= "0842",
            database= "testdb4"
        )

    except:
        log("DB Connecting fail!!", color.red)

    else:
        log("DB Connecting Complete!! :D", color.green)

        while True:
            data = cli.recv(24)
            if not data: break

            text = data.decode("utf-8") # tuple

            machine = machinedata.from_buffer_copy(data)

            params = (
                machine.type_bool,
                machine.type_char.decode("utf-8"),
                machine.type_int8,
                machine.type_int16,
                machine.type_int,
                machine.type_float,
                machine.type_double
            )

            query_command(
                conn,
                """
                INSERT INTO machine_data (
                    type_bool,
                    type_char,
                    type_int8,
                    type_int16,
                    type_int,
                    type_float,
                    type_double
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                params
            )

            result = query_command(
                conn,
                """
                SELECT * FROM machine_data
                WHERE id = LAST_INSERT_ID()
                """
            )

            for row in result:
                print(row)

            time.sleep(1)

finally:
    server.close()
    log("Server Close", color.pink)
