# 用于Unix与windows绝对时间的换算
from datetime import datetime


def read_real_time(head_dic):
    timestamp = head_dic['4-起始基准时间100ns'][0]#todo 时间戳换算 win32 to Unix
    real_time = datetime.fromtimestamp(timestamp)
    return real_time
