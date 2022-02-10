# 用于解析雷达信号文件
import struct

file_path = 'data_file/测试数据包 信噪比15dB_消除敏感值.psc'
bin_file = open(file_path, 'rb')

###################格式字段读取#######################
data_1 = struct.unpack_from('Q', bin_file.read(8), 0)
print('文件总长度', data_1)

data_2 = struct.unpack_from('h', bin_file.read(2), 0)
print('文件头长度', data_2)

data_3 = struct.unpack_from('s', bin_file.read(14), 0)
print('采集设备代码', data_3)

data_4 = struct.unpack_from('Q', bin_file.read(8), 0)
print('起始基准时间100ns', data_4)

data_5 = struct.unpack_from('I', bin_file.read(4), 0)
print('接收机中心频率kHz', data_5)

data_6 = struct.unpack_from('I', bin_file.read(4), 0)
print('中心频率kHz', data_6)

data_7 = struct.unpack_from('I', bin_file.read(4), 0)
print('中频带宽kHz', data_7)

data_8 = struct.unpack_from('I', bin_file.read(4), 0)
print('采样率kSps', data_8)

data_9 = struct.unpack_from('b', bin_file.read(1), 0)
print('采样深度代码（见附件A2）', data_9)

data_10 = struct.unpack_from('b', bin_file.read(1), 0)
print('变换方式', data_10)

data_11 = struct.unpack_from('I', bin_file.read(4), 0)
print('采集脉冲个数', data_11)

data_12 = struct.unpack_from('H', bin_file.read(2), 0)
print('天线起始指向deg', data_12)

data_13 = struct.unpack_from('H', bin_file.read(2), 0)
print('天线中止指向deg', data_13)

data_14 = struct.unpack_from('b', bin_file.read(1), 0)
print('采集方式', data_14)

data_15 = struct.unpack_from('b', bin_file.read(1), 0)
print('采集模式', data_15)

data_16 = struct.unpack_from('b', bin_file.read(1), 0)
print('天线类型', data_16)

data_17 = struct.unpack_from('b', bin_file.read(1), 0)
print('天线波束', data_17)

data_18 = struct.unpack_from('H', bin_file.read(2), 0)
print('射频衰减dB', data_18)

data_19 = struct.unpack_from('H', bin_file.read(2), 0)
print('中频衰减dB', data_19)

data_20 = struct.unpack_from('c', bin_file.read(12), 0)
print('设备地理位置', data_20)

data_21 = struct.unpack_from('H', bin_file.read(2), 0)
print('保留', data_21)

data_22 = struct.unpack_from('Q', bin_file.read(8), 0)
print('脉冲到达时间ns', data_22)

data_23 = struct.unpack_from('I', bin_file.read(4), 0)
print('脉冲频率kHz', data_23)

data_24 = struct.unpack_from('I', bin_file.read(4), 0)
print('脉冲脉宽ns', data_24)

data_25 = struct.unpack_from('h', bin_file.read(2), 0)
print('脉冲功率/幅度，dBm/dB', data_25)

data_26 = struct.unpack_from('H', bin_file.read(2), 0)
print('脉冲到达角deg', data_26)

data_27 = struct.unpack_from('B', bin_file.read(1), 0)
print('脉内调制类型', data_27)

data_28 = struct.unpack_from('h', bin_file.read(2), 0)
print('脉冲信噪比的dB', data_28)

data_29 = struct.unpack_from('B', bin_file.read(1), 0)
print('脉冲采集信道', data_29)

data_30 = struct.unpack_from('B', bin_file.read(1), 0)
print('脉冲采集波束', data_30)

data_31 = struct.unpack_from('I', bin_file.read(4), 0)
print('脉冲上升沿保护长度', data_31)

data_32 = struct.unpack_from('I', bin_file.read(4), 0)
print('脉冲下降沿保护长度', data_32)

data_33 = struct.unpack_from('I', bin_file.read(4), 0)
print('脉冲采样点个数', data_33)

# _______脉冲幅值数据格式由采样深度决定________#
A2_code = int(data_9[0])
if A2_code == 1:
    # 有符号的单字节整数
    data_34 = struct.unpack_from('b', bin_file.read(1), 0)
    print('脉冲幅值', data_34)
elif A2_code == 2:
    # 无符号的单字节整数
    data_34 = struct.unpack_from('B', bin_file.read(1), 0)
    print('脉冲幅值', data_34)
elif A2_code == 3:
    # 有符号的双字节整数
    data_34 = struct.unpack_from('h', bin_file.read(2), 0)
    print('脉冲幅值', data_34)
elif A2_code == 4:
    # 无符号的双字节整数
    data_34 = struct.unpack_from('H', bin_file.read(2), 0)
    print('脉冲幅值', data_34)
elif A2_code == 5:
    # 有符号的四字节整数
    data_34 = struct.unpack_from('i', bin_file.read(4), 0)
    print('脉冲幅值', data_34)
elif A2_code == 6:
    # 无符号的四字节整数
    data_34 = struct.unpack_from('I', bin_file.read(4), 0)
    print('脉冲幅值', data_34)
elif A2_code == 7:
    # 单精度浮点
    data_34 = struct.unpack_from('f', bin_file.read(4), 0)
    print('脉冲幅值', data_34)
elif A2_code == 8:
    # 双精度浮点
    data_34 = struct.unpack_from('d', bin_file.read(8), 0)
    print('脉冲幅值', data_34)
else:
    print('脉冲幅值字段无效或备用未录入')
# _______脉冲幅值数据格式由采样深度决定________#

###################格式字段读取#######################

bin_file.close()
