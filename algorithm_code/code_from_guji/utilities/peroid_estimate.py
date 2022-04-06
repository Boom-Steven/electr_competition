import cupy as cp
import numpy as np
# import matplotlib.pyplot as plt
# By GuJi in WT&T, BUPT
def period_estimate(fft_x_in, estimated_period):
    circular_spectrum = cp.asnumpy(cp.abs(fft_x_in)).copy()
    len_x = len(fft_x_in)
    neighbor_radius = max(round(len_x/estimated_period/10), 4)
    envelope_circular_spectrum_background_threshold = np.zeros(len_x)
    envelope_border = round(1+len_x/2)
    circular_spectrum[envelope_border:] = 0
    for i in range(int(max(np.ceil(len_x/estimated_period/4)-1, neighbor_radius)),int(np.floor(len_x/4*3))):
        envelope_circular_spectrum_background_threshold[i] = max(np.max(circular_spectrum[i-neighbor_radius:i-1]), np.max(circular_spectrum[i+2:i+neighbor_radius+1]))
    # plt.plot(circular_spectrum)
    # plt.plot(envelope_circular_spectrum_background_threshold*2)
    # plt.show()
    # plot(envelope_circular_spectrum_smoothed*5);

    # symbol_rate_found = False
    period_len = 0
    for i in range(int(np.ceil(len_x/estimated_period/4)-1), int(np.floor(len_x/4*3))):
        if(circular_spectrum[i]>envelope_circular_spectrum_background_threshold[i]*2):
            symbol_rate = i/len_x
            period_len = round(1/symbol_rate)
            # symbol_rate_found = true;
            break
    return period_len

