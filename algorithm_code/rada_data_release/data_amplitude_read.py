# 脉冲幅度的读取--80byte之后
# 数据类型由'9-采样深度代码'决定
# 实数采集或IQ采集'15-采集模式'由决定
# 需要考虑数据长度
import struct


def data_get(bin_file, file_head_dic, data_head_dic):
    ###################数据字段读取#######################
    a2_code = int(file_head_dic["9-采样深度代码（见附件A2）"][0])  # 采样数据格式
    count = int(data_head_dic['33-脉冲采样点个数'][0])  # 周期长度
    sample_mode = int(file_head_dic['15-采集模式'][0])  # 实数采样或IQ采样
    ###################数据字段读取#######################
    data_radar = []

    if sample_mode == 1:  # 实数采集

        # <editor-fold desc="采样深度判断、实数模式数据读取">
        if a2_code == 1:
            # 有符号的单字节整数
            for i in range(count):
                data_radar.append(struct.unpack_from('b', bin_file.read(1), 0)[0])
        elif a2_code == 2:
            # 无符号的单字节整数
            for i in range(count):
                data_radar.append(struct.unpack_from('B', bin_file.read(1), 0)[0])
        elif a2_code == 3:
            # 有符号的双字节整数
            for i in range(count):
                data_radar.append(struct.unpack_from('h', bin_file.read(2), 0)[0])
        elif a2_code == 4:
            # 无符号的双字节整数
            for i in range(count):
                data_radar.append(struct.unpack_from('H', bin_file.read(2), 0)[0])
        elif a2_code == 5:
            # 有符号的四字节整数
            for i in range(count):
                data_radar.append(struct.unpack_from('i', bin_file.read(4), 0)[0])
        elif a2_code == 6:
            # 无符号的四字节整数
            for i in range(count):
                data_radar.append(struct.unpack_from('I', bin_file.read(4), 0)[0])
        elif a2_code == 7:
            # 单精度浮点
            for i in range(count):
                data_radar.append(struct.unpack_from('f', bin_file.read(4), 0)[0])
        elif a2_code == 8:
            # 双精度浮点
            for i in range(count):
                data_radar.append(struct.unpack_from('d', bin_file.read(8), 0)[0])
        else:
            print('脉冲幅值字段无效或备用未录入')
        # </editor-fold>

    elif sample_mode == 2:  # IQ采集

        # <editor-fold desc="采样深度判断、IQ模式数据读取">
        if a2_code == 1:
            # 有符号的单字节整数
            for i in range(count / 2):  # 实部
                data_radar.append(struct.unpack_from('b', bin_file.read(1), 0)[0])
                data_radar.append(0)
            for i in range(count / 2):  # 虚部
                data_radar[2 * i] = struct.unpack_from('b', bin_file.read(1), 0)[0]

        elif a2_code == 2:
            # 无符号的单字节整数
            for i in range(count / 2):
                data_radar.append(struct.unpack_from('B', bin_file.read(1), 0)[0])
                data_radar.append(0)
            for i in range(count / 2):  # 虚部
                data_radar[2 * i] = struct.unpack_from('B', bin_file.read(1), 0)[0]
        elif a2_code == 3:
            # 有符号的双字节整数
            for i in range(count / 2):
                data_radar.append(struct.unpack_from('h', bin_file.read(2), 0)[0])
                data_radar.append(0)
            for i in range(count / 2):  # 虚部
                data_radar[2 * i] = struct.unpack_from('h', bin_file.read(2), 0)[0]
        elif a2_code == 4:
            # 无符号的双字节整数
            for i in range(count / 2):
                data_radar.append(struct.unpack_from('H', bin_file.read(2), 0)[0])
                data_radar.append(0)
            for i in range(count / 2):  # 虚部
                data_radar[2 * i] = struct.unpack_from('H', bin_file.read(2), 0)[0]
        elif a2_code == 5:
            # 有符号的四字节整数
            for i in range(count / 2):
                data_radar.append(struct.unpack_from('i', bin_file.read(4), 0)[0])
                data_radar.append(0)
            for i in range(count / 2):  # 虚部
                data_radar[2 * i] = struct.unpack_from('i', bin_file.read(4), 0)[0]
        elif a2_code == 6:
            # 无符号的四字节整数
            for i in range(count / 2):
                data_radar.append(struct.unpack_from('I', bin_file.read(4), 0)[0])
                data_radar.append(0)
            for i in range(count / 2):  # 虚部
                data_radar[2 * i] = struct.unpack_from('I', bin_file.read(4), 0)[0]
        elif a2_code == 7:
            # 单精度浮点
            for i in range(count / 2):
                data_radar.append(struct.unpack_from('f', bin_file.read(4), 0)[0])
                data_radar.append(0)
            for i in range(count / 2):  # 虚部
                data_radar[2 * i] = struct.unpack_from('f', bin_file.read(4), 0)[0]
        elif a2_code == 8:
            # 双精度浮点
            for i in range(count / 2):
                data_radar.append(struct.unpack_from('d', bin_file.read(8), 0)[0])
                data_radar.append(0)
            for i in range(count / 2):  # 虚部
                data_radar[2 * i] = struct.unpack_from('d', bin_file.read(8), 0)[0]
        else:
            print('脉冲幅值字段无效或备用未录入')
        # </editor-fold>

    else:
        print("'['15-采集模式'], 传入失败'")

    return data_radar
