from communication_data_release import file_head_read, data_amplitude_read
import matplotlib.pyplot as plt

file_path = 'E:\python_project\python_20220114_electr_competition\data_file\内场通信测试数据包.dat'
bin_file = open(file_path, 'rb')
file_head_dic = file_head_read.head_get(bin_file)
data_communication = data_amplitude_read.data_get(bin_file, file_head_dic)

plt.specgram(data_communication, NFFT=512, Fs=200e6, noverlap=256)  # 时频图绘制
plt.ylabel('frequency')  # 横纵坐标标识
plt.xlabel('time')
plt.ylim(5e7, 10e7)  # 频率轴范围
plt.show()  # 时频图绘制

bin_file.close()
