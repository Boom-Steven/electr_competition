import numpy as np
# import matplotlib.pyplot as plt
import cv2
# init_reference_constellations
# By GuJi in WT&T, BUPT

constellation_2ASK = np.array([0, np.sqrt(2)])
constellation_2ASK_2 = -np.array([0, np.sqrt(2)])
constellation_BPSK = np.array([-1, 1])
constellation_QPSK = np.exp(1j*np.array(range(4))/4*2*np.pi)
constellation_8PSK = np.exp(1j*np.array(range(8))/8*2*np.pi)

constellation_8QAM = np.array([1, 1+1j, 1j, -1+1j, -1, -1-1j, -1j, 1-1j]) * (1+1j)
constellation_8QAM = constellation_8QAM / np.sqrt(np.mean(np.abs(constellation_8QAM)**2))

constellation_symbols = [constellation_2ASK, constellation_2ASK_2, constellation_BPSK, constellation_QPSK, constellation_8PSK, constellation_8QAM]
constellation_names   = ['2ASK', '2ASK', 'BPSK', 'QPSK', '8PSK', '8QAM']
# constellation_32QAM = 
for N_QAM_in_one_branch in [4, 8, 16]:
    constellation_N2QAM = np.empty(N_QAM_in_one_branch**2, dtype=np.complex64)
    for x_I in range(N_QAM_in_one_branch):
        for x_Q in range(N_QAM_in_one_branch):
            constellation_N2QAM[x_I*N_QAM_in_one_branch+x_Q] = x_I + 1j*x_Q
    constellation_N2QAM = constellation_N2QAM - np.mean(constellation_N2QAM)
    constellation_N2QAM = constellation_N2QAM * (1+1j)
    constellation_N2QAM = constellation_N2QAM / np.sqrt(np.mean(np.abs(constellation_N2QAM)**2))
    constellation_symbols.append(constellation_N2QAM)
    constellation_names.append(str(N_QAM_in_one_branch**2)+'QAM')

# for i in range(len(constellation_symbols)):
#     x = constellation_symbols[i]
#     print(constellation_names[i])
#     plt.scatter(np.real(x), np.imag(x))
#     plt.show()

def constellation_recognition(symbol_samples):
    symbol_samples_normalized = symbol_samples / np.sqrt(np.mean(np.abs(symbol_samples)**2)) * np.sqrt(0.5) * (1+1j)
    # select most occured values
    resolution = 512
    hist_range = max(np.max(np.abs(np.real(symbol_samples_normalized))), np.max(np.abs(np.imag(symbol_samples_normalized))))/0.9
    (hist_symbols, xedges, yedges) = np.histogram2d(np.real(symbol_samples_normalized), np.imag(symbol_samples_normalized), bins=resolution, range=[[-hist_range, hist_range], [-hist_range, hist_range]])
    hist_symbols = cv2.GaussianBlur(hist_symbols, (0, 0), resolution/128)
    peak_indication = peak_find_2d(hist_symbols)

    [Is_hist, Qs_hist] = np.nonzero(peak_indication)
    Is = (Is_hist/(resolution-1))*(xedges[-2]-xedges[0]) + np.mean(xedges[:2])
    Qs = (Qs_hist/(resolution-1))*(yedges[-2]-yedges[0]) + np.mean(yedges[:2])
    symbol_samples_selected = (Is+1j*Qs) * np.sqrt(0.5) * (1-1j)
    symbol_weights = hist_symbols[(Is_hist, Qs_hist)]

    # symbol_samples_normalized = symbol_samples_normalized.reshape((1, len(symbol_samples_normalized)))
    error_score = np.empty(len(constellation_symbols))
    for i in range(len(constellation_symbols)):
        constellation_symbol_ref_vector = constellation_symbols[i].reshape((len(constellation_symbols[i]), 1))
        errors = np.abs(symbol_samples_selected - constellation_symbol_ref_vector)
        average_error = np.mean(np.min(errors, axis=0)*symbol_weights)
        demod_symbol_i = np.argmin(errors, axis=0)
        # print(demod_symbol_i)
        unique_demod_symbol_i = np.unique(demod_symbol_i)
        # print(unique_demod_symbol_i)
        occupied_proportion = np.size(unique_demod_symbol_i)/np.size(constellation_symbol_ref_vector)
        error_score[i] = average_error/(occupied_proportion**2) # +(1-occupied_proportion)
        # print(average_error, error_score[i])
        
        # plt.scatter(np.real(symbol_samples_selected), np.imag(symbol_samples_selected))
        # plt.scatter(np.real(constellation_symbol_ref_vector), np.imag(constellation_symbol_ref_vector))
        # plt.show()
    i_mod = np.argmin(error_score)
    return constellation_names[i_mod]

def peak_find_2d(image):
    len_x = np.size(image, axis=1)
    len_y = np.size(image, axis=0)
    image_leftshift = np.concatenate((image[:, 1:], np.zeros([len_y, 1])), axis=1)
    image_rightshift = np.concatenate((np.zeros([len_y, 1]), image[:, :-1]), axis=1)
    image_downshift = np.concatenate((np.zeros([1, len_x]), image[:-1, :]), axis=0)
    image_upshift = np.concatenate((image[1:, :], np.zeros([1, len_x])), axis=0)

    grad_1 = np.clip(image - image_leftshift, 0, None)
    grad_2 = np.clip(image - image_rightshift, 0, None)
    grad_3 = np.clip(image - image_downshift, 0, None)
    grad_4 = np.clip(image - image_upshift, 0, None)

    grad_all = grad_1*grad_2*grad_3*grad_4

    grad_all[np.nonzero(grad_all)] = 1
    return grad_all