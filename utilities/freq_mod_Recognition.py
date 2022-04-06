# By GuJi in WT&T, BUPT
# from utilities.N_order_Carrier_Sync import N_order_Carrier_Sync
from utilities.peroid_estimate import period_estimate
import cupy as cp
import numpy as np
# import matplotlib.pyplot as plt
from utilities.main_lobe_BW_estimate import main_lobe_BW_estimate
from scipy.signal import find_peaks

def freq_mod_recognition(signal_, fft_signal_):
    # fft_signal = fft_signal_.copy()
    signal = signal_
    
    # [carrier, freqs] = cp.asarray(N_order_Carrier_Sync(1, cp.asnumpy(signal), 0, 1e-3, 1e-3))

    signal_slice_last = cp.concatenate((cp.array([0]), signal[:-1]))
    aa = signal * cp.conj(signal_slice_last)
    aa = aa / (cp.abs(signal)**2)

    FM_Demod_Signal = cp.imag(aa[2:])
    i_demod_BW = main_lobe_BW_estimate(cp.fft.fft(FM_Demod_Signal), 5)
    FM_Demod_Signal = FM_Demod_Signal[i_demod_BW*2:-i_demod_BW*2]


    i_demod_BW = main_lobe_BW_estimate(cp.fft.fft(FM_Demod_Signal), 5)
    gaussian_sigma = min(len(signal)/i_demod_BW/4, len(signal)/16)
    gaussian_half_size = gaussian_sigma*10
    # gaussian_x = fftsize/2-cp.abs(cp.arange(0, fftsize)-fftsize/2)
    gaussian_x = cp.abs(cp.arange(0, gaussian_half_size*2+1)-gaussian_half_size)
    gaussian_window = cp.exp(-cp.power(gaussian_x/gaussian_sigma, 2)/2)
    FM_Demod_Signal_filtered = cp.convolve(FM_Demod_Signal, gaussian_window, mode='same')
    # ee = FM_Demod_Signal
    # plt.plot(cp.asnumpy(FM_Demod_Signal))
    # plt.show()
    # 计算符号速率
    demod_symbol_len = period_estimate(cp.fft.fft(cp.abs(FM_Demod_Signal_filtered)), round(len(FM_Demod_Signal)/i_demod_BW))
    # print("demod_symbol_len:", demod_symbol_len)

    if(demod_symbol_len == 0):
        return ["FM", 0]
    
    # 计算频率个数
    gaussian_sigma = min(demod_symbol_len/8, len(signal)/16)
    gaussian_half_size = gaussian_sigma*10
    # gaussian_x = fftsize/2-cp.abs(cp.arange(0, fftsize)-fftsize/2)
    gaussian_x = cp.abs(cp.arange(0, gaussian_half_size*2+1)-gaussian_half_size)
    gaussian_window = cp.exp(-cp.power(gaussian_x/gaussian_sigma, 2)/2)
    FM_Demod_Signal_filtered = cp.convolve(FM_Demod_Signal, gaussian_window, mode='same')
    # plt.plot(cp.asnumpy(FM_Demod_Signal))
    # plt.plot(cp.asnumpy(FM_Demod_Signal_filtered))
    # plt.show()
    FM_Demod_Signal_filtered_normalized = FM_Demod_Signal_filtered / cp.max(cp.abs(FM_Demod_Signal_filtered)) * 0.9
    resolution = 64
    # freq_count = np.zeros(resolution)

    # for i_freq in range(len(FM_Demod_Signal_filtered_normalized)):
    #     i_freq_in_count = min(int(((FM_Demod_Signal_filtered_normalized[i_freq]+1)/2)*resolution), resolution-1)
    #     freq_count[i_freq_in_count] += 1
    # print(type(FM_Demod_Signal_filtered_normalized))
    freq_count = cp.asnumpy(cp.histogram(FM_Demod_Signal_filtered_normalized, bins=resolution, range=(-1, 1))[0])
    # plt.stem(freq_count)
    # plt.plot(np.ones(resolution)*len(FM_Demod_Signal_filtered_normalized)/resolution)
    # plt.show()
    nof_freq = find_peaks(np.clip(freq_count, len(FM_Demod_Signal_filtered_normalized)/resolution, None))[0]
    # print("!!!!!!!!!!!!", max(freq_count)/(len(FM_Demod_Signal_filtered_normalized)/resolution))
    freq_cnt_PAR = max(freq_count)/(len(FM_Demod_Signal_filtered_normalized)/resolution)
    if(len(nof_freq) == 2):
        mean_delta_freq = np.sqrt(np.mean(FM_Demod_Signal**2))*2 / (2*np.pi)
        demod_symbol_rate = 1/demod_symbol_len
        fm_factor = mean_delta_freq/demod_symbol_rate
        if(freq_cnt_PAR < 10 and fm_factor < 0.5):
            return ["GMSK", demod_symbol_len]
        if(fm_factor > 0.75 or fm_factor < 0.375):
            return ["2FSK", demod_symbol_len]
        return ["MSK", demod_symbol_len]
        # print('mean_delta_freq:', mean_delta_freq, 'demod_symbol_rate:', demod_symbol_rate, 'ratio:', mean_delta_freq/demod_symbol_rate)
        # print("!!!!!!!!!!!!", max(freq_count)/(len(FM_Demod_Signal_filtered_normalized)/resolution))
    if(len(nof_freq) == 4):
        return ["4FSK", demod_symbol_len]
    if(len(nof_freq) == 8):
        return ["8FSK", demod_symbol_len]
    return ["N/A", demod_symbol_len]