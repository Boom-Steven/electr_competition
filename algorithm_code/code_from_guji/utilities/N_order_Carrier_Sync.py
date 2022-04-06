import numpy as np
# import matplotlib.pyplot as plt
# By GuJi in WT&T, BUPT
def N_order_Carrier_Sync(order_N, signal, estimated_freq, loop_BW, max_freq_err):
    signal_normal = signal/np.sqrt(np.mean(np.abs(signal)**2))
    free_freq = estimated_freq
    loop_gain_k0 = max_freq_err * 10
    loop_gain_k1 = loop_BW * max_freq_err*100

    siglen = len(signal_normal)
    # phase_base = zeros(1, siglen)
    carrier_base = np.zeros(siglen, dtype=np.complex64)
    # phase_following = zeros(1, siglen)
    integral_following_freqs = np.zeros(siglen, dtype=np.complex64)
    carrier_following = np.zeros(siglen, dtype=np.complex64)
    LF_ins = np.zeros(siglen)
    delta_freq = np.zeros(siglen)

    phase_following = 0
    following_freq = free_freq
    integral_followint_freq = 0
    
    for i in range(siglen):
        phase_following = np.mod(phase_following + following_freq*2*np.pi, 2*np.pi*order_N)
        
        carrier_now = np.exp(1j*phase_following)
        LF_in = np.imag(signal_normal[i]*np.conj(carrier_now))
        integral_followint_freq = integral_followint_freq + loop_gain_k1 * LF_in
        following_freq = free_freq + integral_followint_freq + loop_gain_k0 * LF_in

    for i in range(siglen-1, -1, -1):
        phase_following = np.mod(phase_following - following_freq*2*np.pi, 2*np.pi*order_N)
        
        carrier_now = np.exp(1j*phase_following)
        LF_in = -np.imag(signal_normal[i]*np.conj(carrier_now))
        integral_followint_freq = integral_followint_freq + loop_gain_k1 * LF_in
        following_freq = free_freq + integral_followint_freq + loop_gain_k0 * LF_in
    
    loop_gain_k0 = max_freq_err * 10
    loop_gain_k1 = loop_BW * max_freq_err*100
    
    for i in range(siglen):
        phase_following = np.mod(phase_following + following_freq*2*np.pi, 2*np.pi*order_N)
        
        delta_freq[i] = following_freq - free_freq
        carrier_now = np.exp(1j*phase_following)
        carrier_base[i] = np.exp(1j*phase_following/order_N)
        carrier_following[i] = carrier_now
        LF_in = np.imag(signal_normal[i]*np.conj(carrier_now))
        LF_ins[i] = LF_in
        integral_followint_freq = integral_followint_freq + loop_gain_k1 * LF_in
        following_freq = free_freq + integral_followint_freq + loop_gain_k0 * LF_in
        integral_following_freqs[i] = integral_followint_freq
    # plt.plot((np.real(signal_normal)))
    # plt.plot((np.real(carrier_following)))
    # plt.plot((LF_ins))
    # plt.plot((delta_freq/max_freq_err/100))
    # plt.show()
    return [carrier_base, integral_following_freqs]