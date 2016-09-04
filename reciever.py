import pyaudio 
import wave
import numpy as np
from subprocess import call
import matplotlib.pyplot as plt
from scipy.fftpack import fft, rfft
from scipy.io import wavfile # get the api
from time import sleep
import timeit

def get_audio(RECORD_SECONDS):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	WAVE_OUTPUT_FILENAME = "output.wav"

	p = pyaudio.PyAudio()


	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()




def freq_listener():
	#listen for reciever tone
	#take a sound every .1 seconds 
	big_ass_array = []
	get_audio(10)
	fs, data = wavfile.read('output.wav') # load the data
	a = data.T[0] # this is a two channel soundtrack, I get the first track
	b = [(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
	for i in range(90):
		section = b[int(i * 4403.2) : int((i + 1) * 4403.2)]
		c = fft(section) # calculate fourier transform (complex numbers list)
		d = len(c)  # you only need half of the fft list (real signal symmetry)
		freqs = np.fft.fftfreq(d)
		maxPositions = np.argsort(abs(c.imag))[len(c.imag) - 20 : len(c.imag)][:-1]
		freq = freqs[maxPositions]*44100
		freq_in_right_range = freq[np.logical_and(freq > 350, freq < 700)]
		if len(freq_in_right_range) > 0:
			big_ass_array.append(freq_in_right_range[0])

		print len(section)
		#print b
		print fs

	return big_ass_array
		# plt.plot(abs(c[:1000]),'r') 
		# plt.show()

#def seq_listener(tones):
	

print freq_listener()