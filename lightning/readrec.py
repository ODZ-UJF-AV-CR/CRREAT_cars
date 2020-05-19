import pandas as pd
import numpy as np
import sys

headerdt = np.dtype([
	("startOffset", "<i8"),
	("descSpan", "<i8"),
	("preTrigger", "<i8"),
	("postTrigger", "<i8"),
	("fractBase", "<i8")
])

syncposdt = np.dtype([
	("w", "<i8"),
	("f", "<u1")
])

def loadrec(file, skipsamples=False):
	head = np.frombuffer(file.read(headerdt.itemsize), dtype=headerdt)[0]
	samplebytes = (head['preTrigger'] + head['postTrigger']) * head['descSpan']
	if skipsamples:
		samples = None
		file.seek(headerdt.itemsize + samplebytes)
	else:
		samples = np.fromfile(file, count=samplebytes//16, dtype=np.dtype("(8,)<i2"))
	synclog = np.frombuffer(file.read(), dtype=syncposdt)

	return head, samples, synclog

def edges(rec):
	h, s, p = rec
	num_samples = 4096
	r = [
		(m['w'] - h['startOffset'], float(m['f']) / h['fractBase'])
		for m in p
	]

	return [
		(s[a-num_samples:a+num_samples], np.arange(-num_samples, num_samples) + b)
		for a, b in r
		if a > num_samples and a < len(s) - num_samples
	]

from matplotlib.ticker import Locator, FuncFormatter

class TimeTickLocator(Locator):
	def __init__(self, t2s, s2t):
		self.t2s, self.s2t = t2s, s2t
	
	def __call__(self):
		return self.tick_values(*self.axis.get_data_interval())
	
	def tick_values(self, vmin, vmax):
		intervals = [
			"10 s", "5 s", "2 s", "1 s",
			"500 ms", "200 ms", "100 ms", "50 ms",
			"20 ms", "10 ms", "5 ms", "2 ms", "1 ms"
		]
		tmin, tmax = map(self.s2t, (vmin, vmax))
        
		for inter in reversed(intervals):
			inter_td = pd.Timedelta(inter)
			no = (tmax - tmin)/pd.Timedelta(inter)
			if no <= 10:
				break
		
		ret = []
		tick = tmin.ceil(inter)
		while tick < tmax:
			ret.append(self.t2s(tick))
			tick += inter_td
		
		return ret

def assign_time_axis(fn, header, synclog):
	sps = 10e6

	# take approximate trigger sample position and time based on header contents and filename
	approx_trigger_pos = (header['preTrigger'] - 0.5) * header['descSpan']//16
	approx_trigger_time = pd.to_datetime(fn[4:], yearfirst=True)

	# we can convert any sample position to time by comparing to trigger time and sample position
	def approx_sample_time(pos):
		return approx_trigger_time + pd.Timedelta((pos - approx_trigger_pos) / sps, 'seconds')
	
	# take sample positions of sync edges
	synclog_rel = [s[0] - header['startOffset'] for s in synclog]
	
	# pick one synclog entry to use for synchronization
	synclog_pick = np.argmin(np.abs(synclog_rel))
	tick_pos = synclog_rel[synclog_pick]
	tick_time = approx_sample_time(tick_pos).round("1 s")
	#print(approx_sample_time(tick_pos), tick_time)
    
	t2s = lambda t: ((t-tick_time)/pd.Timedelta(1, 'seconds'))*sps + tick_pos
	s2t = lambda s: tick_time + pd.Timedelta((s - tick_pos)/sps, 'seconds')
    
	#print(approx_trigger_time, s2t(approx_trigger_pos))
	
	return t2s, s2t, TimeTickLocator(t2s, s2t), FuncFormatter(lambda x, _: s2t(x).strftime("%H:%M:%S.%f"))

from matplotlib import pyplot as plt
import scipy.signal
import numpy as np
import math
import traceback

def waterfallize_pre(signal, bins):
    window = 0.5 * (1.0 - np.cos((2 * math.pi * np.arange(bins)) / bins))
    segment = int(bins / 2)
    nsegments = int(len(signal) / segment)
    m = np.repeat(np.reshape(signal[0:segment * nsegments], (nsegments, segment)), 2, axis=0)
    t = np.reshape(m[1:len(m) - 1], (nsegments - 1, bins))
    img = np.multiply(t, window)
    wf = np.fft.fft(img)
    return np.concatenate((wf[:, int(bins / 2):bins], wf[:, 0:int(bins / 2)]), axis=1)

def waterfallize(signal, bins):
    return np.log(np.abs(waterfallize_pre(signal, bins)))

def abs2(x):
    return x.real**2 + x.imag**2

def wf_plotrec(samples, sample_rate, freq_offset=0, freq_lim=None, bins=8192, ax=None, title=None,
       offset=0):
    img = waterfallize(samples, bins).T
    img[np.isneginf(img)] = np.nan
    # ^^ might not be needed, was copied from pysdr-recviewer
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(24, 6))
    if title is not None:
        fig.suptitle(title)

    ax.imshow(img, extent=[offset, offset+len(samples), freq_offset + sample_rate/2, freq_offset - sample_rate/2],
             aspect='auto', interpolation='none', cmap='magma')
    ax.set_xlabel('Time [s]'); ax.set_ylabel('Frequency [Hz]');
    
    if freq_lim is not None:
        ax.set_ylim(freq_lim[0] + freq_offset, freq_lim[1] + freq_offset)

    return ax


