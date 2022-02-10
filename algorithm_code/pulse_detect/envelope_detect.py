# 根据matlab测试结果，envelope的提取方法采用RMS的均方根估计效果最好、抗噪声性能更强
# 输出坐标数组与flag指示数组（a代变上升沿，b代表下降沿，c代变采样截止点）
import math
import numpy as np


def get_mse(radar_data, x_scale):  # todo 窗口尺度的迭代
    """
    获取均方根估计值，用作包络估计
    :param radar_data: 雷达数据
    :param x_scale: 均方根尺度（迭代更新一次）
    :return: 输出包络数组
    """

    nums_sample = len(radar_data)
    mse_envelope = [0 for _ in range(nums_sample)]
    for i in range(nums_sample - x_scale - 1):
        data_in_scale = radar_data[i:i + x_scale]
        mse_envelope[i] = math.sqrt(sum(x ** 2 for x in data_in_scale)) / x_scale
    return mse_envelope


def get_pulse_location(mse_envelope):
    """
    抓取脉冲位置
    :param mse_envelope: 包络数据
    :return: 【脉冲上升沿坐标，脉冲下降沿坐标】
    """
    # 脉冲包络求微分
    mse_envelope = np.array(mse_envelope)  # 数组转numpy
    div_envelope = np.diff(mse_envelope)  # 数组求差分/微分

    # _________________________微分滑动窗积分求冲击_____________________________#
    x_scale = 200  # 滑窗步长
    w_scale = 400  # 滑窗宽度
    div_envelope_window = np.zeros(1)
    for i in range(0, len(div_envelope), x_scale):  # 0-结尾，步长为x_scale
        div_envelope_window = np.append(div_envelope_window, np.sum(div_envelope[i:i + w_scale]))

    data = div_envelope_window
    average_abs_envelope = np.max(data) / 2

    pulse_start_location = np.zeros(1)  # 新建空数组
    pulse_flag_location = np.zeros(1)

    for i in range(len(div_envelope_window)):
        if div_envelope_window[i] >= average_abs_envelope:  # 上升沿
            pulse_flag_location = np.append(pulse_flag_location, 'a')
            pulse_start_location = np.append(pulse_start_location, (i * x_scale + w_scale / 2))
        elif div_envelope_window[i] <= -average_abs_envelope:  # 下降沿
            pulse_flag_location = np.append(pulse_flag_location, 'b')
            pulse_start_location = np.append(pulse_start_location, (i * x_scale + w_scale / 2))

    pulse_flag_location = np.delete(pulse_flag_location, 0)  # 删掉首位零元素
    pulse_flag_location = np.append(pulse_flag_location, 'c')  # 增加末尾元素
    pulse_start_location = np.delete(pulse_start_location, 0)
    pulse_start_location = np.append(pulse_start_location, 0)
    # _________________________坐标数据处理（重复数据整合）_____________________________#
    pulse_start_location_final = np.zeros(1)  # 新建空数组
    pulse_flag_location_final = np.zeros(1)
    flag_count = 1
    average_location = 0
    for i in range(len(pulse_start_location) - 1):  # 重复数据取平均
        if pulse_flag_location[i] == pulse_flag_location[i + 1]:
            flag_count = flag_count + 1
        else:
            for j in range(flag_count):
                average_location = average_location + pulse_start_location[i - j]
            pulse_start_location_final = np.append(pulse_start_location_final, (int(average_location / flag_count)))
            pulse_flag_location_final = np.append(pulse_flag_location_final, pulse_flag_location[i])
            flag_count = 1
            average_location = 0
    # _________________________坐标数据处理（重复数据整合）_____________________________#
    pulse_start_location_final = np.delete(pulse_start_location_final, 0)  # 删掉首位零元素
    pulse_flag_location_final = np.delete(pulse_flag_location_final, 0)  # 删掉首位零元素
    loc_ans = [pulse_start_location_final.tolist(), pulse_flag_location_final.tolist()]  # 拼接数据输出{位置坐标，指示标志}
    print(loc_ans)
    return loc_ans
