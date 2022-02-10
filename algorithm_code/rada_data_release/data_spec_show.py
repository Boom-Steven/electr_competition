import keyboard as keyboard
import tftb
from rada_data_release import file_head_read, data_head_read, data_amplitude_read
from pulse_detect import envelope_detect
import matplotlib.pyplot as plt
import numpy as np

file_path = 'E:/python_project/python_20220114_electr_competition/data_file/测试数据包 信噪比15dB_消除敏感值.psc'
bin_file = open(file_path, 'rb')
file_head_dic = file_head_read.head_get(bin_file)
number_impulse = file_head_dic['11-采集脉冲个数'][0]

for nums in range(number_impulse):  # 遍历每一个雷达文件
    data_head_dic = data_head_read.head_get(bin_file)
    data_radar = data_amplitude_read.data_get(bin_file, file_head_dic, data_head_dic)

    ####################################时频图绘制#########################################
    # plt.specgram(data_radar, NFFT=1024, Fs=2.4e9, noverlap=512)  # 时频图绘制
    # plt.ylabel('frequency')  # 横纵坐标标识
    # plt.xlabel('time' + str(nums))
    # # plt.ylim(0, 2e8)  # 频率轴范围
    # plt.show()  # 时频图绘制
    ####################################时频图绘制#########################################

    ####################################时域波形绘制#########################################
    mse_envelope = envelope_detect.get_mse(data_radar, 200)
    [pulse_start_location, pulse_stop_location] = envelope_detect.get_pulse_location(mse_envelope)
    plt.plot(data_radar)
    plt.ylabel('amplitude')  # 横纵坐标标识
    plt.xlabel('time,file' + str(nums))

    for i in pulse_start_location:
        plt.axvline(i, c="r")

    ####################################时域波形绘制#########################################
    plt.show()
    keyboard.wait('down')  # 热键切换图片

bin_file.close()
