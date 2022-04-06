import cupy as cp
import numpy as np
# import matplotlib.pyplot as plt
# By GuJi in WT&T, BUPT
def main_lobe_BW_estimate(fft_signal, BW_decision_relative_power_in_dB):
    slice_len = len(fft_signal)

    DC_skipping_len = 5
    pwr_spectrum = cp.abs(fft_signal)**2
    logpwr_spectrum = cp.asnumpy(cp.log(pwr_spectrum))
    logpwr_spectrum[:DC_skipping_len] = np.max(logpwr_spectrum[DC_skipping_len:-DC_skipping_len])-100
    logpwr_spectrum[-DC_skipping_len:] = np.max(logpwr_spectrum[DC_skipping_len:-DC_skipping_len])-100
    logpwr_spectrum = np.clip(logpwr_spectrum, np.max(logpwr_spectrum)-100, None)
    equivalent_rectangular_i_BW = int(np.round(np.sum(pwr_spectrum)/np.max(pwr_spectrum)))
    # smooth_window = 10;
    # logpwr_spectrum_smoothed = conv(logpwr_spectrum, ones(1, 1+smooth_window*2))/(smooth_window*2+1);
    # logpwr_spectrum_smoothed = logpwr_spectrum_smoothed(smooth_window+1:end-smooth_window);
    logpwr_spectrum_smoothed = np.zeros(slice_len)
    logpwr_fall_acc = 0.01
    logpwr_fall_speed = 0
    logpwr_now = logpwr_spectrum[0]
    for i in range(slice_len):
        logpwr_fall_speed = logpwr_fall_speed + logpwr_fall_acc
        logpwr_now = logpwr_now - logpwr_fall_speed
        if(logpwr_now < logpwr_spectrum[i]):
            logpwr_now = logpwr_spectrum[i]
            logpwr_fall_speed = 0
        logpwr_spectrum_smoothed[i] = logpwr_now
    # plot(logpwr_spectrum_smoothed)

    # BW_decision_relative_power_in_dB = 7.5
    spectrum_peak_detection_tolerane = 2
    max_logpwr_spectrum = max(logpwr_spectrum_smoothed)

    # for i = floor(slice_len/2):-1:1
    #     if(logpwr_spectrum_smoothed(i)+BW_decision_relative_power_in_dB >= max_logpwr_spectrum)
    #         i_BW = i;
    #         break
    #     end
    # end
    i_BW = 1
    for i in range(int(slice_len/2)-1, -1, -1):
        if(logpwr_spectrum_smoothed[i]+spectrum_peak_detection_tolerane >= max_logpwr_spectrum):
            last_peak = i
            break
    for i in range(last_peak,int(slice_len/2)):
        if(logpwr_spectrum_smoothed[i]+BW_decision_relative_power_in_dB <= max_logpwr_spectrum):
            i_BW = i
            break
    i_BW = max(i_BW, equivalent_rectangular_i_BW)
    BW_indication = logpwr_spectrum.copy()
    BW_indication[i_BW+1:] = -30
    # plt.plot(logpwr_spectrum)
    # plt.plot(BW_indication)
    # plt.show()
    return i_BW