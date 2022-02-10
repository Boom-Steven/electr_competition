# 通信文件头读取
import struct


def head_get(bin_file):
    ###################格式字段读取#######################
    file_head_dic = \
        {
            '1-序号': struct.unpack_from('i', bin_file.read(4), 0),
            '2-采集时间': struct.unpack_from('s', bin_file.read(32), 0),
            '3-采样率MHz': struct.unpack_from('d', bin_file.read(8), 0),
            '4-中频频率MHz': struct.unpack_from('d', bin_file.read(8), 0),
            '5-中频带宽MHz': struct.unpack_from('d', bin_file.read(8), 0),
            '6-工作模式': struct.unpack_from('h', bin_file.read(2), 0)[0],
            '7-处理模式': struct.unpack_from('h', bin_file.read(2), 0),
            '8-控首频段起点频率MHz': struct.unpack_from('d', bin_file.read(8), 0),
            '9-控首频段终点频率MHz': struct.unpack_from('d', bin_file.read(8), 0),
            '10-样点个数': struct.unpack_from('i', bin_file.read(4), 0),
        }
    ###################格式字段读取#######################

    return file_head_dic
