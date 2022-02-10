# 用于解读取雷达信号头文件
import struct


def head_get(bin_file):
    ###################格式字段读取#######################
    data_head_dic = \
        {
            '22-脉冲到达时间ns': struct.unpack_from('Q', bin_file.read(8), 0),
            '23-脉冲频率kHz': struct.unpack_from('I', bin_file.read(4), 0),
            '24-脉冲脉宽ns': struct.unpack_from('I', bin_file.read(4), 0),
            '25-脉冲功率/幅度，dBm/dB': struct.unpack_from('h', bin_file.read(2), 0),
            '26-脉冲到达角deg': struct.unpack_from('H', bin_file.read(2), 0),
            '27-脉内调制类型': hex(struct.unpack_from('b', bin_file.read(1), 0)[0]),
            '28-脉冲信噪比的dB': struct.unpack_from('h', bin_file.read(2), 0),
            '30-脉冲采集波束': struct.unpack_from('B', bin_file.read(1), 0),
            '29-脉冲采集信道': struct.unpack_from('B', bin_file.read(1), 0),
            '31-脉冲上升沿保护长度': struct.unpack_from('I', bin_file.read(4), 0),
            '32-脉冲下降沿保护长度': struct.unpack_from('I', bin_file.read(4), 0),
            '33-脉冲采样点个数': struct.unpack_from('I', bin_file.read(4), 0)
        }
    ###################格式字段读取#######################

    return data_head_dic


if __name__ == '__main__':
    ans = head_get('../data_file/测试数据包 信噪比15dB_消除敏感值.psc')
