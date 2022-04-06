import comm_read
import cupy as cp
import numpy as np
# import commpy
# import matplotlib.pyplot as plt
import scipy.signal
# By GuJi in WT&T, BUPT

print("[Info] Program start.")

signal_info = comm_read.get_singnal_IQs('comm_dataset.dat')
signal = signal_info['IQSamples']

print(
    'dataSerialNo:', signal_info['dataSerialNo'], 
    '\ngatheringTime:', signal_info['gatheringTime'], 
    '\nsampleRate:', signal_info['sampleRate'], 
    '\nIFFreq:', signal_info['IFFreq'], 
    '\nIFBandWidth:', signal_info['IFBandWidth'], 
    '\nworkingMode:', signal_info['workingMode'], 
    '\nprocessingMode:', signal_info['processingMode'], 
    '\nlisteningBandStart:', signal_info['listeningBandStart'], 
    '\nlisteningBandStop:', signal_info['listeningBandStop'], 
    '\nnofSamples:', signal_info['nofSamples']
    )
if(len(signal) != signal_info['nofSamples']):
    raise('Sample length dismatch!')

# TODO optimize the generation of window array
targetFreqResolution = 100e3
targetFreqClearane = 100e3
max_half_BW = 2e6
fs = signal_info['sampleRate']

targetFFTSize = round(fs/targetFreqResolution)
fftsize = 2**int(np.ceil(np.log2(targetFFTSize)))
overlap_len = 0

freq_continuation_tolerance = max(2, np.floor(targetFreqClearane/fs*fftsize/2))

nof_frames = int(np.floor(len(signal)/fftsize))
gaussian_sigma = targetFreqClearane/fs*fftsize/2
print('Frame size:', fftsize, ", gaussian_sigma:", gaussian_sigma, ',freq_continuation_tolerance:', freq_continuation_tolerance)
gaussian_half_size = gaussian_sigma*10
# gaussian_x = fftsize/2-cp.abs(cp.arange(0, fftsize)-fftsize/2)
gaussian_x = cp.abs(cp.arange(0, gaussian_half_size*2+1)-gaussian_half_size)
gaussian_window = cp.exp(-cp.power(gaussian_x/gaussian_sigma, 2)/2)
# ifft_gaussian_window = cp.real(cp.fft.fftshift(cp.fft.ifft(gaussian_window)))
# ifft_gaussian_window = ifft_gaussian_window + cp.roll(ifft_gaussian_window, -1)

# plt.plot(cp.asnumpy(cp.real(gaussian_window)))
# plt.show()
# exit()

# NOTE implemention of circular convolution in frequency domain
# by window function in time domain did not work properly. 
# Using direct convolution in frequency domain alternately. 

# fft_window = cp.blackman(fftsize)*ifft_gaussian_window
fft_window = cp.blackman(fftsize)

spectrum = cp.empty([nof_frames-1, fftsize])
for i_frame in range(nof_frames-1):
    # stft
    frame_with_window = cp.multiply(signal[i_frame*fftsize:(i_frame+1)*fftsize], fft_window)
    # fft_frame = cp.fft.fftshift(cp.fft.fft(frame_with_window))
    fft_frame = cp.fft.fft(frame_with_window)
    abs_fft_frame = cp.abs(fft_frame)
    power_fft_frame = cp.power(abs_fft_frame, 2)
    spectrum[i_frame] = cp.convolve(power_fft_frame, gaussian_window, mode='same')
# TODO use noise detect algorithm to determine the average noise level
spectrum_np = cp.asnumpy(cp.maximum(spectrum, cp.mean(spectrum)))

# cv2.imshow('WaterFall', spectrum_np/np.max(spectrum_np))
# cv2.waitKey()

# spectrum hostory records
class segment_t:
    start = 0
    length = 0
    freq = 0
    group = None
    def __init__(self, start, length, freq) -> None:
        self.start = start
        self.length = length
        self.freq = freq
        self.group = None
class previous_locs_t:
    start_time = 0
    presence_in_the_current_frame = 0
    last_freq_pos = 0
    def __init__(self, start_time, last_freq_pos) -> None:
        self.start_time = start_time
        self.last_freq_pos = last_freq_pos
        self.presence_in_the_current_frame = True
        pass

