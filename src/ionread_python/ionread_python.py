

import io
# from . import ionogram
from typing import List
from typing import Dict


if __package__ is None or __package__ == '':
    import ionogram
    import passport_constants as cfg
else:
    from . import ionogram
    from . import passport_constants as cfg

# from . import ionogram
import re

BLOCK_SIZE = 4

# Смещение амплитуды внутри блока данных
OFFSET_AMPLITUDE = 0

# Смещение высоты внутри блока
OFFSET_HEIGHT = 2

# Скорость света м/с
LIGHT_VELOCITY = 300000000


def get_pasp_value_double(paspport_map: Dict[str, str], pasport_key: str) -> float:
    valued_string = paspport_map[pasport_key]
    m = re.search(r'[-+]?(?:\d*(?:\.|,)*\d+)', valued_string)

    return float(m[0].replace(',', '.'))


def get_pasp_value_int(paspport_map: Dict[str, str], pasport_key: str) -> int:
    return int(get_pasp_value_double(paspport_map, pasport_key))


def get_pasp_value_string(paspport_map: Dict[str, str], pasport_key: str):
    return paspport_map[pasport_key]


def CalcStartHeight(passport: ionogram.Passport) -> float:
    '''
    Начальная дальность для ионограммы в метрах
    '''
    latency = passport.latency  # "7.00 мс"
    return (latency / float(1000)) * LIGHT_VELOCITY


def CalcEndHeight(passport: ionogram.Passport) -> float:
    '''
    Конечная дальность для ионограммы
    '''
    mode = passport.mode
    p = passport.analisys_wide
    v = passport.velocity * 1000
    t = passport.latency / float(1000)
    c = LIGHT_VELOCITY

    if (mode == "ВЗ"):

        return (c * p) / v + c * t 
        # return (c * p) / (2 * v) + c * t / 2

    if (mode == "НЗ"):

        return (c * p) / v + c * t

    return 0


