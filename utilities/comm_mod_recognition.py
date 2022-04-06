import utilities.constellation_recognition as constellation_recognition
from utilities.clock_sync import clock_sync
from utilities.peroid_estimate import period_estimate
from sympy import sign
from utilities.freq_mod_Recognition import freq_mod_recognition
import cupy as cp
import numpy as np
# By GuJi in WT&T, BUPT
from utilities.main_lobe_BW_estimate import main_lobe_BW_estimate
from utilities.N_order_Carrier_Sync import N_order_Carrier_Sync
# import matplotlib.pyplot as plt

def mod_recognition(signal):

    slice_len = min(len(signal), 1048576)
    signal_slice = signal[:slice_len].copy()
    fft_signal_slice = cp.fft.fft(signal_slice)

    # envelope characteristics
    fft_signal_5BW = fft_signal_slice.copy()
    i_BW = main_lobe_BW_estimate(fft_signal_slice, 10)
    fft_signal_5BW[i_BW*5+1:-(i_BW*5)] = 0
    signal_5BW = cp.fft.ifft(fft_signal_5BW)

    envelope = cp.abs(signal_5BW)
    average_power = cp.power(cp.average(envelope), 2)
    var_envelope = cp.var(envelope)
    var_to_power_ratio = var_envelope / average_power
    # plt.plot(np.abs(cp.asnumpy(signal)))
    # plt.show()

    # 直流分量计算 

    line_spectrum_pos = cp.argmax(abs(fft_signal_5BW))
    pwr_spectrum_rolled = cp.roll(cp.power(cp.abs(fft_signal_5BW), 2), -line_spectrum_pos)
    DC_Power = cp.sum(pwr_spectrum_rolled[:2]) + cp.sum(pwr_spectrum_rolled[-1:])
    ALL_Power = cp.sum(pwr_spectrum_rolled)
    DC_Power_ratio = DC_Power/ALL_Power
    # plt.plot(cp.asnumpy(cp.fft.fftshift(pwr_spectrum_rolled)))
    # plt.show()

    print("var_to_average_ratio:", var_to_power_ratio, ', DC_ratio:', DC_Power_ratio)
    # Freq Demodulation
    # signal_slice_last = cp.concatenate((cp.array([0]), signal_slice[:-1]))
    # aa = signal_slice * cp.conj(signal_slice_last)
    # aa = aa / cp.abs(aa)
    # plt.plot(cp.asnumpy(cp.imag(aa)))
    # plt.show()
    mod_type = ["N/A", 0]
    if(var_to_power_ratio < 0.002 and DC_Power_ratio < 0.5):
        mod_type = freq_mod_recognition(signal_5BW, fft_signal_5BW)
    else:
        gaussian_sigma = min(len(fft_signal_5BW)/(i_BW*2), len(fft_signal_5BW)/16)
        gaussian_half_size = gaussian_sigma*10
        # gaussian_x = fftsize/2-cp.abs(cp.arange(0, fftsize)-fftsize/2)
        gaussian_x = cp.abs(cp.arange(0, gaussian_half_size*2+1)-gaussian_half_size)
        gaussian_window = cp.exp(-cp.power(gaussian_x/gaussian_sigma, 2)/2)
        signal_5BW_gaussian_filtered = cp.convolve(signal_5BW, gaussian_window, mode='same')
        symbol_len = period_estimate(cp.fft.fft(cp.abs(signal_5BW_gaussian_filtered)), round(len(fft_signal_5BW)/i_BW))
        print("symbol_len:", symbol_len)
        if(symbol_len == 0):
            # AM
            mod_type = ["AM", 0]
        else:
            # 2ASK, BPSK, QPSK, 8PSK, 8QAM, 16QAM, ...
            # Symbol Clock Sync
            clk_sample_pattern = clock_sync(cp.abs(signal_5BW_gaussian_filtered), 1/symbol_len)
            # Try to do carrier sync with dirrerent orders
            for order_N in [1, 2, 4, 8, 16]:
                signal_N_order = cp.power(signal_slice, order_N)
                # print(order_N, "order.")
                pwr_fft_signal_Norder = cp.asnumpy(cp.abs(cp.fft.fft(signal_N_order)))
                
                # decide if there is a line spectrum and find it
                mask_threshold = np.zeros(slice_len)
                mask_threshold_len = min(100, round(slice_len/symbol_len))
                #pwr_fft_aa_4order_1 = [pwr_fft_aa_Norder(end-mask_threshold_len+1:end), pwr_fft_aa_Norder, pwr_fft_aa_Norder(1:mask_threshold_len)];
                pwr_fft_signal_Norder_cyc = np.concatenate((pwr_fft_signal_Norder[-mask_threshold_len:], pwr_fft_signal_Norder, pwr_fft_signal_Norder[:mask_threshold_len]))
                # for i in range(mask_threshold_len, slice_len+mask_threshold_len):
                line_spectrum_found = False
                for i in list(range(mask_threshold_len, mask_threshold_len+4*order_N+1)) + list(range(slice_len+mask_threshold_len-4*order_N-1, slice_len+mask_threshold_len)):
                    mask_threshold[i-mask_threshold_len] = max(np.max(pwr_fft_signal_Norder_cyc[i-mask_threshold_len:i-1]), np.max(pwr_fft_signal_Norder_cyc[i+2:i+mask_threshold_len+1]))
                    if(pwr_fft_signal_Norder[i-mask_threshold_len] - mask_threshold[i-mask_threshold_len]*2 > 0):
                        line_spectrum_found = True
                        i_carroer_orderN = i-mask_threshold_len
                if(line_spectrum_found):
                    # print('i_carroer found!:')
                    break
            print('order_N:', order_N)
            # print('i_carroer_orderN:', i_carroer_orderN)
            # plt.plot(pwr_fft_signal_Norder)
            # plt.plot(mask_threshold*2)
            # plt.show()

            # Carrier Sync
            carrier_recovered = N_order_Carrier_Sync(order_N, cp.asnumpy(signal_N_order), i_carroer_orderN/slice_len, 1/slice_len, 2/slice_len)
            # signal_sync = cp.asnumpy(signal_slice)*clk_sample_pattern*np.conj(carrier_recovered[0])
            # plt.plot(np.real(signal_sync))
            # plt.show()

            # generate symbol sample
            symbol_sample_index = np.nonzero(clk_sample_pattern)
            symbol_samples = cp.asnumpy(signal_slice)[symbol_sample_index]*np.conj(carrier_recovered[0][symbol_sample_index])
            
            mod_type = [constellation_recognition.constellation_recognition(symbol_samples), symbol_len]
            
            # draw comstellation


    # print(mod_type)
    return mod_type