segment_start_time = cp.empty(fftsize, dtype=np.uint64)
segments = []
previous_locs = []
# last_freq_pos = np.empty(0, dtype=np.uint32)
for i_frame in range(nof_frames-1):
    # TODO optimize the peak finding procedure
    current_freq_pos, _ = scipy.signal.find_peaks(spectrum_np[i_frame])
    # print(current_freq_pos)
    # plt.plot(cp.asnumpy(spectrum_np[i_frame]))
    # plt.show()
    # find new start of segments
    for c_pos in current_freq_pos:
        # decide if the current pos is a new start
        new_start = True
        for previous_loc in previous_locs:
            if(abs(c_pos-previous_loc.last_freq_pos) <= freq_continuation_tolerance):
                new_start = False
                previous_loc.presence_in_the_current_frame = True
                previous_loc.last_freq_pos = c_pos
                break
        if(new_start):
            previous_locs.append(previous_locs_t(i_frame, c_pos))
            
    i = 0
    while True:
        if(i >= len(previous_locs)): break
        if(previous_locs[i].presence_in_the_current_frame == False):
            # new signal segment detected
            if(i_frame - previous_locs[i].start_time > 2):
                segments.append(segment_t(previous_locs[i].start_time, i_frame-previous_locs[i].start_time, previous_locs[i].last_freq_pos))
                # print(i_frame-previous_locs[i].start_time)
            previous_locs.pop(i)
        else:
            previous_locs[i].presence_in_the_current_frame = False
            i += 1

# for segment in segments:
#     print(segment.length)

# start clustering (start from the latest signal)
segments_ungrouped = segments.copy()

groups = []
while(True):
    if(len(segments_ungrouped) == 0): break
    seg_to_match = segments_ungrouped.pop()
    group = [seg_to_match]
    for i in range(len(segments_ungrouped)-1, -1, -1):
        # add the matching segments to the group
        print(
            "current_end:", segments_ungrouped[i].start + segments_ungrouped[i].length - 1, 
            ", matching start:", seg_to_match.start, 
            ", current len:", segments_ungrouped[i].length, 
            ", matching len:", seg_to_match.length
        )
        if(
            (abs(segments_ungrouped[i].start + segments_ungrouped[i].length - 1 - seg_to_match.start) <= 2) and 
            (abs(segments_ungrouped[i].length - seg_to_match.length) <= 2)):
            seg_to_match = segments_ungrouped.pop(i)
            group.append(seg_to_match)
    if(len(group) >= 5):
        group.reverse()
        groups.append(group)
WTXX = []
# for group in groups:
for group in groups:
    print("================ group ===============")

    freq_array = np.empty(len(group))
    for i_seg in range(len(group)):
        freq_array[i_seg] = group[i_seg].freq

    # decide freq hopping cycle len
    # TODO cycle detection algorithm should be carefully rewritten
    offset_error = np.zeros(len(group))
    # freq_hopping_cycle_len = 0
    for i_offset in range(2, len(group)-2):
        overlap_len = len(group)-i_offset
        offset_error[i_offset] = np.sum(np.abs(freq_array[i_offset:]-freq_array[:-i_offset]))/overlap_len
    # print("!!!!!!!!!!!!!!!!!!!!!!!!\n", offset_error)
    
    offset_error = offset_error / np.sqrt(np.var(freq_array))
    # freq_hopping_cycle_len = 0
    # for i_offset in range(2, len(group)-2):
    #     if(np.sum(np.abs(freq_array[0:2]-freq_array[i_offset:i_offset+2]))<10):
    #         freq_hopping_cycle_len = i_offset
    #         break
    target_offset_error = max(min(offset_error[2:len(group)-2])*10, 1e-2)
    # print(target_offset_error)
    freq_hopping_cycle_len = 0
    for i_offset in range(2, len(group)-2):
        if(offset_error[i_offset] <= target_offset_error):
            freq_hopping_cycle_len = i_offset
            break
    nof_cycles = np.floor(len(freq_array)/freq_hopping_cycle_len)
    freq_array_grouped = np.reshape(freq_array[:int(nof_cycles*freq_hopping_cycle_len)], [int(nof_cycles),freq_hopping_cycle_len])
    freq_array_average = np.average(freq_array_grouped, axis=0)
    # print(freq_array_grouped)
    if(freq_hopping_cycle_len != 0):
        print("freq_hopping_cycle_len:", freq_hopping_cycle_len)
        # print("freq hopping pattern(MHz):", (freq_array[0:freq_hopping_cycle_len]/fftsize-0.5)*fs/1e6)
        freq_hopping_pattern = (freq_array_average/fftsize)*fs/1e6
        print("freq hopping pattern(MHz):", freq_hopping_pattern)

    # Calcuate hopping speed
    hopping_len_in_time = (group[-1].start+group[-1].length-group[0].start)/len(group)*fftsize/fs
    hopping_speed_in_Hertz = 1/hopping_len_in_time
    print("hopping speed(Hz):", hopping_speed_in_Hertz)
    WTXX.append({
        'TS': str(hopping_speed_in_Hertz),# 跳速
        'PLZ': str(freq_hopping_pattern.tolist())[1:-1],  # 频率值
        'TPTA':str(freq_hopping_pattern.tolist())[1:-1]
    })

DWJJ = "北京邮电大学_零幺零队_通信调制识别_1BUPT010" # TODO 检查一下
WTGS = str(len(groups))
json_to_send = {
    "DWJJ": DWJJ,
    "WTGS": WTGS,
    "WTXX": WTXX
}
print(json_to_send)
    # print()