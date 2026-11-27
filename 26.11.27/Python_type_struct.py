from dataclasses import dataclass

@dataclass
class machinedata:
    type_bool:  bool  | None = None
    type_str:   str   | None = None
    type_int8:  int   | None = None
    type_float: float | None = None