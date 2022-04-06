# import cupy as cp
import numpy as np
import struct


class data_parser:
    def __init__(self, raw_data) -> None:
        self.data_buf = bytes(raw_data)
        self.ptr = 0

    def readn(self, n) -> bytes:
        self.ptr += n
        return self.data_buf[self.ptr - n:self.ptr]

    def read(self) -> bytes:
        return self.data_buf[self.ptr:]


def get_singnal_IQs(raw_data):
    fo = data_parser(raw_data)
    dataSerialNo = int.from_bytes(fo.readn(4), 'little')
    gatheringTime = fo.readn(32).decode('utf-8')
    sampleRate = struct.unpack('d', fo.readn(8))[0] * 1e6
    IFFreq = struct.unpack('d', fo.readn(8))[0] * 1e6
    IFBandWidth = struct.unpack('d', fo.readn(8))[0] * 1e6
    workingMode = int.from_bytes(fo.readn(2), 'little')
    processingMode = int.from_bytes(fo.readn(2), 'little')
    listeningBandStart = struct.unpack('d', fo.readn(8))[0] * 1e6
    listeningBandStop = struct.unpack('d', fo.readn(8))[0] * 1e6
    nofSamples = int.from_bytes(fo.readn(4), 'little')

    dt = np.dtype(np.int16).newbyteorder('<')
    rawdata = np.frombuffer(fo.read(), dtype=dt)
    IQ_cp_array = np.asarray(rawdata).astype(np.float32).reshape(-1, 2)
    IQ_cp_array = IQ_cp_array[:, 0] + np.multiply(IQ_cp_array[:, 1], 1j)

    # print(
    #     'dataSerialNo:', dataSerialNo, 
    #     '\ngatheringTime:', gatheringTime, 
    #     '\nsampleRate:', sampleRate, 
    #     '\nIFFreq:', IFFreq, 
    #     '\nIFBandWidth:', IFBandWidth, 
    #     '\nworkingMode:', workingMode, 
    #     '\nprocessingMode:', processingMode, 
    #     '\nlisteningBandStart:', listeningBandStart, 
    #     '\nlisteningBandStop:', listeningBandStop, 
    #     '\nnofSamples:', nofSamples
    #     )
    # if(len(IQ_cp_array) != nofSamples):
    #     raise('Sample length dismatch!')
    return {
        'dataSerialNo': dataSerialNo,
        'gatheringTime': gatheringTime,
        'sampleRate': sampleRate,
        'IFFreq': IFFreq,
        'IFBandWidth': IFBandWidth,
        'workingMode': workingMode,
        'processingMode': processingMode,
        'listeningBandStart': listeningBandStart,
        'listeningBandStop': listeningBandStop,
        'nofSamples': nofSamples,
        'IQSamples': IQ_cp_array
    }
