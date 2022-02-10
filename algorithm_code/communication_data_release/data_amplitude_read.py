# 读取通信调制信号的数据
import struct

data_communication = []


def data_get(bin_file, file_head_dic):
    count = int(file_head_dic['10-样点个数'][0])
    for i in range(count):
        data_I = struct.unpack_from('h', bin_file.read(2), 0)[0]
        data_Q = struct.unpack_from('h', bin_file.read(2), 0)[0]
        data_communication.append(complex(data_I, data_Q))

    return data_communication
