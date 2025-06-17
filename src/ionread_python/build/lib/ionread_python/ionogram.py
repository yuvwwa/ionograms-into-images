from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Bin:
    freq: int
    dist: float
    num_dist: int
    ampl: int

    @staticmethod
    def from_dict(obj: Any) -> 'Bin':
        _freq = int(obj.get("freq"))
        _dist = float(obj.get("dist"))
        _num_dist = int(obj.get("num_dist"))
        _ampl = int(obj.get("ampl"))
        return Bin(_freq, _dist, _num_dist, _ampl)

@dataclass
class Passport:
    transmitter: str
    receiver: str
    session_date: str
    session_time: str
    mode: str
    latency: int
    start_freq: int
    end_freq: int
    velocity: int
    analisys_wide: int
    antenna: str
    acp_number: int
    step_freq: int
    count_distances: int
    count_frequences: int
    gain_factor: int

    @staticmethod
    def from_dict(obj: Any) -> 'Passport':
        _transmitter = str(obj.get("transmitter"))
        _receiver = str(obj.get("receiver"))
        _session_date = str(obj.get("session_date"))
        _session_time = str(obj.get("session_time"))
        _mode = str(obj.get("mode"))
        _latency = int(obj.get("latency"))
        _start_freq = int(obj.get("start_freq"))
        _end_freq = int(obj.get("end_freq"))
        _velocity = int(obj.get("velocity"))
        _analisys_wide = int(obj.get("analisys_wide"))
        _antenna = str(obj.get("antenna"))
        _acp_number = int(obj.get("acp_number"))
        _step_freq = int(obj.get("step_freq"))
        _count_distances = int(obj.get("count_distances"))
        _count_frequences = int(obj.get("count_frequences"))
        _gain_factor = int(obj.get("gain_factor"))
        return Passport(_transmitter, _receiver, _session_date, _session_time, _mode, _latency, _start_freq, _end_freq, _velocity, _analisys_wide, _antenna, _acp_number, _step_freq, _count_distances, _count_frequences, _gain_factor)

@dataclass
class Ionogram:
    passport: Passport
    data: List[Bin]

    @staticmethod
    def from_dict(obj: Any) -> 'Ionogram':
        _passport = Passport.from_dict(obj.get("passport"))
        _data = [Bin.from_dict(y) for y in obj.get("data")]
        return Ionogram(_passport, _data)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)

# Convert source
# https://json2csharp.com/code-converters/json-to-python