def wf(samples, sample_rate, freq_offset=0, freq_lim=None, bins=8192, ax=None, title=None,
       offset=0):
    img = waterfallize(samples, bins).T
    img[np.isneginf(img)] = np.nan
    # ^^ might not be needed, was copied from pysdr-recviewer
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(24, 6))
    if title is not None:
        fig.suptitle(title)

    ax.imshow(img, extent=[offset/sample_rate, (offset+len(samples))/sample_rate, freq_offset + sample_rate/2, freq_offset - sample_rate/2],
             aspect='auto', interpolation='none', cmap='magma')
    ax.set_xlabel('Time [s]'); ax.set_ylabel('Frequency [Hz]');
    
    if freq_lim is not None:
        ax.set_ylim(freq_lim[0] + freq_offset, freq_lim[1] + freq_offset)

    return ax


def plotrec(h, samples, synclog, fn, pre_trigger_blocks=10, post_trigger_blocks=5, title=None,
            marktimes=[]):
    t2s, s2t, ticker, formatter = assign_time_axis(fn, h, synclog)
    
    if pre_trigger_blocks > h['preTrigger']:
        pre_trigger_blocks = h['preTrigger']
    if post_trigger_blocks > h['postTrigger']:
        post_trigger_blocks = h['postTrigger']
    
    a = (h['preTrigger']-pre_trigger_blocks)*h['descSpan']//16 #select block of samples before trigger
    b = (h['preTrigger']+post_trigger_blocks)*h['descSpan']//16  #select blocks after trigger 
    
    fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(figsize=(28, 28), nrows=8, sharex=True)
    if title is not None:
        fig.suptitle(title)
        
    ax1.xaxis.set_major_locator(ticker)
    ax1.xaxis.set_major_formatter(formatter)

    ax1.plot(range(a, b), samples[a:b,0:2], linestyle="",marker="o", markersize=1)
    ax1.set_title("Channels 0 and 1")
    wf_plotrec(samples[a:b,0] + 1j*samples[a:b,1], 10e6, bins=8192, ax=ax2, offset=a)

    ax3.plot(range(a, b), samples[a:b,2:4], linestyle="", marker="o", markersize=1)
    ax3.set_title("Channels 2 and 3")
    wf_plotrec(samples[a:b,2] + 1j*samples[a:b,3], 10e6, bins=8192, ax=ax4, offset=a)

    ax5.plot(range(a, b), samples[a:b,4:6], linestyle="", marker="o", markersize=1)
    ax5.set_title("Channels 4 and 5")
    wf_plotrec(samples[a:b,4] + 1j*samples[a:b,5], 10e6, bins=8192, ax=ax6, offset=a)

    ax7.plot(range(a, b), samples[a:b,6:8], linestyle="", marker="o", markersize=1)
    ax7.set_title("Channels 6 and 7")
    wf_plotrec(samples[a:b,6] + 1j*samples[a:b,7], 10e6, bins=8192, ax=ax8, offset=a)
    
    at, bt = s2t(a), s2t(b)
    for t in marktimes:
        if t > at and t < bt:
            for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]:
                ax.axvline(x=t2s(t), color='purple', ls='--')
    return fig
    #plt.show()