def read_ionogram(path: str) -> ionogram.Ionogram:

    with open(path, 'rb') as f:
        byte_array = f.read()
        dataLength = len(byte_array)

        counter = 0
        pasp_trigger = 0

        # В цикле ищем окончание паспорта
        while (pasp_trigger < 4 and counter < dataLength - 1):
            counter += 1
            pasp_trigger = pasp_trigger + 1 if byte_array[counter] == 0 else 0

        passport_bytes = byte_array[:counter-4]

        pasport_string = str(passport_bytes, 'cp866')

        # print(pasport_string)

        passport_lines = pasport_string.splitlines()
        passport_map_raw = {}

        def convert_pasport_lines_to_dict(passport_lines):
            for l in passport_lines:
                m_splited = l.split(':', maxsplit=1)

                key = m_splited[0]
                value = str(m_splited[1]).strip()

                passport_map_raw[key] = value

            return passport_map_raw

        passport_map_raw = convert_pasport_lines_to_dict(passport_lines)

        way = get_pasp_value_string(passport_map_raw, cfg.WAY)

        points = way.split('/')  # По умолчанию трасса делится символом "/"

        # Также трасса может делиться символом "-" (для обратной совместимости)
        if (len(points) == 1):
            points = way.split('-')

        transmitter = points[0].strip()
        receiver = points[1].strip()

        p_map = {'transmitter': transmitter,
                 'receiver': receiver,
                 'session_date': get_pasp_value_string(passport_map_raw, cfg.SESSION_DATE),
                 'session_time': get_pasp_value_string(passport_map_raw, cfg.SESSION_TIME),
                 'mode': get_pasp_value_string(passport_map_raw, cfg.MODE),
                 'latency': get_pasp_value_int(passport_map_raw, cfg.LATENCY),
                 'start_freq': get_pasp_value_int(passport_map_raw, cfg.START_FREQ_NAME),
                 'end_freq': get_pasp_value_int(passport_map_raw, cfg.END_FREQ_NAME),
                 'velocity': get_pasp_value_int(passport_map_raw, cfg.VELOCITY),
                 'analisys_wide': get_pasp_value_int(passport_map_raw, cfg.ANALSYS_WIDE),
                 'antenna': get_pasp_value_string(passport_map_raw, cfg.ANTENNA),
                 'acp_number': get_pasp_value_int(passport_map_raw, cfg.ACP_NUMBER),
                 'step_freq': get_pasp_value_int(passport_map_raw, cfg.STEP_FREQ_NAME),
                 'count_distances': 0,
                 'count_frequences': 0,
                 'gain_factor': get_pasp_value_int(passport_map_raw, cfg.GAIN_FACTOR)}

        passport = ionogram.Passport.from_dict(p_map)

        # exit()

        offsetInCluster = 0
        num_freq = 0

        start_freq = passport.start_freq
        step_freq = passport.step_freq

        # Стартовая и конечная дистанции в километрах
        start_real_d = round(CalcStartHeight(passport) / 1000)
        end_real_d = round(CalcEndHeight(passport) / 1000)

        bins: List[ionogram.Bin] = []

        for i in range(counter + 1, dataLength, BLOCK_SIZE):
            # Начало кластера, если старший бит == 1
            # TODO Потенциальная проблема может быть здесь
            # offsetInCluster = (int)(unsigned char)bytes[i] >= 0x80 ? 0 : offsetInCluster + 1;
            offsetInCluster = 0 if byte_array[i] >= 0x80 else offsetInCluster + 1

            if (offsetInCluster == 0):
                # Признаком начала очередного кластера информации является наличие «1» в старшем разряде первого слова,
                # при этом остальные биты этого двухбайтного слова определяют номер этого кластера в файле
                # (координату X при построении ионограммы, при этом максимально возможное значение
                # координаты X равно 600) и несут информацию о частоте зондирования.
                num_freq += 1
            else:
                h = (byte_array[i + OFFSET_HEIGHT]
                     ) << 8 | byte_array[i + OFFSET_HEIGHT + 1]
                ampl = (byte_array[i + OFFSET_AMPLITUDE]
                        ) << 8 | byte_array[i + OFFSET_AMPLITUDE + 1]

                freq = start_freq + step_freq * num_freq

                ion_bin = ionogram.Bin(
                    freq=freq, dist=h, num_dist=h, ampl=ampl)
                bins.append(ion_bin)

        # [backward_compat] В старых ионограммах не всегда встречаются блоки с минимальной задержкой
        # например минимальный номер задержки в таких случайх может быть равен 73, а не 1
        # но для корректного отображения шкалы задержек, необходимо,
        # чтобы это число ([min_d_bin.dist]) равнялось 1
        if not [b for b in bins if b.num_dist == 1]:
            bins.append(ionogram.Bin(freq=passport.start_freq + passport.step_freq, dist=1, num_dist=1, ampl=1))

        # Сырые данные преобразовываем в конкретные значения высот и частот
        # Здесь ищется максимальный номер высоты в данных! Для обеспечения обратной совместимости необходимо,
        # чтобы в ионограмме обязательно присутствовал бин с максимальной высотой (дистанцией)!
        # Можно добавлять фейковый бин с незначимой (маленькой, например 1) амплитудой и максимальной высотой!
        max_d_bin = max(bins, key=lambda b: b.dist)
        min_d_bin = min(bins, key=lambda b: b.dist)

        count_distances = max_d_bin.dist - min_d_bin.dist + 1

        passport.count_distances = count_distances
        passport.count_frequences = num_freq

        # Коэффициент поправки для коррекции шкалы высот
        k = (end_real_d - start_real_d) / (count_distances) 

        for b in bins:
            b.dist = start_real_d + b.num_dist * k

        output_ingr = ionogram.Ionogram(passport, bins)

        # print('Success reading!\n', pasport_string)

        return output_ingr


# print('fgh')
