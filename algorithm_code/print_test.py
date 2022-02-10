# just a code test

import matplotlib.pyplot as plt
from rada_data_release import data_head_read

head_dic = data_head_read.head_get('data_file/测试数据包 信噪比15dB_消除敏感值.psc')

for value in head_dic.items():
    print(value)

# 用于解析雷达信号文件
import struct

file_path = 'data_file/测试数据包 信噪比15dB_消除敏感值.psc'
bin_file = open(file_path, 'rb')



bin_file.close()
