# 用于解读取雷达信号头文件
import struct


def head_get(bin_file):

    ###################格式字段读取#######################
    file_head_dic = \
        {'1-文件总长度': struct.unpack_from('Q', bin_file.read(8), 0),
         '2-文件头长度': struct.unpack_from('H', bin_file.read(2), 0),
         '3-采集设备代码': struct.unpack_from('s', bin_file.read(14), 0),
         '4-起始基准时间100ns': struct.unpack_from('Q', bin_file.read(8), 0),
         '5-接收机中心频率kHz': struct.unpack_from('I', bin_file.read(4), 0),
         '6-中心频率kHz': struct.unpack_from('I', bin_file.read(4), 0),
         '7-中频带宽kHz': struct.unpack_from('I', bin_file.read(4), 0),
         '8-采样率kSps': struct.unpack_from('I', bin_file.read(4), 0),
         '9-采样深度代码（见附件A2）': struct.unpack_from('b', bin_file.read(1), 0),
         '10-变换方式': struct.unpack_from('b', bin_file.read(1), 0),
         '11-采集脉冲个数': struct.unpack_from('I', bin_file.read(4), 0),
         '12-天线起始指向deg': struct.unpack_from('H', bin_file.read(2), 0),
         '13-天线中止指向deg': struct.unpack_from('H', bin_file.read(2), 0),
         '14-采集方式': struct.unpack_from('b', bin_file.read(1), 0),
         '15-采集模式': struct.unpack_from('b', bin_file.read(1), 0),
         '16-天线类型': struct.unpack_from('b', bin_file.read(1), 0),
         '17-天线波束': struct.unpack_from('b', bin_file.read(1), 0),
         '18-射频衰减dB': struct.unpack_from('H', bin_file.read(2), 0),
         '19-中频衰减dB': struct.unpack_from('H', bin_file.read(2), 0),
         '20-设备地理位置': struct.unpack_from('c', bin_file.read(12), 0),
         '21-保留': struct.unpack_from('H', bin_file.read(2), 0),
         }
    ###################格式字段读取#######################

    return file_head_dic


if __name__ == '__main__':
    head_get('E:/python_project/python_20220114_electr_competition/data_file/测试数据包 信噪比15dB_消除敏感值.psc')
