from ctypes import Structure, c_char, c_int8, c_int16, c_int, c_float, c_double, c_bool, sizeof

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

for name, dtype in machinedata._fields_:
    print(name, "Size:", sizeof(dtype),)

print("\nTotal Size:", sizeof(machinedata))
