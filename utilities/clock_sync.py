import numpy as np
import cupy as cp
# import matplotlib.pyplot as plt
# By GuJi in WT&T, BUPT

def clock_sync(envelope, estimated_symbol_rate):
#     x = 1:1000000;
#     pwr = sin(x*2*pi*352.745/1000000+95.1534);
#     plot(pwr);

    envelope_normal = cp.asnumpy(envelope/cp.max(envelope))
    # fft_pwr = fft(envelope_normal);
    free_symbol_rate = estimated_symbol_rate
    loop_gain_k0 = free_symbol_rate*0.1
    loop_gain_k1 = free_symbol_rate*0.01

    dll_dt_span = 0.1
    t_symbol = 0
    siglen = len(envelope_normal)
    clk_sample_pattern = np.zeros(siglen, dtype=np.bool)
    last_early_factor = 0
    dll_symbol_rate = free_symbol_rate
    integral_dll_symbol_rate = 0
    while True:
        t_symbol = t_symbol + 1/dll_symbol_rate
        if t_symbol+0.5/dll_symbol_rate>siglen-1:
            break
        t_early = t_symbol - dll_dt_span/dll_symbol_rate
        t_late = t_symbol + dll_dt_span/dll_symbol_rate
        late_factor = -envelope_normal[round(t_late)]+envelope_normal[round(t_early)]
#         d_error_factor = abs(late_factor)-abs(last_early_factor);
#         last_early_factor = late_factor;
        dll_symbol_rate = free_symbol_rate+loop_gain_k0*late_factor+integral_dll_symbol_rate
        # integral_dll_symbol_rate = integral_dll_symbol_rate + loop_gain_k1*late_factor;
        integral_dll_symbol_rate = integral_dll_symbol_rate + loop_gain_k1*(late_factor-integral_dll_symbol_rate)
        # dll_symbol_rate = dll_symbol_rate - loop_gain_k1*early_factor;
        # clk_sample_pattern(round(t_symbol)) = late_factor*10;
    
    loop_gain_k0 = free_symbol_rate*0.01
    loop_gain_k1 = free_symbol_rate*0.001
    
    while(True):
        t_symbol = t_symbol - 1/dll_symbol_rate
        if(t_symbol-0.5/dll_symbol_rate<0):
            break
        t_early = t_symbol + dll_dt_span/dll_symbol_rate
        t_late = t_symbol - dll_dt_span/dll_symbol_rate
        late_factor = -envelope_normal[round(t_late)]+envelope_normal[round(t_early)]
#         d_error_factor = abs(late_factor)-abs(last_early_factor);
#         last_early_factor = late_factor;
        dll_symbol_rate = free_symbol_rate+loop_gain_k0*late_factor+integral_dll_symbol_rate
        # integral_dll_symbol_rate = integral_dll_symbol_rate + loop_gain_k1*late_factor;
        integral_dll_symbol_rate = integral_dll_symbol_rate + loop_gain_k1*(late_factor-integral_dll_symbol_rate)
        # dll_symbol_rate = dll_symbol_rate - loop_gain_k1*early_factor;
        # clk_sample_pattern(round(t_symbol)) = late_factor*10;
    
    while(True):
        t_symbol = t_symbol + 1/dll_symbol_rate
        if(t_symbol+0.5/dll_symbol_rate>siglen-1):
            break
        t_early = t_symbol - dll_dt_span/dll_symbol_rate
        t_late = t_symbol + dll_dt_span/dll_symbol_rate
        late_factor = -envelope_normal[round(t_late)]+envelope_normal[round(t_early)]
#         d_error_factor = abs(late_factor)-abs(last_early_factor);
#         last_early_factor = late_factor;
        dll_symbol_rate = free_symbol_rate+loop_gain_k0*late_factor+integral_dll_symbol_rate
        # integral_dll_symbol_rate = integral_dll_symbol_rate + loop_gain_k1*late_factor;
        integral_dll_symbol_rate = integral_dll_symbol_rate + loop_gain_k1*(late_factor-integral_dll_symbol_rate)
        # dll_symbol_rate = dll_symbol_rate - loop_gain_k1*early_factor;
        clk_sample_pattern[round(t_symbol)] = 1
    
    
    # plt.plot(envelope_normal)
    # plt.plot(clk_sample_pattern)
    # plt.show()
    return clk_sample_pattern